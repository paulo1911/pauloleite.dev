#!/usr/bin/env python3
"""Gera imagens Open Graph (1200x630) por livro/SmartBook em assets/images/og/<id>.jpg.
Requer: Chrome (headless) e Pillow. Uso: python3 tools/make_og.py (rodar na raiz do repositório)."""
import json, os, subprocess, tempfile
from html import escape as e
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
def load(n): return json.load(open(os.path.join(ROOT, 'data', n + '.json'), encoding='utf8'))
items = [i for i in load('books') + load('smartbooks') if i.get('status', 'published') == 'published']

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Manrope;font-weight:700 800;src:url('file://%(root)s/assets/fonts/manrope-var.woff2') format('woff2')}
@font-face{font-family:Inter;font-weight:400 600;src:url('file://%(root)s/assets/fonts/inter-var.woff2') format('woff2')}
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:radial-gradient(60%% 70%% at 15%% 0%%,rgba(139,92,246,.30) 0%%,transparent 70%%),#0b0d14;font-family:Inter,sans-serif;color:#f8fafc;position:relative}
.eyebrow{position:absolute;left:80px;top:78px;font-weight:600;font-size:22px;letter-spacing:.14em;color:#c4b5fd;text-transform:uppercase}
h1{position:absolute;left:80px;top:128px;width:600px;font-family:Manrope;font-weight:800;font-size:%(fs)spx;line-height:1.08;letter-spacing:-.025em}
.sub{position:absolute;left:80px;bottom:128px;width:600px;font-size:27px;line-height:1.35;color:#c4b5fd;font-weight:500}
.by{position:absolute;left:80px;bottom:60px;font-size:26px;color:#9298aa}
.cv{position:absolute;left:740px;top:95px;width:400px;height:440px;border-radius:26px;background:#151827;border:1px solid #3b3566;display:grid;place-items:center;padding:20px;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.cv img{max-width:360px;max-height:400px;width:auto;height:auto;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.55)}
</style></head><body>
<div class="eyebrow">%(kind)s</div><h1>%(title)s</h1><div class="sub">%(sub)s</div>
<div class="by">Paulo Leite · pauloleite.dev</div>
<div class="cv"><img src="file://%(root)s/%(cover)s"></div></body></html>"""

for it in items:
    t = it['title']
    fs = 72 if len(t) <= 16 else 58 if len(t) <= 30 else 50
    html = TPL % dict(root=ROOT, fs=fs, kind=e(it['format']), title=e(t), sub=e(it['subtitle']), cover=it['image']['src'])
    with tempfile.TemporaryDirectory() as d:
        h, png = os.path.join(d, 'og.html'), os.path.join(d, 'og.png')
        open(h, 'w', encoding='utf8').write(html)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1200,630', f'--screenshot={png}', 'file://' + h], check=True, capture_output=True)
        out = os.path.join(ROOT, 'assets', 'images', 'og', it['id'] + '.jpg')
        Image.open(png).convert('RGB').save(out, quality=86, optimize=True, progressive=True)
        print('OG:', out, os.path.getsize(out) // 1024, 'KB')
