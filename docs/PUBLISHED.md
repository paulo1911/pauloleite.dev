# Publicação — estado (2026-11-05)

**Feito (GitHub):** push da `main`, repositório público, Pages ativo (branch `main`, raiz), domínio personalizado `pauloleite.dev`, indexação liberada (`"indexable": true`), build "built", páginas respondem 200 pelo IP do Pages.

**Pendente (GoDaddy → DNS, feito pelo Paulo):**
1. Apagar os 2 registros A antigos (`13.248.243.5`, `76.223.105.230`) e criar 4 A: `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` (AAAA do IPv6 já estão corretos).
2. CNAME `www` → `paulo1911.github.io` (hoje aponta para `pauloleite.dev`).
3. Desligar "Encaminhamento de domínio" no GoDaddy, se ativo.
4. (Recomendado) verificar o domínio em github.com/settings/pages (TXT `_github-pages-challenge-paulo1911`).

**Depois do DNS propagar:** Settings → Pages → marcar **Enforce HTTPS** (certificado automático, até ~1h; `.dev` exige HTTPS) → conferir https://pauloleite.dev e https://www.pauloleite.dev → Search Console (sitemap) → PageSpeed Insights → trocar o link da bio do Instagram (UTMs em `docs/ANALYTICS.md`).
