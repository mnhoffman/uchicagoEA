# UChicago Effective Altruism — static site

A dependency-free static clone of [uchicagoea.org](https://uchicagoea.org) (originally
built on Squarespace), rebuilt as plain HTML/CSS/JS with all images stored locally.

## Run it

```sh
python3 -m http.server 8734
# then open http://localhost:8734
```

Any static file server works; there is no build step.

## Structure

```
index.html                      Home
about-us/index.html             About Us → UChicago EA (leadership)
about-ea/index.html             About Us → Effective Altruism
intro-fellowship/index.html     Programs → Intro Fellowship
impact-research-groups/index.html
longtermist-reading-group/index.html
contact-us/index.html           Contact (embedded Airtable form)
css/styles.css                  Single shared stylesheet (theme + layout)
js/main.js                      Mobile nav toggle + alumni carousel arrows
assets/images/                  All site images (downloaded from the live site)
assets/favicon.ico
```

## Notes

- **Theme**: colors and type were measured from the live site — accent
  `hsl(189 82% 31%)`, dark accent `hsl(196 58% 25%)`, light accent
  `hsl(184 100% 80%)`; Raleway headings, Merriweather body, Inter Tight buttons.
  Section color schemes mirror Squarespace's themes via the `theme-*` classes
  in `css/styles.css`.
- **Fonts** load from Google Fonts (the only external asset besides the two
  embeds below).
- **Embeds**: the contact form is the live Airtable form
  (`airtable.com/embed/shrmD16AfIWEnvJln`); the About EA page embeds the same
  YouTube video as the original.
- Pages are plain hand-editable HTML — edit content directly in each
  `index.html`.

## Dormant links (not published on the site)

Removed from the site because the club does not actively check them;
kept here in case they come back:

- Slack invite: https://uchicago-ea.slack.com/join/shared_invite/zt-vnp07uq8-zHu8N4hCVEWGdpr_CpUCvg#/shared-invite/email
- Instagram: https://www.instagram.com/uchicago.ea/
- Old Airtable contact form (was embedded on the contact page): https://airtable.com/embed/shrmD16AfIWEnvJln

## Website editor (uchicagoea.org/edit/)

A board-only, in-browser editor for quick text edits. Behind the same
password gate as the board page; publishing additionally requires each
editor's own GitHub personal access token (classic, repo scope) for an
account with collaborator access, stored only in their browser. Saves
commit straight to main, which deploys the site. Source lives in
`board-src/edit.html` (gitignored) and is encrypted by the same script
as the board page.

## Board page (uchicagoea.org/board/)

A password-protected page for board members. The published file
(`board/index.html`) contains only AES-256-GCM-encrypted content; it is
unlocked in the browser with the shared board password. The page is not
linked from the site, not in the sitemap, and marked noindex.

- The plaintext source lives in `board-src/board.html` (gitignored, local
  only). The current content can always be recovered by unlocking the
  live page in a browser.
- To edit the page: update `board-src/board.html`, then run
  `python3 tools/encrypt_board_page.py` (it prompts for the password)
  and commit the regenerated `board/index.html`.
- To change the password: run the same script with the new password.
  Anyone with the old password can still read OLD versions from git
  history, so rotate after removing someone's access and don't treat
  the page as a vault; it is for links and low-stakes notes.
