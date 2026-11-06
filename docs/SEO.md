# SEO, dados estruturados e llms.txt

## O que é gerado (tools/build.py)
- **Metadados por página:** title, description, canonical, hreflang pt-BR, robots (controlado por `indexable` em `data/site.json`), Open Graph e Twitter Card.
- **Imagem de compartilhamento:** padrão do site (`assets/images/og-image.jpg`) e uma por livro/SmartBook (`assets/images/og/<id>.jpg`). Regerar com `python3 tools/make_og.py` (requer Chrome e Pillow).
- **JSON-LD:**
  - Início: `Person` (com `sameAs` e `knowsAbout`) e `WebSite`.
  - Sobre: `ProfilePage` + `Person`. Conhecimento: `CollectionPage`. Conecte-se: `ContactPage`.
  - Livros: `Book` (SmartBooks: `CreativeWork`) com `datePublished` (campo `published` em `data/books.json`) e `dateModified`.
  - Mentoria: `Service` (gratuito) + `FAQPage`. Projetos: `SoftwareApplication`.
  - `BreadcrumbList` em todas as páginas internas.
- **sitemap.xml:** `lastmod` real por página (ver abaixo). `changefreq`/`priority` não são usados (o Google os ignora).
- **llms.txt e llms-full.txt:** gerados a partir dos dados do site, sem e-mail nem telefone.

## Como funciona o lastmod
`data/lastmod.json` guarda, por página, um hash do **conteúdo** (dados de `data/*.json` e textos da página) e a data. Quando o conteúdo muda, a data vira a do dia do build. Mudanças só de CSS/JS/template **não** alteram o lastmod. Versione esse arquivo junto com o conteúdo.

## Conferência
- `python3 tools/seo_check.py`: valida sitemap, title/description (tamanho e duplicidade), canonical, H1 único, og:image no disco, JSON-LD válido e links do llms.txt.
- Valide os dados estruturados também no Rich Results Test e no Schema Markup Validator (ferramentas do Google/Schema.org, só online).

## Fora do código (ações manuais)
- Enviar `https://pauloleite.dev/sitemap.xml` ao Google Search Console.
- Forçar a atualização de pré-visualização no LinkedIn (Post Inspector) após trocar imagens.
