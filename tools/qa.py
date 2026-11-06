#!/usr/bin/env python3
"""QA automatizado via Chrome headless (CDP): axe-core (WCAG 2.2 AA), overflow horizontal,
menu mobile, foco por teclado e métricas básicas de performance.
Requer: Google Chrome, `pip install websocket-client`, servidor local em :8765
(python3 -m http.server 8765 na raiz). Uso: python3 tools/qa.py"""
import json, subprocess, time, urllib.request, os, sys, tempfile
import websocket

BASE = 'http://localhost:8765'
PAGES = ['/', '/sobre/', '/conhecimento/', '/mentoria/', '/conhecimento/system-design/', '/conhecimento/plano-de-acao/', '/projetos/', '/privacidade/', '/conecte-se/', '/404.html']
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
AXE = os.path.join(tempfile.gettempdir(), 'axe.min.js')
if not os.path.exists(AXE):
    urllib.request.urlretrieve('https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js', AXE)
axe_src = open(AXE, encoding='utf8').read()

proc = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=9333', '--user-data-dir=' + tempfile.mkdtemp(), '--no-first-run', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            tabs = [t for t in json.load(urllib.request.urlopen('http://localhost:9333/json')) if t.get('type') == 'page']
            if tabs: break
            time.sleep(0.2)
        except Exception: time.sleep(0.2)
    ws = websocket.create_connection(tabs[0]['webSocketDebuggerUrl'], timeout=30, suppress_origin=True)
    _id = [0]; logs = []
    def send(method, **params):
        _id[0] += 1; ws.send(json.dumps({'id': _id[0], 'method': method, 'params': params}))
        while True:
            m = json.loads(ws.recv())
            if m.get('method') == 'Runtime.exceptionThrown': logs.append(m['params']['exceptionDetails']['text'])
            if m.get('method') == 'Log.entryAdded' and m['params']['entry']['level'] in ('error',): logs.append(m['params']['entry']['text'] + ' ' + m['params']['entry'].get('url', ''))
            if m.get('id') == _id[0]: return m.get('result', {})
    def ev(expr):
        r = send('Runtime.evaluate', expression=expr, awaitPromise=True, returnByValue=True)
        return r.get('result', {}).get('value')
    for d in ('Page', 'Runtime', 'Log'): send(d + '.enable')
    def nav(url):
        r = send('Page.navigate', url=url)
        if r.get('errorText'): print('NAV ERROR', url, r['errorText'])
        for _ in range(100):
            if ev("document.readyState==='complete' && location.href!=='about:blank'"): break
            time.sleep(0.1)
        ev('document.fonts.ready.then(()=>1)'); time.sleep(0.5)
    fails = 0
    for vp, (w, h, mob) in {'desktop': (1280, 900, False), 'mobile': (390, 844, True)}.items():
        send('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=mob)
        for path in PAGES:
            logs.clear()
            nav(BASE + path)
            ev(axe_src)
            res = ev("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}}).then(r=>JSON.stringify({v:r.violations.map(x=>({id:x.id,impact:x.impact,n:x.nodes.length,t:x.nodes.slice(0,2).map(n=>n.target.join(' '))})),p:r.passes.length}))")
            r = json.loads(res)
            ov = ev('document.documentElement.scrollWidth > window.innerWidth + 1')
            perf = ev("(()=>{const n=performance.getEntriesByType('navigation')[0];const f=performance.getEntriesByName('first-contentful-paint')[0];return JSON.stringify({dcl:Math.round(n.domContentLoadedEventEnd),load:Math.round(n.loadEventEnd),fcp:f?Math.round(f.startTime):null})})()")
            tag = 'OK ' if not r['v'] and not ov and not logs else 'FAIL'
            if tag == 'FAIL': fails += 1
            print(f"[{tag}] {vp:7} {path:16} axe-violations={len(r['v'])} overflow={ov} console-errors={len(logs)} perf={perf}")
            for v in r['v']: print('      ', v)
            for l in logs: print('       log:', l)
    # menu mobile + teclado
    send('Emulation.setDeviceMetricsOverride', width=390, height=844, deviceScaleFactor=1, mobile=True)
    nav(BASE + '/')
    t = lambda x: ev(x)
    nav_hidden = ev("getComputedStyle(document.getElementById('nav')).display==='none'")
    ev("document.querySelector('.nav-toggle').click()")
    opened = ev("document.querySelector('.nav-toggle').getAttribute('aria-expanded')==='true' && getComputedStyle(document.getElementById('nav')).display!=='none'")
    ev("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}))")
    closed = ev("document.querySelector('.nav-toggle').getAttribute('aria-expanded')==='false' && getComputedStyle(document.getElementById('nav')).display==='none'")
    print(f"[{'OK ' if nav_hidden and opened and closed else 'FAIL'}] menu mobile: fechado inicial={nav_hidden} abre={opened} Esc fecha={closed}")
    fails += 0 if (nav_hidden and opened and closed) else 1
    send('Emulation.setDeviceMetricsOverride', width=1280, height=900, deviceScaleFactor=1, mobile=False)
    nav(BASE + '/')
    focus = ev("""(()=>{const els=[...document.querySelectorAll('a[href],button,summary')].filter(e=>e.offsetParent!==null||e.classList.contains('skip-link'));
      let bad=[];for(const e of els){e.focus();const cs=getComputedStyle(e);const cl=e.classList.contains('card__link');
      const a=cl?getComputedStyle(e,'::after'):cs; if(!(document.activeElement===e)) bad.push('nofocus '+(e.textContent||'').trim().slice(0,20));}
      return JSON.stringify({total:els.length,bad:bad,first:document.querySelector('a[href]').className})})()""")
    print('[INFO] foco/teclado:', focus)
    print('RESULTADO:', 'FALHAS=%d' % fails)
    sys.exit(1 if fails else 0)
finally:
    proc.terminate()
