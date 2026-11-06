#!/usr/bin/env python3
"""Verificações de SEO nos arquivos gerados (somente stdlib). Uso: python3 tools/seo_check.py"""
import json, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site = json.load(open(os.path.join(ROOT, 'data', 'site.json'), encoding='utf8'))
D = site['domain']
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf8').read()
locs = re.findall(r'<loc>([^<]+)</loc><lastmod>([^<]*)</lastmod>', sm)
fails, titles, descs = [], {}, {}
def bad(m): fails.append(m); print('[FAIL]', m)
for loc, lm in locs:
    path = loc[len(D) + 1:]
    f = os.path.join(ROOT, path, 'index.html') if not path.endswith('.html') else os.path.join(ROOT, path)
    h = open(f, encoding='utf8').read()
    try: datetime.date.fromisoformat(lm)
    except Exception: bad(f'{loc}: lastmod inválido "{lm}"')
    t = re.search(r'<title>([^<]+)</title>', h); d = re.search(r'name="description" content="([^"]*)"', h)
    c = re.search(r'rel="canonical" href="([^"]+)"', h)
    if not t or not d or not c: bad(f'{loc}: falta title/description/canonical'); continue
    if c.group(1) != loc: bad(f'{loc}: canonical diferente ({c.group(1)})')
    if not 15 <= len(t.group(1)) <= 70: bad(f'{loc}: title com {len(t.group(1))} caracteres')
    if not 70 <= len(d.group(1)) <= 170: bad(f'{loc}: description com {len(d.group(1))} caracteres')
    if titles.setdefault(t.group(1), loc) != loc: bad(f'{loc}: title duplicado com {titles[t.group(1)]}')
    if descs.setdefault(d.group(1), loc) != loc: bad(f'{loc}: description duplicada com {descs[d.group(1)]}')
    if h.count('<h1') != 1: bad(f'{loc}: {h.count("<h1")} h1')
    og = re.search(r'og:image" content="([^"]+)"', h)
    if not og or not os.path.exists(os.path.join(ROOT, og.group(1)[len(D) + 1:])): bad(f'{loc}: og:image ausente no disco')
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            j = json.loads(m)
            types = [n.get('@type') for n in j.get('@graph', [j])]
            print(f'[ ok ] {path or "/":42} ld={types} lastmod={lm}')
        except Exception as ex: bad(f'{loc}: JSON-LD inválido ({ex})')
    if not re.search(r'<script type="application/ld\+json">', h): print(f'[ -- ] {path or "/":42} sem JSON-LD')
for fn in ('llms.txt', 'llms-full.txt'):
    txt = open(os.path.join(ROOT, fn), encoding='utf8').read()
    for u in re.findall(r'\((' + re.escape(D) + r'[^)]*)\)', txt):
        if u not in [l for l, _ in locs] + [D + '/llms-full.txt']: bad(f'{fn}: link interno inexistente {u}')
    if re.search(r'@|\+55|\d{4,5}-\d{4}', txt): bad(f'{fn}: possível e-mail/telefone no texto')
print('RESULTADO: FALHAS=%d' % len(fails)); sys.exit(1 if fails else 0)
