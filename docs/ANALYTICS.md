# SEO & Analytics (Sprint 5)

## SEO
- Por página: `<title>`, description, canonical, Open Graph, Twitter Card (`summary_large_image`), favicon SVG + apple-touch-icon.
- Imagem social: `assets/images/og-image.jpg` (1200×630, gerada de `tools/og-template.html` via Chrome headless).
- JSON-LD `Person` + `WebSite` na home (sem dados inventados: só nome, cargo da bio, foto, descrição e `sameAs` Instagram/LinkedIn).
- `sitemap.xml` e `robots.txt` gerados por `tools/build.py`.
- **Indexação controlada por `"indexable"` em `data/site.json`** (hoje `false` → meta `noindex, nofollow` e `robots.txt` com `Disallow: /`). No lançamento: mudar para `true`, rodar `python3 tools/build.py`. A 404 é sempre `noindex`.

## Analytics
- `js/analytics.js` escuta cliques em elementos com `data-event` e empilha em `window.dataLayer` (sem rede, sem cookies). Parâmetros = `data-*` em snake_case + `page_path`. O e-mail nunca é enviado.
- **GA4 desativado** (`"ga4_id": null`). Para ativar: colocar o ID `G-XXXXXXXXXX` em `data/site.json`, rodar o build. **Antes disso, adicionar aviso de cookies (LGPD)** — não implementado nesta versão.

| Evento | Onde | Parâmetros |
|---|---|---|
| hero_cta_click | CTA do hero | cta_id |
| book_click | livros, SmartBooks, recomendações | book_id, store, category? |
| mentoring_click | CTA ADPList | placement |
| project_click | DogNAS em Projetos | project_id |
| featured_click | destaques da home | project_id / item_id |
| social_click | Instagram, LinkedIn | network |
| contact_click | WhatsApp, e-mail | method |

## UTMs (tráfego do Instagram)
Link da bio (cada link com UTMs próprios):
`https://pauloleite.dev/?utm_source=instagram&utm_medium=bio&utm_campaign=link_in_bio`
Stories/posts: trocar `utm_medium` (`story`, `post`) e `utm_campaign`. O GA4 lê os UTMs sozinho; "sessões, cliques, conversões e origens" aparecem em Aquisição/Eventos. Marque `book_click`, `mentoring_click` e `contact_click` como **eventos-chave** (conversões) no GA4.

## Testado
Eventos disparados em Chrome headless (book_click e contact_click empilhados; clique sem `data-event` ignorado; e-mail ausente nos parâmetros). JSON-LD válido como JSON. **Não testado:** envio real ao GA4 (sem ID), validadores externos (Rich Results, preview do Facebook/LinkedIn) — exigem o site publicado.
