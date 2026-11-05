# Sprint 0 — Discovery & Brand Audit

Fonte: https://linktr.ee/pauloleite.dev (coletado em 2026-11-05). Nenhum código do site foi implementado.

## 1. Perfil atual no Linktree
- Título: **Paulo Leite**
- Bio: "Engenheiro de software com 20+ anos de experiência! Código, liderança e inovação"
- Foto de perfil: `https://ugc.production.linktr.ee/376a4d1f-ed42-47a9-b652-356e1b005b9a_IMG-6535.jpeg` (resolução desconhecida; provavelmente insuficiente para hero — pedir original)
- Redes (ícones): Instagram `instagram.com/pauloleite.dev`, LinkedIn `linkedin.com/in/paulorobertoleite`

## 2. Inventário de links

Status: ✅ responde 200 · 🔒 bloqueia verificação automática (405 a HEAD de bot; Amazon/LinkedIn abrem com GET) · ⚠️ requer atenção.

### Topo (fora de grupos)
| Item | URL | Status |
|---|---|---|
| System Design para Desenvolvedores (livro próprio) | https://www.amazon.com.br/dp/B0F35ZZ6GW | 🔒 |
| O Arquiteto da Própria Carreira (livro próprio) | https://www.amazon.com.br/dp/B0G5JLT49N | ✅ (GET 200) |
| Pessoa Engenheira de Software JR (livro próprio) | https://a.co/d/90pdQ7k | ✅ GET 200; HEAD 404. Página da Amazon existe — **disponibilidade a validar** |
| LinkedIn | https://br.linkedin.com/in/paulorobertoleite | 🔒 |
| YouTube — "Energia Mental e Foco Máximo" (Brown Noise) | https://youtu.be/j9AryH7VKF4 | ✅ |
| WhatsApp | https://wa.me/5511998812487 | ✅ |
| Instagram | https://www.instagram.com/pauloleite.dev (com `igsh` e `utm_source=qr`) | ✅ |

### Grupo "Meus Projetos"
- DogNAS — https://dognas.app ✅

### Grupo "SmartBooks com 50% Desconto" (Hotmart)
| Item | Status |
|---|---|
| Plano de Ação: Do Zero ao Primeiro Emprego em Tecnologia | ✅ |
| Dominando Entrevistas | ✅ |
| Disciplina: O Segredo do Sucesso para crescer na Tecnologia | ✅ |

⚠️ Links Hotmart contêm parâmetros de rastreio (`_hi`, `bid`) do Linktree; limpar. O desconto de 50% **não está confirmado** como vigente — não exibir sem validação.

### Recomendações (afiliados Amazon `amzn.to` / Shopee)
- **Tecnologia (12):** System Design Interview Vol. 2; Programador Pragmático; Como ser um programador melhor; Migrando Monolíticos para Microsserviços; Arquitetura Limpa; Código Limpo; Staff Engineer's Path; A Philosophy of Software Design; Entendendo Algoritmos; Estruturas de Dados e Algoritmos com JavaScript; Lógica de Programação e Algoritmos com JavaScript; Introdução à Programação com Python.
- **Liderança (5):** Carreiras Exponenciais; Seja egoísta com sua carreira; Nada pode me ferir; Nunca é hora de parar; Cérebro com Foco e Disciplina.
- **Produtividade (2):** Cubo Pomodoro (Shopee); A técnica Pomodoro.
- **Neurodiversidade (1):** Guia para Compreensão e Manejo do TDAH.
- **Setup (3):** Suporte Notebook (Shopee); Monitor portátil BETTDOW (Shopee); Roteador Huawei Mesh (Amazon).

Total: 38 links (7 topo, 1 projeto, 3 SmartBooks, 24 recomendações/afiliados, 3 setup).
`amzn.to` não pôde ser validado individualmente (bloqueio a bots); revalidar manualmente.

## 3. Mapeamento para o novo site
| Plano | Fonte no Linktree | Lacuna |
|---|---|---|
| Início | foto + bio + livros próprios | foto de alta resolução; headline final; texto de apresentação |
| Conhecimento › Livros | 3 livros próprios | capas (assets reais) e confirmação do livro JR |
| Conhecimento › SmartBooks | 3 links Hotmart | capas; preço/desconto vigente |
| Conhecimento › Recomendações | Tecnologia, Liderança, Produtividade | Neurodiversidade e Setup **não estão no escopo do plano** — decidir (manter/descartar) |
| Projetos | DogNAS | screenshots reais |
| Conecte-se | Instagram, LinkedIn, WhatsApp, YouTube | **Spotify/podcast: não existe no Linktree**; URL do canal YouTube (hoje só um vídeo); e-mail |
| Mentoring | — | **Nada no Linktree.** Sem informação de oferta/disponibilidade |

## 4. Pendências (decisões suas)
1. **Mentoring:** existe? Disponibilidade, formato, link de contato. Sem confirmação, a seção fica fora.
2. **Podcast/Spotify:** URL real, ou remover do Conecte-se.
3. **YouTube:** URL do canal (o Linktree só tem um vídeo de brown noise).
4. **Contato:** WhatsApp (+55 11 99881-2487 já público no Linktree) e/ou e-mail — qual exibir?
5. **Livro JR:** disponível para venda? Manter como destaque?
6. **SmartBooks:** oferta de 50% ainda vale? Preços?
7. **Neurodiversidade e Setup:** incluir ou descartar?
8. **Foto e capas:** enviar originais (foto hero, 3 capas de livros, 3 capas SmartBooks, screenshots DogNAS).
9. **GA4:** possui ID de medição (`G-…`)?
10. **Domínio:** pauloleite.dev está registrado com acesso ao DNS? Onde (registrar)?
11. **Afiliados:** divulgar nota de afiliado nas recomendações (exigência da Amazon Associados).

## 5. Riscos
- **Links de afiliados** (Amazon/Shopee): exigem aviso de divulgação; `amzn.to` pode expirar — revalidar antes do lançamento.
- **Perda de tráfego na migração:** o Linktree continua sendo a bio do Instagram até a Sprint 7; só trocar após aprovação e verificação do site.
- **Foto de perfil** do Linktree pode ter baixa resolução → impacto no hero e no LCP/Open Graph.
- **Conteúdo comercial sem validação** (desconto, disponibilidade, preços): regra do plano proíbe inventar ofertas.
- **Telefone pessoal** exposto no WhatsApp: confirmar que quer mantê-lo público no site (indexável por buscadores).
- **Links com rastreio** (`igsh`, `_hi`) vazam identificadores do Linktree; substituir por URLs limpas com UTMs próprios.
- **GitHub Pages:** repositório está privado; Pages gratuito exige público (decisão na Sprint 7).

## 6. Estado do repositório
Scaffold inicial (CLAUDE.md, PROJECT_PLAN.md, README, pastas vazias). Sem assets reais ainda.

## Próximo passo
Aguardando respostas às pendências (§4) e aprovação para iniciar a **Sprint 1 — Brand Identity & Design System**.
