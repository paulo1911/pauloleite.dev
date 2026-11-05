# pauloleite.dev

Personal Brand Hub de Paulo Leite — Engineering, Architecture, Leadership.

Site estático (HTML/CSS/Vanilla JS) para GitHub Pages. Veja `PROJECT_PLAN.md` e `CLAUDE.md`.

## Editar conteúdo
O conteúdo vive em `data/*.json` (livros, SmartBooks, recomendações, projetos, redes, mentoring). Itens com `"status": "draft"` não aparecem no site.
Depois de editar, regenere as páginas:

```sh
python3 tools/build.py        # só stdlib, sem dependências
python3 -m http.server 8765   # preview em http://localhost:8765/
```

As páginas HTML são **geradas** — não edite `index.html`, `conhecimento/`, `projetos/` ou `conecte-se/` à mão; altere `data/` ou `tools/build.py`.

**Status:** Sprint 4 concluída. Nada publicado; páginas com `noindex` até a Sprint 7.
