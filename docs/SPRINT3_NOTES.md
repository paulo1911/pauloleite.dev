# Sprint 3 — Core Development (notas)

## Entregue
- 4 páginas estáticas: `index.html`, `conhecimento/`, `projetos/`, `conecte-se/` (HTML5 semântico, 1 `<h1>` por página, landmarks, skip-link, `aria-current`).
- Header/nav (desktop pill + menu mobile acessível), footer, Hero com foto, componentes do Design System aplicados.
- `js/main.js`: toggle do menu (aria-expanded, Esc, fecha ao navegar). Sem dependências.
- Ícones Lucide 0.468.0 como sprite local `assets/icons/sprite.svg` (sem CDN). Para adicionar um ícone: baixar de `lucide-static` e incluir um `<symbol id="i-nome">`.
- Atributos `data-event` / `data-*` já nos CTAs (hero_cta_click, book_click, mentoring_click, project_click, featured_click, social_click) — o listener GA4 vem na Sprint 5.

## Decisões
- **`noindex, nofollow` em todas as páginas** até o lançamento aprovado (remover na Sprint 7).
- Caminhos relativos por profundidade (funciona em qualquer host, inclusive antes do domínio).
- (Superado na Sprint 4) Páginas agora geradas por `tools/build.py`; header/footer vêm do template.
- Foto do hero: **provisória**, a mesma do Linktree (2000×2000, reduzida a 960px). Substituir se houver foto melhor.

## Conteúdo (somente validado)
Hero (bio do Linktree), 2 livros próprios (links Amazon), mentoring ADPList, DogNAS, Instagram, LinkedIn.
**Fora/rascunho:** livro JR, SmartBooks, recomendações (placeholder "em preparação"), YouTube, podcast, WhatsApp/e-mail. Capas e screenshots são ícones/placeholders até chegarem imagens reais.
Conteúdo ainda está no HTML; a migração para `data/*.json` é a Sprint 4.

## Como rodar localmente
`python3 -m http.server 8765` na raiz → http://localhost:8765/ (o sprite SVG exige HTTP, não `file://`).

## Testes feitos
Renderização no Chrome (1280px e 500px) de Início e Conecte-se; Conhecimento e Projetos gerados pelo mesmo layout, não inspecionados em screenshot. Script: 1 h1/página, imagens com alt, sem ids duplicados, sem links internos quebrados. **Não testado:** menu mobile por interação real, teclado/leitor de tela, dispositivos reais, Lighthouse (Sprint 6).
