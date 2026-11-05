# Deploy — GitHub Pages + pauloleite.dev

**Estado: preparado, NÃO publicado.** Repositório privado, Pages desativado, páginas com `noindex`.

## Já preparado no repositório
- `CNAME` → `pauloleite.dev` (usado quando o Pages for ativado a partir da branch `main`, pasta raiz).
- `.nojekyll` (serve os arquivos como estão).
- `404.html` (gerado por `tools/build.py`, caminhos absolutos — requer o domínio na raiz).

## Checklist de publicação (executar só com aprovação explícita do Paulo)
1. DNS: TXT de verificação (`_github-pages-challenge-paulo1911`) + 4 registros A (+ AAAA opcional) em `@` + CNAME `www` → `paulo1911.github.io` (ver conversa; remover os 2 A antigos do GoDaddy e o encaminhamento de domínio).
2. `git push` da `main`.
3. Tornar o repositório **público** (Pages gratuito exige) — isso torna o código visível a todos.
4. Settings → Pages: Source = *Deploy from a branch*, `main` / `/ (root)`; Custom domain = `pauloleite.dev`.
5. Aguardar o certificado e marcar **Enforce HTTPS** (domínios `.dev` só abrem em HTTPS).
6. Conferir: `dig`, https://pauloleite.dev, https://www.pauloleite.dev (redireciona ao apex), 404, links.
7. Liberar indexação: `"indexable": true` em `data/site.json` → `python3 tools/build.py` → commit/push (remove `noindex` e troca `robots.txt` para `Allow: /`).
8. Enviar `https://pauloleite.dev/sitemap.xml` ao Google Search Console; rodar PageSpeed Insights; validar OG no LinkedIn Post Inspector.
9. Trocar o link da bio do Instagram para `https://pauloleite.dev/?utm_source=instagram&utm_medium=bio&utm_campaign=link_in_bio` (manter o Linktree até confirmar que tudo funciona).

## Reversão
Settings → Pages → Unpublish; ou voltar o repositório a privado (o site sai do ar).
