# Sprint 4 — Content & Conversion (notas)

## Entregue
- Conteúdo movido para `data/`: `site.json`, `books.json`, `smartbooks.json`, `recommendations.json`, `projects.json`, `socials.json`.
- `tools/build.py` (Python stdlib) gera as 4 páginas a partir do JSON → HTML estático completo (SEO, no-JS, sem fetch). **Desvio do plano da Sprint 2** (que previa render via fetch no cliente): escolhido por SEO/performance e por funcionar sem servidor. Continua sem backend/framework.
- **Conhecimento:** 3 livros próprios (inclui eBook Kindle JR), 3 SmartBooks (Hotmart), recomendações Tecnologia (12, 6 visíveis + "Ver mais"), Liderança (5), Produtividade (2); nota de afiliados.
- **Início:** hero, 2 livros em destaque (`featured`), mentoring ADPList, DogNAS, contato (WhatsApp + e-mail).
- **Conecte-se:** mentoring, Instagram, LinkedIn, WhatsApp, e-mail.
- E-mail **não está no HTML**: é montado por `js/main.js` a partir de `data-email-*`; sem JS aparece "[arroba]" sem link.
- Links de afiliados com `rel="sponsored noopener"`; todos os externos com `noopener`.

## Rascunho (`status: draft`, não renderizado)
YouTube, Podcast (sem URL — sem conteúdo publicado); categorias Neurodiversidade e Setup (links preservados em `recommendations.json`).

## Links
Hotmart sem parâmetros de rastreio do Linktree (3 URLs limpas retornaram 200); livro JR com URL limpa da Amazon; `amzn.to`/Shopee preservados (carregam o tracking de afiliado). Verificado com curl em 2026-11-05: Hotmart, Amazon JR e WhatsApp = 200; `amzn.to` e LinkedIn não verificáveis por bot.

## Conversão
1 CTA primário por tela; mentoring ADPList na home e no Conecte-se; todos os CTAs com `data-event` (listener na Sprint 5).

## Limitações
- Sem desconto/preço nos SmartBooks (oferta de 50% não confirmada).
- Capas e screenshots = placeholders (aguardam imagens reais; `image` nos JSON).
- Textos de apoio (ex.: "Guias práticos para destravar a carreira…", "Leituras e materiais que indico") foram redigidos por mim — **revisar o tom**.
- Verificação: build + checagem automática (1 h1/página, alt, ids, links internos, noopener, drafts ausentes, e-mail fora do HTML) + screenshots de Conhecimento (desktop) e Conecte-se (mobile) + execução do JS do e-mail em Chrome headless. Não testado: menu mobile por clique, teclado/leitor de tela, dispositivos reais.
