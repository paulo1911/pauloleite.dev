# Qualidade (Sprint 6)

## Como rodar
```sh
python3 -m http.server 8765 &          # na raiz
python3 -m venv /tmp/qa && /tmp/qa/bin/pip install websocket-client
/tmp/qa/bin/python tools/qa.py          # requer Google Chrome
```
`tools/qa.py` abre o site no Chrome headless (desktop 1280px e mobile 390px, 5 páginas) e roda **axe-core 4.10** (WCAG 2.0/2.1/2.2 A+AA + boas práticas), checa overflow horizontal, erros de console, tempos de carregamento, abertura/fechamento do menu mobile (clique e Esc) e foco por teclado.

## Resultado (2026-11-05, local)
- **0 violações axe** nas 5 páginas × 2 viewports (inclui contraste e tamanho de alvo 2.5.8).
- Sem overflow horizontal e sem erros de console.
- Menu mobile: inicia fechado, abre (`aria-expanded`), Esc fecha.
- Teclado: 18 elementos focáveis na home, todos recebem foco; primeiro foco = "Pular para o conteúdo".
- Carregamento local: FCP ≈ 50–300 ms (não representa rede real).
- Peso (sem compressão): home ≈ 198 KB, demais ≈ 105–115 KB.

## Correções feitas nesta sprint
- `heading-order` em Projetos (h3 logo após h1) → card do projeto usa h2 nessa página.
- Fontes **auto-hospedadas** (Inter e Manrope variáveis, subset latin, 73 KB): removidas requisições ao Google Fonts (mais rápido, mais privado/LGPD) e preload das fontes.
- O próprio QA pegou um erro de caminho nas fontes (404) antes do commit.

## Não coberto (limites honestos)
- Lighthouse/Core Web Vitals reais, rede móvel lenta: dependem do site publicado (rodar PageSpeed Insights após o deploy).
- Leitor de tela (VoiceOver/NVDA) e teste em iPhone/Android reais: não feito; recomendo uma passada manual sua.
- Safari/Firefox: só Chrome foi testado.
- Axe não cobre tudo (cobre ~30–40% dos problemas de acessibilidade); revisão manual de ordem de leitura e textos de link recomendada.
