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
