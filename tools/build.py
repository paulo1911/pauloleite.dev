#!/usr/bin/env python3
"""Gera as páginas estáticas a partir de data/*.json (somente stdlib).
Uso: python3 tools/build.py   (rodar na raiz do repositório)
Itens com "status": "draft" não são renderizados."""
import json, os, datetime
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n): return json.load(open(os.path.join(ROOT, 'data', n + '.json'), encoding='utf8'))
def pub(items): return [i for i in items if i.get('status', 'published') == 'published']

SITE = load('site')
BOOKS, SMART = pub(load('books')), pub(load('smartbooks'))
PROJECTS, SOCIALS = pub(load('projects')), pub(load('socials'))
RECO = pub(load('recommendations'))
PATHS, CREDS, TESTI = load('paths'), pub(load('credentials')), pub(load('testimonials'))
ENDORSE = pub(load('endorsements'))
PHOTO = SITE['photo']
SIZES = '(min-width: 64em) 384px, 240px'
def srcset(ext): return ', '.join(f"{{p}}{PHOTO['base']}-{w}.{ext} {w}w" for w in PHOTO['widths'])
PRELOAD_HERO = f'<link rel="preload" as="image" type="image/webp" fetchpriority="high" imagesrcset="{srcset("webp").replace("{p}", "")}" imagesizes="{SIZES}">'

def minify_css(t):
    import re
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r' ?([{};,]) ?', r'\1', t)
    return t.replace(';}', '}').strip()

def minify_js(t):
    import re
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    return '\n'.join(l.strip() for l in t.split('\n') if l.strip() and not l.strip().startswith('//'))

def bundle_assets():
    css = ''.join(open(os.path.join(ROOT, 'css', f), encoding='utf8').read() + '\n' for f in ('fonts.css', 'tokens.css', 'base.css', 'components.css'))
    open(os.path.join(ROOT, 'css', 'site.min.css'), 'w', encoding='utf8').write(minify_css(css) + '\n')
    js = '\n'.join(open(os.path.join(ROOT, 'js', f), encoding='utf8').read() for f in ('analytics.js', 'main.js'))
    open(os.path.join(ROOT, 'js', 'site.min.js'), 'w', encoding='utf8').write(minify_js(js) + '\n')

SPRITE = open(os.path.join(ROOT, 'assets', 'icons', 'sprite.svg'), encoding='utf8').read()
def inline_sprite(html):
    import re
    used = set(re.findall(r'sprite\.svg#(i-[a-z0-9-]+)', html)) | {'i-menu', 'i-x'}
    html = re.sub(r'href="[^"]*sprite\.svg#', 'href="#', html)
    syms = ''.join(m.group(0) for m in re.finditer(r'<symbol id="(i-[a-z0-9-]+)".*?</symbol>', SPRITE, re.S) if m.group(1) in used)
    return html.replace('</body>', f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">{syms}</svg>\n</body>')

EXT = '<span class="visually-hidden"> (abre em nova aba)</span>'
NAV = [('Início', '', 'home'), ('Conhecimento', 'conhecimento/', 'conhecimento'), ('Mentoria', 'mentoria/', 'mentoria'), ('Projetos', 'projetos/', 'projetos'), ('Conecte-se', 'conecte-se/', 'conecte-se')]

def ic(p, n): return f'<svg class="icon" aria-hidden="true" focusable="false"><use href="{p}assets/icons/sprite.svg#i-{n}"/></svg>'
def ext_attrs(store=None):
    rel = 'sponsored noopener' if store in ('amazon-aff', 'shopee') else 'noopener'
    return f'target="_blank" rel="{rel}"'
def social(kind): return [s for s in SOCIALS if s['kind'] == kind]
def soc(id_): return next(s for s in SOCIALS if s['id'] == id_)

def product_url(p, id_): return f'{p}conhecimento/{id_}/'

def img_or_cover(p, item, cls):
    im = item.get('image')
    if im:
        return f'<img class="{cls}" src="{p}{e(im["src"])}" width="{im["width"]}" height="{im["height"]}" alt="Capa de {e(item["title"])}" loading="lazy" decoding="async" fetchpriority="low">'
    return f'<div class="{cls}" aria-hidden="true" style="display:grid;place-items:center;color:var(--color-text-muted)">{ic(p, "book-open")}</div>'

def book_card(p, b):
    return f'''<article class="card card--interactive book">
  {img_or_cover(p, b, 'book__cover')}
  <div class="book__body">
    <span class="badge">{e(b['format'])}</span>
    <h3 class="card__title" style="font-size:var(--fs-lg)"><a class="card__link" href="{product_url(p, b['id'])}" data-event="product_click" data-book-id="{b['id']}" data-store="{b['store']}">{e(b['title'])}</a></h3>
    <p class="card__text">{e(b['subtitle'])}</p>
  </div>
</article>'''

def smart_card(p, b):
    return f'''<article class="card card--interactive">
  <div class="card__media card__media--contain">{img_or_cover(p, b, '')}</div>
  <span class="badge">{e(b['format'])}</span>
  <h3 class="card__title" style="font-size:var(--fs-lg)"><a class="card__link" href="{product_url(p, b['id'])}" data-event="product_click" data-book-id="{b['id']}" data-store="{b['store']}">{e(b['title'])}</a></h3>
  <p class="card__text">{e(b['subtitle'])}</p>
</article>'''

def smart_grid(p, items): return '<div class="grid grid--3 grid--start">' + ''.join(smart_card(p, b) for b in items) + '</div>'

def grid(p, items, cols=2): return f'<div class="grid grid--{cols}">' + ''.join(book_card(p, b) for b in items) + '</div>'

def mentoring(p, placement):
    m = SITE['mentoring']
    return f'''<div class="band">
  <div class="band__text">
    <p class="eyebrow">Mentoria</p>
    <h2 style="font-size:var(--fs-xl)">{e(m['title'])}</h2>
    <p class="text-muted">{e(m['text'])}</p>
  </div>
  <a class="btn btn--primary" href="{e(m['url'])}" {ext_attrs()} data-event="mentoring_click" data-placement="{placement}">{e(m['cta'])} {ic(p, 'arrow-up-right')}{EXT}</a>
</div>'''

def project_card(p, pr, event, lv=3):
    return f'''<article class="card card--featured">
  <span class="badge">{ic(p, 'sparkles')} Projeto</span>
  <h{lv} class="card__title"{' style="font-size:var(--fs-xl)"' if lv == 2 else ''}>{e(pr['title'])}</h{lv}>
  <p class="card__text">{e(pr['description'])}</p>
  <p><a class="btn btn--primary" href="{e(pr['url'])}" {ext_attrs()} data-event="{event}" data-project-id="{pr['id']}">{e(pr['cta'])} {ic(p, 'arrow-up-right')}{EXT}</a></p>
</article>'''

def link_card(p, s):
    if s.get('email'):
        u, d = s['email']['user'], s['email']['domain']
        a = f'<a class="card__link" href="#contato" data-email-user="{u}" data-email-domain="{d}" data-event="contact_click" data-method="email">{e(s["label"])}</a>'
        meta = f'<span data-email-text>{e(s["meta"])}</span>'
    else:
        ev = 'contact_click" data-method="' + s['id'] if s['kind'] == 'contact' else 'social_click" data-network="' + s['id']
        a = f'<a class="card__link" href="{e(s["url"])}" {ext_attrs()} data-event="{ev}">{e(s["label"])}{EXT}</a>'
        meta = e(s['meta'])
    arrow = '' if s.get('email') else ic(p, 'arrow-up-right')
    return f'''<article class="card card--interactive social">
  <span class="social__icon">{ic(p, s['icon'])}</span>
  <div class="social__body"><h3 class="social__label" style="font-size:var(--fs-base)">{a}</h3><p class="social__meta">{meta}</p></div>
  {arrow}
</article>'''

def reco_card(c, per=6):
    def li(i):
        sub = f'<span class="reco__sub"> — {e(i["subtitle"])}</span>' if i.get('subtitle') else ''
        aff = 'sponsored noopener'
        return f'<li><a href="{e(i["url"])}" target="_blank" rel="{aff}" data-event="book_click" data-book-id="{i["id"]}" data-category="{c["id"]}" data-store="{i["store"]}">{e(i["title"])}{EXT}</a></li>'
    first, rest = c['items'][:per], c['items'][per:]
    more = ''
    if rest:
        more = f'<details class="reco__more"><summary>Ver mais ({len(rest)})</summary><ul class="reco">{"".join(li(i) for i in rest)}</ul></details>'
    return f'<article class="card"><h3 class="card__title">{e(c["title"])}</h3><ul class="reco">{"".join(li(i) for i in first)}</ul>{more}</article>'

def path_card(p, pa):
    byid = {x['id']: x for x in BOOKS + SMART}
    items = ''.join(f'<li><a href="{product_url(p, i)}" data-event="product_click" data-book-id="{i}" data-store="{byid[i]["store"]}" data-placement="trilha">{e(byid[i]["title"])}</a><span class="path__fmt">{e(byid[i]["format"])}</span></li>' for i in pa['items'] if i in byid)
    m = SITE['mentoring']
    ig = soc('instagram')
    lk = {'mentoring': f'<li><a href="{p}mentoria/" data-event="mentoring_click" data-placement="trilha">Mentoria 1:1 gratuita</a></li>',
          'instagram': f'<li><a href="{e(ig["url"])}" {ext_attrs()} data-event="social_click" data-network="instagram" data-placement="trilha">Conteúdo no Instagram {e(ig["meta"])}{EXT}</a></li>'}
    items += ''.join(lk[k] for k in pa['links'])
    return f'''<article class="card path">
  <p class="eyebrow">{e(pa['eyebrow'])}</p>
  <h3 class="card__title">{e(pa['title'])}</h3>
  <p class="card__text">{e(pa['text'])}</p>
  <ul class="path__list">{items}</ul>
</article>'''

def credentials():
    t = [c['text'].format(n_books=len(BOOKS), n_smart=len(SMART)) for c in CREDS]
    return '<ul class="creds" aria-label="Credenciais">' + ''.join(f'<li>{e(x)}</li>' for x in t) + '</ul>'

def quotes_section(items, hid, eyebrow, h2, src_html):
    if not items: return ''
    cards = ''.join(f'<figure class="card quote"><blockquote><p>“{e(t["quote"])}”</p></blockquote><figcaption><strong>{e(t["name"])}</strong> - {e(t["role"])}</figcaption></figure>' for t in items)
    return f'''<section class="section container" aria-labelledby="{hid}">
  <div class="section-head"><p class="eyebrow">{e(eyebrow)}</p><h2 id="{hid}">{e(h2)}</h2></div>
  <div class="grid quotes" role="group" aria-label="{e(h2)}" tabindex="0">{cards}</div>
  <p class="note section-cta" style="margin-top:var(--space-4)">{src_html}</p>
</section>'''

def testimonials(p):
    return quotes_section(TESTI, 'dep-h', 'Mentorados', 'O que dizem quem já fez mentoria',
        f'Avaliações públicas no <a href="{e(SITE["mentoring"]["url"])}" {ext_attrs()}>perfil do ADPList{EXT}</a>.')

def endorsements():
    return quotes_section(ENDORSE, 'rec-h', 'Liderança', 'Quem já trabalhou comigo',
        f'Recomendações públicas no <a href="{e(soc("linkedin")["url"])}" {ext_attrs()}>LinkedIn{EXT}</a>.')

def about():
    return '<section class="section container" aria-labelledby="sobre-h"><div class="section-head"><p class="eyebrow">Sobre</p><h2 id="sobre-h">Quem está do outro lado</h2></div><div class="about">' + ''.join(f'<p>{e(x)}</p>' for x in SITE['about']) + '</div></section>'

STORE_CTA = {'amazon': 'Comprar na Amazon', 'hotmart': 'Adquirir na Hotmart'}

def product_page(it):
    pa = next((x for x in PATHS if it['id'] in x['items']), None)
    byid = {x['id']: x for x in BOOKS + SMART}
    im = it.get('image')
    cover = f'<img class="prod__cover" src="../../{e(im["src"])}" width="{im["width"]}" height="{im["height"]}" alt="Capa de {e(it["title"])}" decoding="async" fetchpriority="high">' if im else ''
    cta = STORE_CTA.get(it['store'], 'Comprar')
    desc = f'<p class="prod__desc">{e(it["description"])}</p>' if it.get('description') else ''
    learn = ''
    if it.get('learn'):
        learn = '<section class="section container" aria-labelledby="learn-h"><div class="section-head"><h2 id="learn-h">O que você vai encontrar</h2></div><ul class="checks">' + ''.join(f'<li>{e(x)}</li>' for x in it['learn']) + '</ul></section>'
    fit = ''
    more = ''
    if pa:
        fit = f'''<section class="section container" aria-labelledby="fit-h">
  <div class="section-head"><p class="eyebrow">Para quem é</p><h2 id="fit-h">{e(pa['eyebrow'])}: {e(pa['title'])}</h2><p>{e(pa['text'])}</p></div>
</section>'''
        others = [byid[i] for i in pa['items'] if i != it['id'] and i in byid]
        if others:
            more = '<section class="section container" aria-labelledby="more-h"><div class="section-head"><p class="eyebrow">Na mesma trilha</p><h2 id="more-h">Continue por aqui</h2></div><div class="grid grid--3 grid--start">' + ''.join(smart_card('../../', o) if o['store'] == 'hotmart' else book_card('../../', o) for o in others) + '</div></section>'
    body = f'''<nav class="container crumbs" aria-label="Trilha de navegação"><a href="../">Conhecimento</a><span aria-hidden="true"> / </span><span>{e(it['title'])}</span></nav>
<section class="container prod">
  <div class="prod__media">{cover}</div>
  <div class="prod__body">
    <span class="badge">{e(it['format'])}</span>
    <h1>{e(it['title'])}</h1>
    <p class="prod__sub">{e(it['subtitle'])}</p>
    {desc}
    <p><a class="btn btn--primary" href="{e(it['url'])}" {ext_attrs()} data-event="book_click" data-book-id="{it['id']}" data-store="{it['store']}" data-placement="produto">{cta} {ic('../../', 'arrow-up-right')}{EXT}</a></p>
  </div>
</section>
{learn}
{fit}
{more}
<section class="section container" aria-label="Mentoria">{mentoring('../../', 'produto')}</section>'''
    typ = 'Book' if it['format'] != 'SmartBook' else 'CreativeWork'
    ld = {"@context": "https://schema.org", "@type": typ, "name": it['title'], "alternativeHeadline": it['subtitle'],
          "url": f"{SITE['domain']}/conhecimento/{it['id']}/", "inLanguage": "pt-BR",
          "author": {"@type": "Person", "@id": SITE['domain'] + "/#person", "name": SITE['name']}}
    if im: ld["image"] = f"{SITE['domain']}/{im['src']}"
    jl = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n'
    d = f"{it['title']}: {it['subtitle']}. {it['format']} de Paulo Leite."
    return layout('conhecimento', 2, f"{it['title']} — Paulo Leite", d, body, f"conhecimento/{it['id']}/", jsonld=jl)

TOPICS = ['Carreira e transição', 'Engenharia e back-end', 'Arquitetura de software', 'Cloud computing', 'Liderança e gestão', 'Comunicação e negociação', 'Resolução de problemas', 'Organização e gestão de projetos']
FIT = [('Estou começando', 'Primeiro emprego, entrevistas, o que estudar e como se posicionar.'),
       ('Quero crescer', 'Caminho de pleno a sênior, decisões técnicas, visibilidade e arquitetura.'),
       ('Quero liderar', 'Transição para tech lead ou gestão, liderança de pessoas e comunicação.')]
STEPS = ['Escolha um horário no ADPList. A sessão é gratuita e dura 45 minutos.',
         'Ao agendar, conte seu momento de carreira e o que você quer resolver.',
         'Eu me preparo para a sessão antes. Costumo levar um material-guia, que pode servir para os encontros seguintes.',
         'Na conversa, mapeamos prioridades e saímos com próximos passos claros.']
FAQ = [('A mentoria é paga?', 'Não. As sessões pelo ADPList são gratuitas, sujeitas à disponibilidade de agenda.'),
       ('Quanto tempo dura?', 'Cada sessão tem 45 minutos.'),
       ('O que levar para a sessão?', 'Seu objetivo para os próximos meses, um resumo do seu contexto atual e duas ou três perguntas que você quer ver respondidas.'),
       ('Serve para quem ainda não tem emprego em tecnologia?', 'Sim. A conversa se adapta ao seu momento: da primeira vaga à transição para liderança.')]

def mentoring_page():
    m = SITE['mentoring']
    btn = lambda pl: f'<a class="btn btn--primary" href="{e(m["url"])}" {ext_attrs()} data-event="mentoring_click" data-placement="{pl}">{e(m["cta"])} {ic("../", "arrow-up-right")}{EXT}</a>'
    fit = ''.join(f'<article class="card"><h3 class="card__title">{e(t)}</h3><p class="card__text">{e(x)}</p></article>' for t, x in FIT)
    topics = ''.join(f'<li>{e(t)}</li>' for t in TOPICS)
    steps = ''.join(f'<li>{e(x)}</li>' for x in STEPS)
    faq = ''.join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    body = head('Mentoria', 'Mentoria 1:1 <span class="gradient-text">gratuita</span>', 'Uma conversa de 45 minutos sobre carreira, engenharia e liderança, para você decidir o próximo passo com clareza.') + f'''
<div class="container hero__actions" style="margin-top:calc(var(--space-4) * -1)">{btn('mentoria-topo')}</div>
<section class="section container" aria-labelledby="fit-h"><div class="section-head"><h2 id="fit-h">Para quem é</h2></div><div class="grid grid--3">{fit}</div></section>
<section class="section container" aria-labelledby="top-h"><div class="section-head"><h2 id="top-h">Temas que podemos trabalhar</h2></div><ul class="creds creds--plain">{topics}</ul></section>
<section class="section container" aria-labelledby="how-h"><div class="section-head"><h2 id="how-h">Como funciona</h2></div><ol class="steps">{steps}</ol></section>
{testimonials('../')}
<section class="section container" aria-labelledby="faq-h"><div class="section-head"><h2 id="faq-h">Perguntas frequentes</h2></div><div class="faqs">{faq}</div></section>
<section class="section container" aria-label="Agendar">{mentoring('../', 'mentoria-final')}</section>'''
    return layout('mentoria', 1, 'Mentoria 1:1 gratuita — Paulo Leite',
        'Mentoria gratuita de 45 minutos com Paulo Leite pelo ADPList: carreira, engenharia de software, arquitetura e liderança em tecnologia.', body, 'mentoria/')

def head(eyebrow, h1, lead):
    return f'<section class="page-head"><div class="container"><p class="eyebrow">{e(eyebrow)}</p><h1>{h1}</h1><p>{e(lead)}</p></div></section>'

def layout(key, depth, title, desc, body, path, jsonld='', index=True, head_extra=''):
    p = '../' * depth if isinstance(depth, int) else depth  # str = prefixo absoluto (404)
    nav = ''.join(f'<li><a href="{p}{h}"{" aria-current=&quot;page&quot;" if k == key else ""}>{t}</a></li>'.replace('&quot;', '"') for t, h, k in NAV)
    ig, li_ = soc('instagram'), soc('linkedin')
    url = f"{SITE['domain']}/{path}"
    robots = 'index, follow, max-image-preview:large' if (SITE['indexable'] and index) else 'noindex, nofollow'
    ga = f' data-ga4-id="{SITE["ga4_id"]}"' if SITE.get('ga4_id') else ''
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<!-- robots controlado por "indexable" em data/site.json (Sprint 7 libera) -->
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0b0d14">
<meta name="color-scheme" content="dark">
<meta name="author" content="{e(SITE['name'])}">
<link rel="alternate" hreflang="pt-BR" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<link rel="icon" href="{p}assets/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:locale" content="{SITE['locale']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['domain']}/{SITE['og_image']['src']}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="{SITE['og_image']['width']}">
<meta property="og:image:height" content="{SITE['og_image']['height']}">
<meta property="og:image:alt" content="{e(SITE['og_image']['alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE['domain']}/{SITE['og_image']['src']}">
{jsonld}<link rel="preload" href="{p}assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
{head_extra}<link rel="stylesheet" href="{p}css/site.min.css">
</head>
<body>
<!-- GERADO por tools/build.py a partir de data/*.json — não edite à mão -->
<a class="skip-link" href="#main">Pular para o conteúdo</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="{p or './'}">Paulo Leite<span>.dev</span></a>
    <nav class="nav" id="nav" aria-label="Principal">
      <ul>{nav}</ul>
    </nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu"><svg class="icon" aria-hidden="true" focusable="false"><use href="{p}assets/icons/sprite.svg#i-menu"/></svg></button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container site-footer__inner">
    <span>© 2026 Paulo Leite · {e(SITE['tagline'])}</span>
    <ul class="site-footer__nav" aria-label="Redes">
      <li><a href="{ig['url']}" {ext_attrs()} data-event="social_click" data-network="instagram">Instagram{EXT}</a></li>
      <li><a href="{li_['url']}" {ext_attrs()} data-event="social_click" data-network="linkedin">LinkedIn{EXT}</a></li>
    </ul>
  </div>
</footer>
<script src="{p}js/site.min.js" defer{ga}></script>
</body>
</html>
'''
    return inline_sprite(html)

def home_jsonld():
    graph = [
        {"@type": "Person", "@id": SITE['domain'] + "/#person", "name": SITE['name'], "url": SITE['domain'] + "/",
         "jobTitle": SITE['job_title'], "description": SITE['bio'],
         "image": SITE['domain'] + "/" + PHOTO['base'] + "-960.jpg",
         "sameAs": [soc('instagram')['url'], soc('linkedin')['url']]},
        {"@type": "WebSite", "@id": SITE['domain'] + "/#website", "url": SITE['domain'] + "/", "name": SITE['name'],
         "description": SITE['tagline'], "inLanguage": "pt-BR", "publisher": {"@id": SITE['domain'] + "/#person"}},
    ]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>'

def build():
    bundle_assets()
    ig, li_ = soc('instagram'), soc('linkedin')
    proj = next(x for x in PROJECTS if x.get('featured'))
    pages = {}
    home = f'''<section class="hero">
  <div class="container hero__inner">
    <div class="hero__photo"><picture><source type="image/webp" srcset="{srcset('webp').replace('{p}', '')}" sizes="{SIZES}"><img src="{PHOTO['base']}-768.jpg" srcset="{srcset('jpg').replace('{p}', '')}" sizes="{SIZES}" width="{PHOTO['width']}" height="{PHOTO['height']}" alt="{e(PHOTO['alt'])}" fetchpriority="high" decoding="async"></picture></div>
    <div>
      <p class="eyebrow">{e(SITE['eyebrow'])}</p>
      <h1>Arquitete <span class="gradient-text">sua carreira</span> em tecnologia.</h1>
      <p class="hero__lead">{e(SITE['bio'])}</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="#trilha" data-event="hero_cta_click" data-cta-id="comece-por-aqui">Comece por aqui {ic('', 'arrow-down')}</a>
        <a class="btn btn--secondary" href="{e(SITE['mentoring']['url'])}" {ext_attrs()} data-event="mentoring_click" data-placement="hero">Mentoria gratuita{EXT}</a>
      </div>
    </div>
  </div>
</section>
<section class="container" aria-label="Credenciais">{credentials()}</section>
<section class="section container" id="trilha" aria-labelledby="trilha-h">
  <div class="section-head"><p class="eyebrow">Sua trilha</p><h2 id="trilha-h">Em que momento da carreira você está?</h2><p>Escolha o ponto de partida. Cada trilha reúne o material certo para a sua etapa.</p></div>
  <div class="grid grid--3">{''.join(path_card('', x) for x in PATHS)}</div>
  <p class="section-cta" style="margin-top:var(--space-5)"><a class="btn btn--ghost" href="conhecimento/" data-event="featured_click" data-item-id="conhecimento">Ver todo o conhecimento {ic('', 'arrow-right')}</a></p>
</section>
{about()}
{endorsements()}
{testimonials('')}
<section class="section container" aria-label="Mentoring">{mentoring('', 'home')}</section>
<section class="section container" aria-labelledby="proj-h">
  <div class="section-head"><p class="eyebrow">Projetos</p><h2 id="proj-h">Também construo produtos</h2></div>
  {project_card('', proj, 'featured_click')}
</section>
<section class="section container" aria-labelledby="contato-h">
  <div class="section-head"><h2 id="contato-h">Vamos conversar</h2></div>
  <div class="grid grid--2">{''.join(link_card('', s) for s in social('contact'))}</div>
</section>'''
    pages['index.html'] = layout('home', 0, 'Paulo Leite — Arquitete sua carreira em tecnologia',
        'Paulo Leite, engenheiro com 20+ anos de experiência. Livros, SmartBooks e mentoria gratuita para quem está começando, quer crescer ou liderar em tecnologia.', home, '', jsonld=home_jsonld(), head_extra=PRELOAD_HERO + '\n')

    know = head('Conhecimento', 'Conhecimento', 'Livros, materiais e recomendações para evoluir em engenharia de software.') + f'''
<div class="container"><nav class="anchor-nav" aria-label="Seções"><a class="btn btn--secondary" href="#livros">Livros</a><a class="btn btn--secondary" href="#smartbooks">SmartBooks</a><a class="btn btn--secondary" href="#recomendacoes">Recomendações</a></nav></div>
<section class="section container" id="livros" aria-labelledby="l-h"><div class="section-head"><h2 id="l-h">Livros</h2><p>Publicados por Paulo Leite.</p></div>{grid('../', BOOKS)}</section>
<section class="section container" id="smartbooks" aria-labelledby="s-h"><div class="section-head"><h2 id="s-h">SmartBooks</h2><p>Guias práticos para destravar a carreira em tecnologia.</p></div>{smart_grid('../', SMART)}</section>
<section class="section container" id="recomendacoes" aria-labelledby="r-h"><div class="section-head"><h2 id="r-h">Recomendações</h2><p>Leituras e materiais que indico.</p></div>
<div class="grid grid--3">{''.join(reco_card(c) for c in RECO)}</div>
<p class="note" style="margin-top:var(--space-5)">{e(SITE['affiliate_note'])}</p></section>'''
    pages['conhecimento/index.html'] = layout('conhecimento', 1, 'Conhecimento — Paulo Leite',
        'Livros, SmartBooks e recomendações de Paulo Leite sobre engenharia de software, arquitetura, carreira e liderança.', know, 'conhecimento/')

    pj = head('Projetos', "Things I've built.", 'Ideas transformed into technology.') + f'''
<section class="section container" aria-label="Projetos"><div class="grid">{''.join(project_card('../', x, 'project_click', 2) for x in PROJECTS)}</div><p class="placeholder" style="margin-top:var(--space-5)">Mais projetos em breve.</p></section>'''
    pages['projetos/index.html'] = layout('projetos', 1, 'Projetos — Paulo Leite',
        'Projetos autorais de Paulo Leite. Inicialmente: DogNAS, transforme dispositivos Android em servidores NAS pessoais.', pj, 'projetos/')

    con = head('Conecte-se', 'Conecte-se', 'Vamos conversar sobre tecnologia, carreira e liderança.') + f'''
<section class="section container" aria-label="Mentoring">{mentoring('../', 'conecte-se')}</section>
<section class="section container" aria-labelledby="redes-h"><div class="section-head"><h2 id="redes-h">Redes</h2></div>
<div class="grid grid--2">{''.join(link_card('../', s) for s in social('social'))}</div></section>
<section class="section container" id="contato" aria-labelledby="contato-h"><div class="section-head"><h2 id="contato-h">Contato</h2></div>
<div class="grid grid--2">{''.join(link_card('../', s) for s in social('contact'))}</div></section>'''
    pages['conecte-se/index.html'] = layout('conecte-se', 1, 'Conecte-se — Paulo Leite',
        'Instagram, LinkedIn, e-mail, WhatsApp e mentoria com Paulo Leite.', con, 'conecte-se/')

    pages['mentoria/index.html'] = mentoring_page()
    for it in BOOKS + SMART:
        pages[f"conhecimento/{it['id']}/index.html"] = product_page(it)

    nf = head('Erro 404', 'Página não encontrada', 'O endereço que você acessou não existe ou foi movido.') + '''
<section class="section container"><a class="btn btn--primary" href="/">Voltar ao início</a></section>'''
    pages['404.html'] = layout(None, '/', 'Página não encontrada — Paulo Leite', 'Página não encontrada.', nf, '404.html', index=False)

    for f, h in pages.items():
        path = os.path.join(ROOT, f); os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf8').write(h)
    today = datetime.date.today().isoformat()
    urls = ''.join(f"  <url><loc>{SITE['domain']}/{f.replace('index.html', '')}</loc><lastmod>{today}</lastmod></url>\n" for f in pages if f != '404.html')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    rules = 'Allow: /' if SITE['indexable'] else 'Disallow: /'
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf8').write(f"User-agent: *\n{rules}\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    print('Geradas:', ', '.join(pages))

if __name__ == '__main__':
    build()
