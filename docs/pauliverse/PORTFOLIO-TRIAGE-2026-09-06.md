# Pauliverse Portfolio Triage — 2026-09-06

Status: registry refresh (evidence sweep), not a deployment claim. Source of truth for node shape is `schemas/portfolio-snapshot.schema.json`; this file is a generated view of `seeds/portfolio.snapshot.2026-09-06.json`. Decisions are Fable's recommendation under the Pauliverse Operating Contract; **DELETE always requires an explicit owner gate**, ARCHIVE means stop investment and keep history.

**Coverage:** 289 repositories under `executiveusa` (page-complete via GitHub search, 3 pages). 175 private, 114 public. 101 carry a Lovable scaffold signature.

## Decision counts

| Decision | Count | Meaning |
|---|---|---|
| USE | 84 | keep and operate |
| SELL | 1 | package as offer |
| MERGE | 29 | fold into canonical node |
| PARK | 53 | no investment until evidence |
| ARCHIVE | 122 | stop; keep history; delete only with owner gate |

## Evidence state

| State | Count |
|---|---|
| source-only | 104 |
| builds-claimed | 80 |
| stub/empty | 80 |
| deployed-evidence | 17 |
| fork/reference | 8 |

## Type

| Type | Count |
|---|---|
| template | 91 |
| product | 78 |
| client-site | 40 |
| unknown | 25 |
| stub/empty | 17 |
| reference | 10 |
| runtime | 8 |
| archive | 6 |
| specialist | 4 |
| skill | 3 |
| employee | 3 |
| adapter | 3 |
| fork/reference | 1 |

## Deployment evidence (URL found in source; Fable independently probed the ones marked ✔)

- ✔ `asc3nd-frontend-website-` → https://asc3nd.org — ASC3ND Social Purpose OS public frontend (Next.js 16)
- ✔ `asce3nd-interactive-document` → https://asc3nd-interactive-document.vercel.app — ASC3ND 90-Day Social Presence Builder interactive workbook (bilingual, URL-encoded state), prepared by Macs Di
- · `AVATAR` → https://profilepalette.vercel.app/ — Cloned profilepalette 3D portfolio template
- ✔ `dos2a` → https://dos2a.vercel.app — dos A — Sovereign AV Business OS reference tenant (CDMX event production), Next 15 + Prisma + Stripe + Twilio
- · `kupuri-media-cdmx` → https://akashportfolio.vercel.app — Kupuri Media's full-stack monorepo (internally named 'AKASHPORTFOLIO') combining the live portfolio frontend w
- ✔ `la-silueta` → https://la-silueta.vercel.app — La Silueta mezcal luxury landing (React18/GSAP/Firebase/Vapi)
- · `macs-agent-portal` → https://macs-agent-portal-pi.vercel.app — Agent MAXX front page / Stacy dashboard (Lovable + Vite); SECURITY_INCIDENT.md at root
- ✔ `newworldkids` → https://nwkids.org — New World Kids nonprofit platform (Turborepo: web, timeline, Strapi CMS, Solana donations, Stellar agents)
- ✔ `pauli-command-center` → https://pauli-command-center.vercel.app — Owner cockpit (Next.js 15 PWA): chat/voice → Hermes/Terabithia and StarNet realms, approvals, fleet; no README
- ✔ `PAULIS-PLACE` → https://paulis-place.vercel.app — Pauli's Place — voice-first business OS + 3D world; FastAPI backend on Railway, Next frontend on Vercel
- · `postateesstudio-` → https://ai.studio/apps/drive/1v2pbIXqDrvZ1wQSF17PBDSZbmrBLk-Ru — Canonical, most complete Postatees AI design-studio app - Gemini-powered image/video generation UI built on Go
- · `spy-scape-mustang-maXx` → https://spy-scape-mustang-maxx-ncl58dyko-the-pauli-effect.vercel.app — Agent MAXX 006 cinematic site + FastAPI control plane (Lead Desk)
- · `tierra-sagrada` → https://tierra-sagrada.vercel.app — Site with a stated live deployment (name suggests a wellness/spiritual-land brand, 'Sacred Earth')
- · `UJIMA` → https://ujima-ai.netlify.app — Sovereign agentic OS for nonprofits (rename of asc3nd-social-purpose-os v0.5.0); monorepo with .beads, icm, IC
- · `veronika-mvp-final` → https://veronikadmitova.com — Veronika Dmitova's business-consulting website/MVP — the canonical, actually-deployed Veronika product
- · `vibe-engineering` → https://vibe-engineering-lime.vercel.app — Open-source quality/architecture layer: Claude Code plugin + CLI + MCP server (Vibe/ICM tooling)
- · `VIPposta` → https://ai.studio/apps/drive/1v2pbIXqDrvZ1wQSF17PBDSZbmrBLk-Ru — Earlier/narrower iteration of the same AI-Studio-exported Postatees app, scoped to image generation only

## Duplicate / supersession clusters (edges in the snapshot)

- **frithco-final-version** ← FRITHCO, fritco-locale-scaffold, fritco-v2, frithco-2.0, frithco-3.0, frithco-remix
- **pauli-command-center** ← pauli-deck, pauli-mobile-agent, pauli-studio-control-plane, the-pauli-effect, watcher-factory-dashboard
- **pauli-montage-video-agent** ← Pauli-universe-video, cheggie-studios-, maxx-clipz, pickaxe-nanobanana-g
- **YAPPYVERSE-FACTORY** ← yappyland, yappyverse, yappyverse-drop-control, yappyverse-genesis-project
- **veronika-mvp-final** ← veronika-interactive-document, veronika-jetty-second-brain, veronika-mvp-export
- **asc3nd-frontend-website-** ← asc3nd-events-page, asc3nd-supabase-landing, ascend-demonstration-page
- **postateesstudio-** ← VIPposta, postatees-studio, postateesstudioV.1
- **synthia** ← SYNTHIA-3.1, synthia-3-1-demo
- **thepaulieffect** ← maxx-craft, the-pauli-effect-2026
- **cheggie-dashboard-** ← Cheggie-trade-V2, cheggie-lifestyle-finance
- **impact-city-2026** ← impact-city-builder-verse, impact-city-game
- **social-media-template** ← buffer-blaster-
- **impact-city-game** ← impact-city-2026
- **sweet-psilocybe-app** ← sweet-psilocybe-landing
- **frithco-2.0** ← preeway-pressure-washing
- **dos2a** ← kupuri-client-renta-de-audio-
- **kupuri-studios-landing** ← Telegram-bot
- **nomaticthecost** ← nomadasearch
- **grant-agent** ← archon-lovable-nexus
- **maxx-craft** ← thepaulieffect
- **goatalliance** ← goat-alliance-scaffold
- **abby-wellness-nexus** ← metamorfosis-wellness-journey
- **cultureshocksports** ← culture-shock-sports
- **metamorfosis-wellness-journey** ← abby-wellness-nexus
- **maxx-clipz** ← maxxclipz
- **ivettemushrooms** ← ivettemilo
- **terabithiaweb3** ← schoolofterabithia
- **-yt-knowledge-extractor** ← youtubetranscripts
- **reddit-focus-finder** ← reddit-focus-insight
- **la-pizza-cubana** ← rebanada-world-pizza-hub
- **dispatchhelper** ← dispatchhelper2
- **aiwear-trend-hub-c0e24ba8** ← aiwear-trend-hub
- **BOILERBOYZ** ← BOILER-BOYZ
- **seattle-reuse-exchange** ← seattle-reuse-exchange-v2
- **youtubemonster** ← youtube-monster-tran
- **kinetic-code-canvas-dream** ← p-72343185
- **r-108043** ← r-108043-e63b540f
- **cloneflow-ai-sites** ← nodev
- **akash-master-files** ← akash-orbit-platform
- **O.W.P.I.L** ← yappyverse-merch-forge
- **BOILER-BOYZ** ← BOILERBOYZ
- **archonx-os** ← ARCHON-X2.0
- **goldenhearts** ← golden-heart-compass-ai
- **world-matrix** ← nextjs-enterprise-boilerplate
- **r-108043-e63b540f** ← r-108043
- **web3sass** ← WEB3SAAS-APP
- **sweet-psilocybe-landing** ← sweetmushrooms
- **akash-my-web-lane** ← akash-landing-page-v1.0
- **tonmay-productions** ← tonmay-interactive-document
- **asc3nd-brand-site** ← asc3nd-brand-kit-
- **kupuri-metamorphsis-second-brain** ← metamorphsis-cdmx
- **newworldkids** ← text-new-world-kids-lowrider-bike
- **postateesstudio- (unconfirmed hypothesis - part of the Postatees duplicate cluster)** ← POSTA-STUDIO.V2
- **monorepo-turborepo** ← youtubemonster2.1
- **v0-leonradio-website** ← trail-mixx
- **culture-shock-sports (unconfirmed - flagged as likely duplicate cluster, not independently verified)** ← cultureshocksports
- **youtubemonster2.1** ← youtubemonster
- **nextjs-ai-chatbot** ← chat-bot-template

## Security flags surfaced during the sweep (values were NOT copied; rotate first, then clean history)

- `chat-bot-template`: Root file listing and blob SHAs (LICENSE, .env.example, package.json, biome.jsonc) are identical to nextjs-ai-chatbot's. Same commit message pattern, created 39 minutes earlier same day - clearly the 
- `CLONELY-FANZ`: SECURITY: .env committed in public repo — verify/rotate
- `cruise-reposition-oasis`: Real monorepo structure (apps/, automations/n8n/, contracts/, docs/, supabase/). README describes affiliate cruise adapters as roadmap/stubs, not live. Last commit: 'Enable Lovable Cloud for project' 
- `frithco-final-version`: SECURITY: tracked .env at root — rotate; README copied from sibling; vercel.json added by agent
- `hiring-compass`: SECURITY: .env committed; single commit
- `macs-agent-portal`: README production alias; three deploy configs (vercel/railway/nixpacks); secrets templates present — review SECURITY_INCIDENT.md
- `modernairsolutions`: SECURITY: committed .env — rotate
- `serene-studio-flow-hub`: README states most src/services/ are MOCK implementations. Has a hardcoded mock admin password (admin123/yokai2024) documented in README - security concern if ever deployed as-is. No confirmed live UR
- `sweet-psilocybe-landing`: SECURITY: README appears to contain a live Printful API key (value not copied) — rotate; stray commit_msg files; .beads/, AGENTS, CLAUDE

## Leverage shortlist (USE/SELL with quick-revenue or client-delivery)

| repo | leverage | live? | next action |
|---|---|---|---|
| agent-fanni-kupuri- | client-delivery | no | Register Fanni blueprint in StarNet (already listed); provision scoped identity |
| agent-indigo | client-delivery | no | Complete the Vercel deployment step called out in its own README before treating any metrics as real. |
| airbnbauto | client-delivery | no | Verify real listing-automation logic exists (vs. just the shared scaffold) before quoting to a client. |
| alphadeltarecycling | client-delivery | no | Verify the recycling business is active and Stripe integration is live-configured before treating as revenue-ready. |
| asc3nd-brand-site | client-delivery | no | Owner decision on cutover |
| asc3nd-frontend-website- | client-delivery | yes | Add visible contact/booking path; keep as flagship client proof |
| botanical-memories | client-delivery | no | Capture the actual live Vercel URL and confirm the named client (Judy Bowers) is still engaged. |
| breatheinternational | client-delivery | no | Write real README; confirm deploy |
| cheggie-dashboard- | client-delivery | no | Verify CI; pick deploy target |
| cheggie-lifestyle-finance | client-delivery | no | Centralize YAPP gigaprompt as one skill |
| cloneflow-ai-sites | client-delivery | no | Use for Lovable rescue / site-rescue offers |
| coachdavis | client-delivery | no | Write real README; confirm client and store status |
| culture-shock-sports | client-delivery | no | Deploy; Stacy McSwain program (NWKids) |
| dos2a | client-delivery | yes | Remove parked marketplace code; reuse as tenant template |
| enaswigsandhair | client-delivery | no | Confirm live domain with client |
| fredo-3D | client-delivery | no | Confirm deployment status and deliver a live URL to the artist if not already done. |
| frithco-final-version | client-delivery | no | Rotate .env secrets; make canonical; salvage fritco-locale-scaffold api |
| future-champs-gym | client-delivery | no | Deploy to a preview/production environment and confirm a live URL with Future Champs. |
| goat-alliance-scaffold | client-delivery | no | Verify deploy; reconcile with goatalliance repo |
| goldenhearts | client-delivery | no | Confirm whether the Railway deployment is actually live and get the URL. |
| grant-agent | client-delivery | no | Assign to Impact Office; first real grant search for NWKids |
| humanatar-genesis-suite | client-delivery | no | Extract YAPP pattern to shared skill |
| ivettemushrooms | client-delivery | no | Confirm client and domain |
| kupuri-client-renta-de-audio- | client-delivery | no | Fix TS errors; deploy; consider merging into dos A tenant |
| kupuri-documentos-interactivos-ron | client-delivery | no | Confirm delivery/live-link status with the Ron Daugliesh engagement. |
| kupuri-media-cdmx | client-delivery | yes | Independently verify the live URL; consider renaming the repo to match its actual internal identity (AKASHPORTFOLIO). |
| kupuri-media-main-site | client-delivery | no | Capture the actual live Vercel domain and add it to the registry. |
| kupuri-media-website | client-delivery | no | Re-fetch HERO_README.md and DEVELOPMENT.md directly to get real claims/deploy info before further classification. |
| la-pizza-cubana | client-delivery | no | Find live URL; quick-win audit |
| macs-agent-portal | client-delivery | yes | Review incident file; remove redundant deploy configs |
| macsdigitalmedia | client-delivery | no | Ship approved branch to production |
| metamorfosis-wellness-journey | client-delivery | no | Verify CI; consolidate wellness family |
| newworldkids | client-delivery | yes | Fix 5 s TTFB; consolidate multi-cloud configs |
| nexusgymcdmx | client-delivery | no | Verify live status with client |
| postateesstudio- | client-delivery | yes | Treat as the single canonical Postatees studio repo; consolidate VIPposta's code into this one and archive the others. |
| preeway-pressure-washing | client-delivery | no | Verify live URL; connect client domain |
| pv-construction-platform | client-delivery | no | Ship Vercel deploy; verify live link |
| seattle-reuse-exchange | client-delivery | no | Check Vercel/Encore Cloud dashboards for an actual live URL; looks like one of the most mission-ready products in the se |
| social-media-template | client-delivery | no | Point at self-hosted Postiz (handoff S4); first Facebook Page proof |
| sweet-psilocybe-landing | client-delivery | no | Rotate exposed key, scrub README, then deploy |
| tasteofnawlins | client-delivery | no | Confirm client and deploy target; finish site |
| tecitodelaverdad | client-delivery | no | Deploy and confirm client domain |
| the-minority-report | client-delivery | no | Confirm client relationship with New World Kids; check for a live deployment target. |
| tierra-sagrada | client-delivery | yes | Independently verify the URL resolves and confirm current owner/client relationship. |
| tonmay-productions | client-delivery | no | Build out and deploy; treat as the canonical repo for the tonmay-* pair. |
| trades-landing-template- | client-delivery | no | Keep as trades template for quick-win clients |
| UJIMA | client-delivery | yes | Verify live URL; pick one deploy target |
| v0-leonradio-website | client-delivery | no | Verify the actual public URL before treating as a deployed client asset. |
| veronika-mvp-final | client-delivery | yes | Independently verify the live domain resolves and mark it fully confirmed. |
| allweatherroofs | quick-revenue | no | Quick-win offer: HTTPS on-site repair-request form + h1 (see quickwins) |
| asce3nd-interactive-document | quick-revenue | yes | Add CTA/inquiry path; reuse as productized workbook offer |
| dispatchhelper | quick-revenue | no | Verify Supabase live; demo URL before pitching |
| goatalliance | quick-revenue | no | Clarify current hosting status and whether the Lovable Cloud migration happened. |
| la-silueta | quick-revenue | yes | Quick win: restore Vercel billing/project or redeploy; confirm client |
| maxx-craft | quick-revenue | no | Confirm deploys; package as WP-migration service |
| Open-clipz | quick-revenue | no | Assess whether the video-editor UI is close enough to finish and ship as a standalone tool. |
| speedtolead | quick-revenue | no | Pair with low-hanging-fruit offer; verify deploy |
| text-new-world-kids-lowrider-bike | quick-revenue | no | Confirm the auction is still active and get the live campaign URL; otherwise archive as a completed one-off. |

## Method and limits

Each repo: root listing, README (≤80 lines), one manifest, last commit, deploy-config presence. README claims were recorded as `builds-claimed`, never as deployed. Nine live URLs were probed by Fable with a read-only inquiry-path checker on 2026-09-06; everything else is source-evidence only. District assignment is a proposal; owner may reassign. No revenue, customer or partnership is claimed anywhere in this file.

