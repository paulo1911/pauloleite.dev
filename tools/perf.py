#!/usr/bin/env python3
"""Medição de performance em Chrome headless com throttling (Slow 4G + CPU 4x), cache desligado.
Serve o site com gzip e Cache-Control como o GitHub Pages. Reporta FCP, LCP, CLS, requisições e bytes
transferidos (mediana de N execuções). Requer: Chrome, `pip install websocket-client`.
Uso: python3 tools/perf.py [N=3]"""
import gzip, http.server, json, os, statistics, subprocess, sys, tempfile, threading, time, urllib.request
import websocket

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8766
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PAGES = ['/', '/conhecimento/', '/mentoria/', '/conhecimento/system-design/', '/projetos/', '/conecte-se/']
GZ = ('.html', '.css', '.js', '.svg', '.json', '.xml', '.txt')

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.translate_path(self.path.split('?')[0])
        if os.path.isdir(path): path = os.path.join(path, 'index.html')
        if not os.path.exists(path): return super().do_GET()
        data = open(path, 'rb').read()
        ctype = self.guess_type(path)
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'max-age=600')
        if path.endswith(GZ) and 'gzip' in self.headers.get('Accept-Encoding', ''):
            data = gzip.compress(data); self.send_header('Content-Encoding', 'gzip')
        self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)

srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

proc = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=9334', '--user-data-dir=' + tempfile.mkdtemp(), '--no-first-run', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            tabs = [t for t in json.load(urllib.request.urlopen('http://localhost:9334/json')) if t.get('type') == 'page']
            if tabs: break
        except Exception: pass
        time.sleep(0.2)
    ws = websocket.create_connection(tabs[0]['webSocketDebuggerUrl'], timeout=60, suppress_origin=True)
    n = [0]; events = []
    def send(method, **p):
        n[0] += 1; ws.send(json.dumps({'id': n[0], 'method': method, 'params': p}))
        while True:
            m = json.loads(ws.recv())
            if 'method' in m: events.append(m)
            if m.get('id') == n[0]: return m.get('result', {})
    def ev(x): return send('Runtime.evaluate', expression=x, returnByValue=True).get('result', {}).get('value')
    for d in ('Page', 'Runtime', 'Network'): send(d + '.enable')
    send('Network.setCacheDisabled', cacheDisabled=True)
    send('Network.emulateNetworkConditions', offline=False, latency=150, downloadThroughput=int(1.6 * 1024 * 1024 / 8), uploadThroughput=int(750 * 1024 / 8))
    send('Emulation.setCPUThrottlingRate', rate=4)
    send('Emulation.setDeviceMetricsOverride', width=390, height=844, deviceScaleFactor=2, mobile=True)
    send('Page.addScriptToEvaluateOnNewDocument', source="""window.__m={lcp:0,cls:0};
      new PerformanceObserver(l=>{for(const e of l.getEntries())window.__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
      new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__m.cls+=e.value}).observe({type:'layout-shift',buffered:true});""")
    print(f"Perfil: mobile 390px @2x, Slow 4G (1.6 Mbps, 150 ms RTT), CPU 4x, gzip, sem cache — mediana de {RUNS} execuções")
    print(f"{'página':16} {'FCP ms':>7} {'LCP ms':>7} {'CLS':>6} {'req':>4} {'KB transf.':>10}")
    for path in PAGES:
        rows = []
        for _ in range(RUNS):
            send('Page.navigate', url='about:blank'); time.sleep(0.3); events.clear()
            send('Page.navigate', url=f'http://127.0.0.1:{PORT}{path}')
            for _ in range(200):
                if ev("document.readyState==='complete'"): break
                time.sleep(0.1)
            time.sleep(1.2)
            fcp = ev("(performance.getEntriesByName('first-contentful-paint')[0]||{}).startTime") or 0
            m = ev("JSON.stringify(window.__m)"); m = json.loads(m)
            fin = [e for e in events if e['method'] == 'Network.loadingFinished']
            req = len([e for e in events if e['method'] == 'Network.requestWillBeSent' and e['params']['request']['url'].startswith('http://127.0.0.1')])
            kb = sum(e['params']['encodedDataLength'] for e in fin) / 1024
            rows.append((fcp, m['lcp'], m['cls'], req, kb))
        med = [statistics.median(c) for c in zip(*rows)]
        print(f"{path:16} {med[0]:7.0f} {med[1]:7.0f} {med[2]:6.3f} {med[3]:4.0f} {med[4]:10.1f}")
finally:
    proc.terminate(); srv.shutdown()
