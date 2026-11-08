# SEO & Analytics (Sprint 5)

## SEO
- Por página: `<title>`, description, canonical, Open Graph, Twitter Card (`summary_large_image`), favicon SVG + apple-touch-icon.
- Imagem social: `assets/images/og-image.jpg` (1200×630, gerada de `tools/og-template.html` via Chrome headless).
- JSON-LD `Person` + `WebSite` na home (sem dados inventados: só nome, cargo da bio, foto, descrição e `sameAs` Instagram/LinkedIn).
- `sitemap.xml` e `robots.txt` gerados por `tools/build.py`.
- **Indexação controlada por `"indexable"` em `data/site.json`** (hoje `false` → meta `noindex, nofollow` e `robots.txt` com `Disallow: /`). No lançamento: mudar para `true`, rodar `python3 tools/build.py`. A 404 é sempre `noindex`.

## Analytics
- **GoatCounter (visitas, sem cookies):** `"goatcounter_code": "pauloleite"` em `data/site.json` injeta `<script data-goatcounter="https://pauloleite.goatcounter.com/count" async src="https://gc.zgo.at/count.js">` em todas as páginas (inclusive 404). Não usa cookies nem guarda IP, então carrega **sem** aviso de consentimento e é independente do GTM. Painel: https://pauloleite.goatcounter.com. Para desativar, remova a chave e rode `python3 tools/build.py`. Nota: o GoatCounter ignora `localhost` por padrão; teste só em produção.
- `js/analytics.js` escuta cliques em elementos com `data-event` e empilha em `window.dataLayer` (sem rede, sem cookies). Parâmetros = `data-*` em snake_case + `page_path`. O e-mail nunca é enviado.
- **Google Tag Manager com consentimento (LGPD):** `"gtm_id": "GTM-K9ZTN386"` em `data/site.json`. O contêiner **só é carregado depois que o visitante aceita** o aviso de cookies (`js/consent.js`). Sem aceite, nenhum script do Google é carregado e `data-event` não registra nada. A escolha fica em `localStorage` (`pl_consent`); o botão "Cookies" no rodapé reabre o aviso, e recusar apaga os cookies `_ga*`.
- **Consent Mode:** o padrão é `denied` (analytics, ads, user data, personalization); ao aceitar, só `analytics_storage` vira `granted`.
- **O que configurar no GTM (painel do Google):** a tag do **GA4** dentro do contêiner (ID de medição `G-…`), disparando em "All Pages" ou no evento `gtm.js`. O snippet `<noscript>` do GTM **não** foi incluído de propósito: sem JavaScript não há como pedir consentimento.
- **Eventos (formato plano):** `dataLayer.push({ event: '<nome>', page_path, section_id, ...parâmetros })`. Só são registrados com consentimento. O e-mail nunca é enviado.
- **Importar no GTM (recomendado):** `docs/gtm-container-eventos.json` (gerado por `python3 tools/gtm_container.py`). No GTM: Admin > Importar contêiner > escolher o arquivo > contêiner existente > **Mesclar** (renomear conflitos). Cria 20 variáveis `DLV - …`, o acionador `CE - Eventos do site` e a tag `GA4 - Eventos do site`. Confira o ID de medição na tag (`G-JF46WCSXS2`), use **Visualizar** (Preview), e só então publique.
- **Se preferir manual:** acionador "Evento personalizado" com regex `^(<eventos separados por |>)$`, tag "Evento do Google Analytics: GA4" com nome do evento `{{Event}}` e cada parâmetro mapeado a uma variável de camada de dados com o mesmo nome.

### GoatCounter: os mesmos eventos, sem consentimento
`js/analytics.js` envia cada evento da tabela abaixo também ao GoatCounter (`goatcounter.count({event:true})`), **sempre**, pois ele não usa cookies nem IP. O GTM/GA4 continua só com consentimento.
- **Caminho do evento:** `ev/<evento>/<detalhes>`, ex.: `ev/book_click/system-design/amazon`, `ev/mentoring_click/hero`, `ev/social_click/linkedin/footer`, `ev/section_view/home/trilha`, `ev/scroll_depth/home/50`.
- **Página de origem:** vai como *referrer* do evento. No painel, clique no evento > Referrers para ver de qual página veio o clique.
- **Título:** `evento · texto do link · página › seção`.
- **Conversão (CTR):** cliques do evento ÷ visualizações da página (aba Pages, no mesmo período). Eventos de conversão: `ev/book_click/*`, `ev/product_click/*`, `ev/mentoring_click/*`, `ev/contact_click/*`, `ev/project_click/*`, `ev/social_click/*`. Use o filtro de caminho (`ev/book_click`) para somar.
- Não enviamos URLs completas de saída nem e-mail/telefone: só o domínio de destino em `outbound_click`.
- Eventos de rolagem/seção vistos antes do aceite dos cookies vão só ao GoatCounter (não são reenviados ao GTM).

### Eventos
| Evento | Quando dispara | Parâmetros principais |
|---|---|---|
| `nav_click` | menu, logo, rodapé, breadcrumb, 404 | placement (`header`, `brand`, `footer`, `breadcrumb`, `404`), link_text, link_url |
| `menu_toggle` | botão do menu no celular | state (`open`/`close`) |
| `hero_cta_click` | "Comece por aqui" | cta_id |
| `section_nav_click` | botões Livros/SmartBooks/Recomendações | target |
| `filter_select` | filtro por etapa em Conhecimento | filter (`todos`, `comecando`, `crescendo`, `liderando`) |
| `product_click` | cards de livro/SmartBook e trilhas (abrem a página do produto) | book_id, store, placement |
| `book_click` | botão de compra e links de recomendações | book_id, store, placement, category |
| `mentoring_click` | qualquer botão do ADPList | placement |
| `project_click` / `featured_click` | DogNAS (Google Play, site, destaque na home) | project_id, placement |
| `social_click` | Instagram, LinkedIn | network, placement |
| `contact_click` | WhatsApp, e-mail | method |
| `newsletter_submit` | envio do formulário (quando ativo) | — |
| `reco_expand` | "Ver mais" das recomendações | category |
| `faq_toggle` | abrir pergunta da FAQ (mentoria) | question |
| `carousel_scroll` | primeira rolagem lateral dos depoimentos | section_id |
| `scroll_depth` | 25, 50, 75 e 100% da página | depth |
| `section_view` | seção cruza o centro da tela (1 vez por página) | section_id |
| `outbound_click` | qualquer link externo sem evento próprio | link_domain, link_url |
| `page_not_found` | página 404 | missing_path |

Todos os eventos de clique levam também `link_text`, `link_url`, `link_domain` e `section_id` (nome legível da seção). Nomes e parâmetros seguem os limites do GA4 (nome ≤ 40, valor ≤ 100 caracteres).

### No GA4 (Admin)
1. **Dimensões personalizadas** (escopo Evento), para os parâmetros aparecerem nos relatórios: `placement`, `section_id`, `book_id`, `store`, `filter`, `network`, `method`, `project_id`, `link_text`, `link_domain`, `depth`, `target`, `question`, `category`, `cta_id`, `state`.
2. **Eventos-chave** (conversões): `book_click`, `mentoring_click`, `contact_click`, `newsletter_submit`, `project_click`.
3. **Medição aprimorada:** desligue "Cliques de saída" e "Rolagens" no fluxo de dados, pois `outbound_click` e `scroll_depth` já cobrem isso (evita contagem dupla).
4. **Funil sugerido** (Explorar > Exploração de funil): `section_view` (trilha) → `product_click` → `book_click`; e `section_view` (mentoria) → `mentoring_click`.

## UTMs (tráfego do Instagram)
Link da bio (cada link com UTMs próprios):
`https://pauloleite.dev/?utm_source=instagram&utm_medium=bio&utm_campaign=link_in_bio`
Stories/posts: trocar `utm_medium` (`story`, `post`) e `utm_campaign`. O GA4 lê os UTMs sozinho; "sessões, cliques, conversões e origens" aparecem em Aquisição/Eventos. Marque `book_click`, `mentoring_click` e `contact_click` como **eventos-chave** (conversões) no GA4.

## Testado
Eventos disparados em Chrome headless (book_click e contact_click empilhados; clique sem `data-event` ignorado; e-mail ausente nos parâmetros). JSON-LD válido como JSON. **Não testado:** envio real ao GA4 (sem ID), validadores externos (Rich Results, preview do Facebook/LinkedIn) — exigem o site publicado.
