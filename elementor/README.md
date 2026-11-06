# Elementor setup: First Search Marketing

## 1. Global Colors (Site Settings › Global Colors)

| Name | Hex | Used for |
|---|---|---|
| Primary | **#250762** | Headings, buttons, purple sections, menu |
| Secondary | #3299D5 | Accent words, eyebrows, links |
| Text | #1C1B22 | Body copy |
| Accent | #174FA2 | Royal blue, gradient end |
| Aqua | #72CCD8 | Gradient start, focus rings, title rules |
| Grey | #D9D8D7 | Dividers |
| Soft grey | #F4F4F6 | Light backgrounds, callout boxes |
| White | #FFFFFF | Cards |

Gradient (for backgrounds that take a gradient): linear, 90°, **#72CCD8 → #174FA2**.

## 2. Global Fonts (Site Settings › Global Fonts)

| Name | Font | Weight |
|---|---|---|
| Primary (headings) | Poppins | 700 |
| Secondary (subheads) | Poppins | 600 |
| Text (body) | Poppins | 400, 18px, line height 1.6 |
| Accent (menu, labels, small UI) | Inter | 500 |

## 3. Custom CSS

Paste `site-settings.css` into **Site Settings › Custom CSS**. Buttons, headings, forms and links are styled automatically. Everything else is an opt-in class, added under a widget's or container's **Advanced › CSS Classes**:

| Class | Add to | What it does |
|---|---|---|
| `fs-dark` | Container | Purple section with soft blue glow; white text; gradient buttons |
| `fs-dark-round` | Container (with `fs-dark`) | Rounded corners on the purple block |
| `fs-grad` | Container | Aqua → blue gradient band (stats, CTA banner) |
| `fs-geo` | Container | Light background colour (set bg-geometric.jpg as its Background image) |
| `fs-section` | Container | Standard section top/bottom spacing |
| `fs-stripe` | Thin Container under the header | Gradient header stripe |
| `fs-gcard` (+ `fs-gcard--thin`, `fs-gcard--hover`) | Container | White card with the gradient border |
| `fs-purple-card` | Container | Purple card with blue corner glow |
| `fs-soft-box` | Container | Light grey rounded box |
| `fs-hero` | Hero row Container | Wide text column, 440px media column |
| `fs-eyebrow` | Heading / Text | Small sky-blue label above a heading |
| `fs-h1-rule` (+ `fs-center`) | H1 Heading | Short aqua rule under the page title |
| `fs-hero-lead` | Text Editor | Hero paragraph size and width |
| `fs-btn-grad` / `fs-btn-white` / `fs-btn-lg` | Button | Gradient / white / large button |
| `fs-link-u` | Button | Italic underlined text link (secondary action) |
| `fs-tile` | Icon Box / Image Box | White icon tile with blue glow ring |
| `fs-faq` | Accordion / Toggle | FAQ cards, open question turns purple |
| `fs-nav` | Nav Menu / Mega Menu | Brand menu colours, gradient underline |
| `fs-video` | Video | Gradient frame around the video |
| `fs-img-frame` | Image | Rounded gradient frame |
| `fs-footer` | Footer Container | Purple footer |
| `fs-logo-box` | Image (footer logo) | White glowing box behind the logo |

Inline HTML (inside a Heading or Text Editor):

```html
We put your <span class="fs-gt">business first.</span>      <!-- gradient words -->
We put your <span class="fs-sky">business first.</span>     <!-- sky-blue words -->
<span class="fs-plogo"><b>first</b>brand</span>             <!-- stage logo -->
<span class="fs-plogo fs-plogo--light"><b>first</b>choice</span>  <!-- on purple -->
<span class="fs-pill">Fixed monthly retainer</span>
<span class="fs-type fs-type--blog">Blog</span>              <!-- also --case, --podcast, --video -->
```

## 4. Templates (header, footer and 15 pages)

Everything is in `elementor/templates/`. Do the steps in order.

### Step 1: upload the images first
The templates load their images from
`https://befirstsearch.com/wp-content/uploads/first-search/...`.
Upload the **contents** of `elementor/upload/first-search/` to `wp-content/uploads/first-search/` using SFTP or your host's File Manager. Keep the subfolders.
Do this **before** importing. Elementor copies each image into the Media Library during import. If the files aren't there yet, the images come in blank.

### Step 2: Site Settings
Complete sections 1–3 above (global colors, global fonts, custom CSS) before you import. The templates depend on the `fs-*` classes.

### Step 3: import
Go to **Templates › Saved Templates › Import Templates** and import the files one at a time. They are not a zip.

| File | Type | Where it goes |
|---|---|---|
| `header.json` | Header | Theme Builder › Header › display on **Entire Site** |
| `footer.json` | Footer | Theme Builder › Footer › display on **Entire Site** |
| `pages/01`–`10` | Page | Create the WordPress page, set Template to **Elementor Full Width**, choose Edit with Elementor, then use the folder icon › My Templates › Insert |
| `pages/05` service, `06` framework stage | Page (sample) | Insert into each service or stage page, then swap in that page's copy |
| `pages/11` case study, `13` podcast/video, `14` event | Page (sample) | Use as layouts. Convert to Theme Builder › Single for that post type when you're ready, and replace the text with Dynamic Tags |
| `pages/12-blog-post-single` | Single Post | Theme Builder › Single Post › display on **Posts**. **Delete the "Sample article" HTML widget** (class `fs-sample-content`). It's only there for the design preview. The Post Content widget above it pulls in the real post. |
| `pages/15` location | Page (sample) | One copy per service + town page. Follow `location-pages-seo-guide.md` in the repo root. |

### Step 4: after importing
- **Header menu:** this uses the Menu widget (Elementor Pro 3.16 or later, with the *Menu* feature enabled under Elementor › Settings › Features). The mega-menu panels are built in already. Check the link URLs.
- **Links:** these are placeholders such as `/about-us/`, `/services/seo/`, `/firstbrand/`, `/events/` and `/contact-us/`. Update them to your real slugs.
- **Forms:** the newsletter, contact and event forms are Elementor Pro Form widgets. Set their Actions After Submit (email, webhook to GoHighLevel, and so on).
- **GoHighLevel embeds** (calendar, quiz, podcast player) are HTML widgets with placeholder boxes. Paste your embed code over them, and add the CSS from `/gohighlevel/` in GoHighLevel.
- **Bracketed text** like `[XX]`, `[Client name]` and `[from $X]` marks copy you need to fill in.
- **Resources page:** the Posts and Taxonomy Filter widgets need categories called Blog, Case Study, Podcast and Video, or your own equivalents.

### Rebuilding
The JSON is generated by `elementor/build/build_all.py` (Python 3, no dependencies). `elementor/preview/` contains rough HTML renders I used for visual QA. They are not exactly how Elementor will render.
