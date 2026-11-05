# Design System v1 — pauloleite.dev

Guia vivo: abra `docs/design-system.html` no navegador (usa `css/tokens.css`, `base.css`, `components.css`).
Regra: **nenhum valor de cor/espaçamento fora de `css/tokens.css`**.

## Arquivos
| Arquivo | Função |
|---|---|
| `css/tokens.css` | Variáveis CSS (cores, tipografia, espaço, raio, sombra, motion) |
| `css/base.css` | Reset, elementos, layout (`.container`, `.section`, `.grid`), utilitários, skip-link |
| `css/components.css` | `.btn`, `.card`, `.book`, `.badge`, `.social`, `.section-head`, header/nav, footer, `.note` |

## Cores e contraste (WCAG 2.2 AA)
| Token | Valor | Uso | Contraste |
|---|---|---|---|
| `--color-bg` | #0B0D14 | fundo | — |
| `--color-surface` | #151827 | cards | — |
| `--color-primary` | #8B5CF6 | ícones, brilhos, indicadores | 4.58:1 sobre bg |
| `--color-primary-strong` | #7C3AED | fundo de botão sólido | texto branco 5.70:1 |
| `--color-accent` | #C4B5FD | links, eyebrow, foco | 10.5:1 bg · 9.5:1 surface |
| `--color-text` | #F8FAFC | texto | 18.6:1 bg · 16.8:1 surface |
| `--color-text-muted` | #9298AA | texto secundário | 6.7:1 bg · 6.1:1 surface |
| `--color-border` | #292E40 | divisores decorativos | 1.4:1 (não usar p/ limites de UI) |
| `--color-border-strong` | #5B6280 | bordas de botão/controle | ≥3:1 |

**Desvios da paleta original (decisões a aprovar):**
1. Texto branco sobre `#8B5CF6` dá 4.23:1 (reprova AA). Botões sólidos usam `#7C3AED` (derivado); `#8B5CF6` fica para ícones/brilhos.
2. `#8B5CF6` como texto sobre surface dá 4.16:1 (reprova). Texto colorido usa sempre `--color-accent`.
3. `#292E40` tem 1.4:1 e serve só como divisor; foi criado `--color-border-strong`.

## Tipografia
Manrope 700–800 (títulos), Inter 400–600 (corpo). Escala fluida com `clamp()`: `--fs-xs` … `--fs-3xl`. Line-height corpo 1.65.
Google Fonts com `display=swap`; auto-hospedar fica como otimização da Sprint 6.

## Espaço, forma, movimento
Espaço base 4px (`--space-1…9`). Raios 8/12/16/20px. Cards usam gradiente sutil + `--shadow-card`; hover sobe 4px com borda primary. Transições 150–250ms; `prefers-reduced-motion` desliga animações.

## Componentes
- **Botão** `.btn--primary | --secondary | --ghost` — alvo mínimo 44px, ícone Lucide opcional.
- **Card** `.card` (+ `--interactive`, `--featured`) — com `.card__link` o card inteiro é clicável com **um único** tab stop e foco visível.
- **Book** `.card.book` — capa 2:3 + metadados.
- **Social** `.card.social` — ícone, rótulo, handle.
- **Badge** `.badge`, `.badge--muted`; **Section head**; **Nav** (desktop pill + menu mobile com `aria-expanded`); **Footer**; **Note** (divulgação de afiliados).

## Acessibilidade embutida
Skip-link, `:focus-visible` com anel 3px accent, `aria-current="page"`, landmarks (header/nav/main/footer), alvos ≥44px, `lang="pt-BR"`, hierarquia de headings.

## Ícones
Lucide, versão fixada (`0.468.0`) via unpkg no guia. Na Sprint 3 decidir entre sprite SVG inline (sem dependência de CDN, recomendado) ou CDN.

## Padrões de conteúdo (JSON, Sprint 4)
Livros, projetos e redes virão de `data/*.json`; os componentes acima são os moldes. Novo projeto = nova entrada em `projects.json` renderizada por `.card`.

## Limitações conhecidas
- Placeholders de capa/screenshot: aguardam imagens reais (pendência Sprint 0).
- Verificado visualmente no Chrome (1280px e 500px). Teste em dispositivos reais e Lighthouse ficam para a Sprint 6.
