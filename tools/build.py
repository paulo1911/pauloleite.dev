#!/usr/bin/env python3
"""Gera as páginas estáticas a partir de data/*.json (somente stdlib).
Uso: python3 tools/build.py   (rodar na raiz do repositório)
Itens com "status": "draft" não são renderizados."""
import json, os
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n): return json.load(open(os.path.join(ROOT, 'data', n + '.json'), encoding='utf8'))
def pub(items): return [i for i in items if i.get('status', 'published') == 'published']

SITE = load('site')
BOOKS, SMART = pub(load('books')), pub(load('smartbooks'))
PROJECTS, SOCIALS = pub(load('projects')), pub(load('socials'))
RECO = pub(load('recommendations'))
EXT = '<span class="visually-hidden"> (abre em nova aba)</span>'
NAV = [('Início', '', 'home'), ('Conhecimento', 'conhecimento/', 'conhecimento'), ('Projetos', 'projetos/', 'projetos'), ('Conecte-se', 'conecte-se/', 'conecte-se')]

def ic(p, n): return f'<svg class="icon" aria-hidden="true" focusable="false"><use href="{p}assets/icons/sprite.svg#i-{n}"/></svg>'
def ext_attrs(store=None):
    rel = 'sponsored noopener' if store in ('amazon-aff', 'shopee') else 'noopener'
    return f'target="_blank" rel="{rel}"'
def social(kind): return [s for s in SOCIALS if s['kind'] == kind]
def soc(id_): return next(s for s in SOCIALS if s['id'] == id_)

def img_or_cover(p, item, cls):
    if item.get('image'):
        return f'<img class="{cls}" src="{p}{e(item["image"])}" alt="Capa de {e(item["title"])}" loading="lazy">'
    return f'<div class="{cls}" aria-hidden="true" style="display:grid;place-items:center;color:var(--color-text-muted)">{ic(p, "book-open")}</div>'

def book_card(p, b):
    return f'''<article class="card card--interactive book">
  {img_or_cover(p, b, 'book__cover')}
  <div class="book__body">
    <span class="badge">{e(b['format'])}</span>
    <h3 class="card__title" style="font-size:var(--fs-lg)"><a class="card__link" href="{e(b['url'])}" {ext_attrs()} data-event="book_click" data-book-id="{b['id']}" data-store="{b['store']}">{e(b['title'])}{EXT}</a></h3>
    <p class="card__text">{e(b['subtitle'])}</p>
  </div>
</article>'''

def grid(p, items, cols=2): return f'<div class="grid grid--{cols}">' + ''.join(book_card(p, b) for b in items) + '</div>'

def mentoring(p, placement):
    m = SITE['mentoring']
    return f'''<div class="band">
  <div class="band__text">
    <p class="eyebrow">Mentoring</p>
    <h2 style="font-size:var(--fs-xl)">{e(m['title'])}</h2>
    <p class="text-muted">{e(m['text'])}</p>
  </div>
  <a class="btn btn--primary" href="{e(m['url'])}" {ext_attrs()} data-event="mentoring_click" data-placement="{placement}">{e(m['cta'])} {ic(p, 'arrow-up-right')}{EXT}</a>
</div>'''

def project_card(p, pr, event):
    return f'''<article class="card card--featured">
  <span class="badge">{ic(p, 'sparkles')} Projeto</span>
  <h3 class="card__title">{e(pr['title'])}</h3>
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

def head(eyebrow, h1, lead):
    return f'<section class="page-head"><div class="container"><p class="eyebrow">{e(eyebrow)}</p><h1>{h1}</h1><p>{e(lead)}</p></div></section>'

def layout(key, depth, title, desc, body, path):
    p = '../' * depth if isinstance(depth, int) else depth  # str = prefixo absoluto (404)
    nav = ''.join(f'<li><a href="{p}{h}"{" aria-current=&quot;page&quot;" if k == key else ""}>{t}</a></li>'.replace('&quot;', '"') for t, h, k in NAV)
    ig, li_ = soc('instagram'), soc('linkedin')
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['domain']}/{path}">
<!-- noindex: remover somente na Sprint 7 (lançamento aprovado) -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b0d14">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@700;800&display=swap">
<link rel="stylesheet" href="{p}css/tokens.css">
<link rel="stylesheet" href="{p}css/base.css">
<link rel="stylesheet" href="{p}css/components.css">
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
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu" data-base="{p}assets/icons/sprite.svg"><svg class="icon" aria-hidden="true" focusable="false"><use href="{p}assets/icons/sprite.svg#i-menu"/></svg></button>
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
<script src="{p}js/main.js" defer></script>
</body>
</html>
'''

def build():
    ig, li_ = soc('instagram'), soc('linkedin')
    ph = SITE['photo']
    featured = [b for b in BOOKS if b.get('featured')]
    proj = next(x for x in PROJECTS if x.get('featured'))
    pages = {}
    home = f'''<section class="hero">
  <div class="container hero__inner">
    <div class="hero__photo"><img src="{ph['src']}" width="{ph['width']}" height="{ph['height']}" alt="{e(ph['alt'])}" fetchpriority="high"></div>
    <div>
      <p class="eyebrow">{e(SITE['eyebrow'])}</p>
      <h1>Building technology. <span class="gradient-text">Developing people.</span></h1>
      <p class="hero__lead">{e(SITE['bio'])}</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="conhecimento/" data-event="hero_cta_click" data-cta-id="explorar-conhecimento">Explorar conhecimento {ic('', 'arrow-right')}</a>
        <a class="btn btn--secondary" href="{ig['url']}" {ext_attrs()} data-event="social_click" data-network="instagram">{ic('', 'instagram')} Instagram{EXT}</a>
        <a class="btn btn--secondary" href="{li_['url']}" {ext_attrs()} data-event="social_click" data-network="linkedin">{ic('', 'linkedin')} LinkedIn{EXT}</a>
      </div>
    </div>
  </div>
</section>
<section class="section container" aria-labelledby="livros-h">
  <div class="section-head"><p class="eyebrow">Livros</p><h2 id="livros-h">Escritos para quem constrói carreira em tecnologia</h2></div>
  {grid('', featured)}
  <p style="margin-top:var(--space-5)"><a class="btn btn--ghost" href="conhecimento/" data-event="featured_click" data-item-id="conhecimento">Ver todo o conhecimento {ic('', 'arrow-right')}</a></p>
</section>
<section class="section container" aria-label="Mentoring">{mentoring('', 'home')}</section>
<section class="section container" aria-labelledby="proj-h">
  <div class="section-head"><p class="eyebrow">Projetos</p><h2 id="proj-h">Things I've built</h2></div>
  {project_card('', proj, 'featured_click')}
</section>
<section class="section container" aria-labelledby="contato-h">
  <div class="section-head"><h2 id="contato-h">Vamos conversar</h2></div>
  <div class="grid grid--2">{''.join(link_card('', s) for s in social('contact'))}</div>
</section>'''
    pages['index.html'] = layout('home', 0, 'Paulo Leite — Engineering, Architecture, Leadership',
        'Paulo Leite: engenheiro de software com 20+ anos de experiência. Livros, mentoria e projetos sobre código, liderança e inovação.', home, '')

    know = head('Conhecimento', 'Conhecimento', 'Livros, materiais e recomendações para evoluir em engenharia de software.') + f'''
<div class="container"><nav class="anchor-nav" aria-label="Seções"><a class="btn btn--secondary" href="#livros">Livros</a><a class="btn btn--secondary" href="#smartbooks">SmartBooks</a><a class="btn btn--secondary" href="#recomendacoes">Recomendações</a></nav></div>
<section class="section container" id="livros" aria-labelledby="l-h"><div class="section-head"><h2 id="l-h">Livros</h2><p>Publicados por Paulo Leite.</p></div>{grid('../', BOOKS)}</section>
<section class="section container" id="smartbooks" aria-labelledby="s-h"><div class="section-head"><h2 id="s-h">SmartBooks</h2><p>Guias práticos para destravar a carreira em tecnologia.</p></div>{grid('../', SMART, 3)}</section>
<section class="section container" id="recomendacoes" aria-labelledby="r-h"><div class="section-head"><h2 id="r-h">Recomendações</h2><p>Leituras e materiais que indico.</p></div>
<div class="grid grid--3">{''.join(reco_card(c) for c in RECO)}</div>
<p class="note" style="margin-top:var(--space-5)">{e(SITE['affiliate_note'])}</p></section>'''
    pages['conhecimento/index.html'] = layout('conhecimento', 1, 'Conhecimento — Paulo Leite',
        'Livros, SmartBooks e recomendações de Paulo Leite sobre engenharia de software, arquitetura, carreira e liderança.', know, 'conhecimento/')

    pj = head('Projetos', "Things I've built.", 'Ideas transformed into technology.') + f'''
<section class="section container" aria-label="Projetos"><div class="grid">{''.join(project_card('../', x, 'project_click') for x in PROJECTS)}</div><p class="placeholder" style="margin-top:var(--space-5)">Mais projetos em breve.</p></section>'''
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

    nf = head('Erro 404', 'Página não encontrada', 'O endereço que você acessou não existe ou foi movido.') + '''
<section class="section container"><a class="btn btn--primary" href="/">Voltar ao início</a></section>'''
    pages['404.html'] = layout(None, '/', 'Página não encontrada — Paulo Leite', 'Página não encontrada.', nf, '404.html')

    for f, h in pages.items():
        path = os.path.join(ROOT, f); os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf8').write(h)
    print('Geradas:', ', '.join(pages))

if __name__ == '__main__':
    build()
