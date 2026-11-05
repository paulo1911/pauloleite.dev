# Sprint 2 — UX Architecture & Wireframes

Wireframes navegáveis: `docs/wireframes.html` (desktop e mobile, 4 páginas). Conteúdo marcado **[pendente]** depende de validação do Paulo (ver `SPRINT0_AUDIT.md` §4). Nada aqui é conteúdo final.

## 1. Objetivos e público
| Visitante | Chega por | Quer | Conversão principal |
|---|---|---|---|
| Dev júnior/pleno em busca de carreira | Instagram (bio) | Aprender, ser mentorado | Mentoria ADPList; compra de livro/SmartBook |
| Profissional/recrutador | LinkedIn, busca | Entender quem é Paulo | LinkedIn / contato |
| Usuário Android/homelab | Projetos | Conhecer DogNAS | Clique para dognas.app |

Meta de UX: em **≤ 5 s no mobile** o visitante entende quem é Paulo e vê um próximo passo. 70%+ do tráfego virá do Instagram → **mobile-first**, polegar, 1 coluna.

## 2. Sitemap
```
/                  Início
/conhecimento/     Conhecimento  (#livros · #smartbooks · #recomendacoes)
/projetos/         Projetos      (DogNAS; lista extensível)
/conecte-se/       Conecte-se
(reservado) /blog/ fora do escopo da v1 — slot no menu e no sitemap.xml não criado
```
Navegação global: Início · Conhecimento · Projetos · Conecte-se. Rodapé repete redes + nota de afiliados. Sem CTA duplicado concorrente: **1 CTA primário por tela**.

## 3. Estrutura das páginas (ordem de blocos)
**Início** — 1 Hero (foto real, eyebrow, H1 tagline, bio curta, CTA primário "Explorar conhecimento", secundários Instagram/LinkedIn) · 2 Livros em destaque (2–3 cards) · 3 Mentoring (faixa com CTA ADPList + aviso de disponibilidade) · 4 Destaque DogNAS (card featured) · 5 Conecte-se (strip de ícones) · Footer.
**Conhecimento** — Cabeçalho + âncoras · Livros próprios · SmartBooks (Hotmart) · Recomendações por categoria (Tecnologia, Liderança, Produtividade) · Nota de afiliados.
**Projetos** — Cabeçalho ("Things I've built…") · DogNAS featured (screenshot real, descrição, CTA `dognas.app`) · Card "mais em breve" (marca a extensibilidade).
**Conecte-se** — Cabeçalho · Card Mentoring ADPList (destaque) · Cards sociais: Instagram, LinkedIn, YouTube **[URL do canal pendente]**, Podcast **[pendente]**, WhatsApp/e-mail **[decisão pendente]**.

## 4. Fluxos principais
1. **Instagram → compra:** bio → `/?utm_source=instagram&utm_medium=bio` → Hero → "Explorar conhecimento" → livro → Amazon/Hotmart (`book_click`).
2. **Instagram → mentoria:** bio → `/` → faixa Mentoring → ADPList (`mentoring_click`). Atalho no menu? Não: CTA fica no conteúdo e em Conecte-se.
3. **Descoberta de projeto:** `/` → card DogNAS (`featured_click`) → `/projetos/` → `dognas.app` (`project_click`).
4. **Contato:** qualquer página → rodapé/Conecte-se → rede/contato (`social_click`, `contact_click`).

Links externos abrem em nova aba com `rel="noopener"`; afiliados com `rel="sponsored noopener"`. Indicar visualmente (ícone `arrow-up-right`) e com texto acessível "abre em nova aba".

## 5. Comportamento responsivo
| Faixa | Layout |
|---|---|
| < 48em (mobile) | 1 coluna; menu hambúrguer (`aria-expanded`); hero empilhado: foto acima do texto; CTAs largura total |
| 48–64em | 2 colunas de cards; nav horizontal |
| ≥ 64em | hero 2 colunas (texto | foto); grids de 3; container 72rem |
Mobile: CTA primário visível sem rolar; alvos ≥44px; nenhum scroll horizontal.

## 6. Mapa de eventos GA4 (Sprint 5)
| Evento | Elemento | Parâmetros |
|---|---|---|
| hero_cta_click | CTA do hero | `cta_id`, `destination` |
| book_click | card de livro/SmartBook/recomendação | `book_id`, `category`, `store` (amazon/hotmart/shopee) |
| mentoring_click | CTA ADPList | `placement` (home/conecte-se) |
| project_click | CTA de projeto | `project_id` |
| featured_click | card em destaque na home | `item_id` |
| social_click | Instagram/LinkedIn/YouTube/Podcast | `network` |
| contact_click | WhatsApp/e-mail | `method` |
Implementação: atributos `data-event` + `data-*` no HTML, um único listener delegado; GA4 só carrega se houver ID (sem consentimento/ID = no-op). **LGPD:** avaliar aviso de cookies antes de ativar GA4 (decisão do Paulo).

## 7. Modelo de dados (JSON, Sprint 4)
`data/site.json` (nome, tagline, bio, urls base) · `data/books.json` · `data/smartbooks.json` · `data/recommendations.json` · `data/projects.json` · `data/socials.json`.
Item padrão: `{ "id", "title", "description", "url", "image", "category", "tags", "status": "published|draft", "store" }`. `status: draft` não renderiza — assim conteúdo não validado (JR, Podcast, Mentoring) fica no JSON sem aparecer. Páginas renderizam via `fetch` + templates em JS; **fallback `<noscript>` e conteúdo crítico (hero, livros destaque) em HTML estático** para SEO e performance. Blog futuro: `/blog/` + `data/posts.json` sem mudar a arquitetura.

## 8. Acessibilidade e SEO por página
Um `<h1>` por página; ordem de headings sem saltos; landmarks; `aria-current`; foco visível; imagens com `alt` descritivo; contraste conforme Design System. `<title>`/description únicos, canonical, OG por página (Sprint 5). Ordem de foco = ordem visual.

## 9. Riscos e decisões pendentes de UX
1. **Dependência de JSON via fetch:** quebra em `file://` e sem JS → mitigado por HTML estático nas seções críticas; durante o desenvolvimento usar servidor local.
2. **Mentoring depende de ADPList** (plataforma de terceiros, disponibilidade variável): usar texto "sujeito à disponibilidade" e `status` no JSON.
3. **Volume de recomendações (24 links):** apresentar em lista compacta com "ver mais", para não diluir o hero. Neurodiversidade/Setup seguem pendentes.
4. **Foto hero:** layout depende de enquadramento; sem foto real, o hero usa apenas tipografia (sem avatar fictício).
5. **Número de livros em destaque na home:** 2 (confirmados) ou 3 (se JR for validado).
