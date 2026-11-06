# SEO & Analytics (Sprint 5)

## SEO
- Por página: `<title>`, description, canonical, Open Graph, Twitter Card (`summary_large_image`), favicon SVG + apple-touch-icon.
- Imagem social: `assets/images/og-image.jpg` (1200×630, gerada de `tools/og-template.html` via Chrome headless).
- JSON-LD `Person` + `WebSite` na home (sem dados inventados: só nome, cargo da bio, foto, descrição e `sameAs` Instagram/LinkedIn).
- `sitemap.xml` e `robots.txt` gerados por `tools/build.py`.
- **Indexação controlada por `"indexable"` em `data/site.json`** (hoje `false` → meta `noindex, nofollow` e `robots.txt` com `Disallow: /`). No lançamento: mudar para `true`, rodar `python3 tools/build.py`. A 404 é sempre `noindex`.

## Analytics
- `js/analytics.js` escuta cliques em elementos com `data-event` e empilha em `window.dataLayer` (sem rede, sem cookies). Parâmetros = `data-*` em snake_case + `page_path`. O e-mail nunca é enviado.
- **Google Tag Manager com consentimento (LGPD):** `"gtm_id": "GTM-PWQFMS3W"` em `data/site.json`. O contêiner **só é carregado depois que o visitante aceita** o aviso de cookies (`js/consent.js`). Sem aceite, nenhum script do Google é carregado e `data-event` não registra nada. A escolha fica em `localStorage` (`pl_consent`); o botão "Cookies" no rodapé reabre o aviso, e recusar apaga os cookies `_ga*`.
- **Consent Mode:** o padrão é `denied` (analytics, ads, user data, personalization); ao aceitar, só `analytics_storage` vira `granted`.
- **O que configurar no GTM (painel do Google):** a tag do **GA4** dentro do contêiner (ID de medição `G-…`), disparando em "All Pages" ou no evento `gtm.js`. O snippet `<noscript>` do GTM **não** foi incluído de propósito: sem JavaScript não há como pedir consentimento.
- **Eventos:** cada clique com `data-event` faz `dataLayer.push({event: '<nome>', params: {...}})`. No GTM, crie um acionador "Evento personalizado" por nome (tabela abaixo) e variáveis de camada de dados `params.book_id`, `params.store`, `params.placement`, etc.
- `ga4_id` (gtag direto) continua suportado, mas sem aviso de cookies; prefira o GTM.

| Evento | Onde | Parâmetros |
|---|---|---|
| hero_cta_click | CTA do hero | cta_id |
| book_click | botão de compra nas páginas de produto, recomendações | book_id, store, category?, placement |
| product_click | cards de livros/SmartBooks (abrem a página do produto) | book_id, store, placement? |
| newsletter_submit | formulário (quando ativo) | — |
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
