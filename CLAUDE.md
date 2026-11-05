# CLAUDE.md — pauloleite.dev

Personal Brand Hub de Paulo Leite (Engineering, Architecture, Leadership). Substitui o Linktree.
Tagline: *Building technology. Developing people.*

## Regras
- Ler este arquivo e `PROJECT_PLAN.md` antes de trabalhar.
- Executar uma sprint por vez; aguardar aprovação antes da próxima.
- Não inventar URLs, fotos, depoimentos, métricas ou ofertas. Preservar links validados.
- Mobile-first, acessibilidade WCAG 2.2 AA.
- Executar testes e atualizar documentação a cada sprint.
- **Nunca publicar (GitHub Pages, domínio, merge para produção) sem aprovação explícita.**

## Stack
HTML5 semântico, CSS3, Vanilla JS, Lucide Icons, Google Fonts (Manrope + Inter), JSON em `data/` para conteúdo, GA4 opcional (desativado até haver ID).
Sem React, Next.js, backend ou banco de dados na v1. Reservar arquitetura para blog futuro (fora do escopo).

## Estrutura
`index.html`, `conhecimento/`, `projetos/`, `conecte-se/`, `assets/images/`, `css/`, `js/`, `data/`, `docs/`.
Conteúdo (livros, projetos, redes) em `data/*.json`; páginas HTML são **geradas** por `python3 tools/build.py` (não editar à mão). QA: `tools/qa.py`. Ver `README.md`, `docs/`.

## Design tokens (Dark Premium)
bg #0B0D14 · surface #151827 · primary #8B5CF6 · accent #C4B5FD · text #F8FAFC · text-2 #9298AA · border #292E40.
Cards radius 12–20px.
