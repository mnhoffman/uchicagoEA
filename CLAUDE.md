# uchicagoea.org — working notes for Claude

Static site for UChicago Effective Altruism. No framework, no build step:
hand-written HTML + one shared stylesheet, hosted free on GitHub Pages.

## Deploying

- Repo: github.com/mnhoffman/uchicagoEA. **Pages deploys from `main`** —
  commit on `main`, `git push origin main`, live in ~1 minute.
- `clone-uchicagoea-website` is a legacy branch (old default). Ignore it.
  If GitHub still shows it as default, switching the default to `main` in
  repo settings is a long-standing TODO.
- The Pages "deploy" step occasionally fails transiently (build succeeds,
  deploy fails; owner gets an email). Fix: `git commit --allow-empty` and
  push again; may take 2-3 tries.
- **Verify deploys by fetching live content and checking for the actual
  change** (grep for a new string, or for encrypted pages compare the
  `CT = "..."` ciphertext against the local file). HTTP 200 or "no
  plaintext leaked" checks pass for stale versions too — this has caused
  false "it's live" claims twice.
- CDN/browser cache up to ~10 min; `?nc=<timestamp>` to bypass when
  checking; users may need a hard refresh after HTML changes.

## Design system ("editorial")

- Fonts: **Fraunces** (serif, headings; bold `<em>` inside h1-h3 renders
  as bold teal accent words — the site's signature) and **Nunito Sans**
  (everything else). Loaded per-page from Google Fonts.
- Palette: teal `#0E7C90` (accent), navy `hsl(199,55%,17%)` (buttons,
  dark bands), dark teal `#1B5165`, light aqua `#99F8FF`, cream
  `#F9F6F0` (page background), ink `#19272E`, soft ink `#45565E`,
  orange `#DB6424` (small labels only). Brand one-pager:
  `../UChicago-EA-Brand-Reference.pdf` (regenerate: ask, script was in a
  past session's scratchpad; easy to rebuild from these values).
- Wave motif: layered parallel strands in three teals — big diagonal
  ribbon on the home hero, horizontal "crest" behind interior page-hero
  titles, sweep at the home footer. Inline SVG per page.
- One stylesheet: `css/styles.css`, referenced as `styles.css?v=N`.
  **Bump the version query on every page whenever CSS changes** (cache
  busting; currently v=9).
- Conventions: no em dashes anywhere; buttons are rounded squares
  (10px); "navy band" sections are `class="sec theme-bright"
  style="background:hsl(199, 55%, 17%)"` (theme-bright supplies white
  text and white buttons); compact bands get inline padding ~2.4-2.6rem.
- New program pages: clone `reading-groups/index.html` (simple) or
  `midwest-retreat/index.html` (with hero image + glance row), then fix
  title/metas/canonical/active-states. Checklist: add the link to BOTH
  the header `ed-nav` dropdown AND the mobile `sidebar` on **every**
  page (2 occurrences each), plus `sitemap.xml`.
- Nav: Home · About Us (Our People, The Broader Movement, Contact) ·
  Programs (Intro Fellowship, Reading Groups, Midwest EA Retreat,
  Impact Fund, Collaborations) · Events · header button. Collaborations
  (/collaborations/) hubs Catalyst, Retreats & Conferences, EA Journal.
- People page (about-us): Leadership grid, Advisors, navy join bar,
  Alumni carousel. Mayank's card exists but is `hidden`. New photos:
  `sips -Z 900 -s format jpeg -s formatOptions 85 in --out
  assets/images/name.jpg`; circle-crop tuning via inline
  `object-position` or `transform:scale() / transform-origin`.

## Encrypted board pages (/board/ and /edit/)

- Published files contain only AES-256-GCM ciphertext; the gate decrypts
  in-browser with the shared board password. Source lives in
  `board-src/` (**gitignored, local-only**); regenerate with
  `python3 tools/encrypt_board_page.py --password-file
  ../board-page-password.txt` (password file lives OUTSIDE the repo).
- `/edit/` is a no-code website editor: renders the real page in an
  iframe canvas, click-to-type on text nodes, link-URL bubble, preview,
  publish via GitHub contents API using each editor's own PAT (classic,
  repo scope, collaborator account, stored in their browser).
- **Editor-published commits reformat whole files** (DOMParser →
  serialize normalizes entities/attributes). Expect noisy diffs and
  stale string anchors: always `git pull` and re-read current file
  content before scripted edits. Editors sometimes leave empty tags
  (e.g. `<p><strong></strong></p>`) — clean when touching those files.
- The gate re-executes `<script>` tags after decrypting (needed by the
  editor). Test gated pages with a throwaway password copy; `?demo=1`
  on /edit/ loads sample content without a token.

## Recurring content flows

- Fellowship open/close toggle: header button on all pages ("Apply now"
  ↔ "Get involved" → reading-groups), home hero + "Join us this
  quarter" section (heading always says THIS quarter), fellowship page
  hero/metas/apply card. Interest form (Google) collects notify +
  deferral requests between rounds.
- Club Google Calendar (embedded on /events/, connector available):
  calendar id `6f85f9b4...aa528b7@group.calendar.google.com` ("UChicago
  EA" in her list). Events panel shows it live. The Autumn fellowship
  series has had instances accidentally deleted before (Oct 26, Nov 2
  were re-created as one-offs).
- Local preview: `.claude/launch.json` in the PARENT folder defines
  "site-preview" (python http.server, port 8124, serving this repo).
  Playwright `browser_run_code_unsafe` + screenshots for visual checks.

## Context

- Owner: Madeleine Hoffman (co-president). Non-technical board edits go
  through /edit/. Domain stays registered at Squarespace (~$20/yr,
  DNS → GitHub Pages IPs; keep auto-renew + valid card). Squarespace
  website subscription cancelled (expires Oct 2026 billing end).
- Old retired URLs have meta-refresh redirect stubs
  (/home, /impact-research-groups, /longtermist-reading-group).
- Footer links: Email · Listserv · Google Calendar only. Dormant
  Slack/Instagram links parked in README ("Dormant links").
