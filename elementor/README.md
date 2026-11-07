# Elementor setup: First Search Marketing

Built so the site matches the approved HTML exactly, **and** stays editable in Elementor:

- **Every widget and section carries its own styling** in its Style and Layout tabs (font size per device, weight, line height, colour, padding, gaps, alignment), measured from the approved HTML. Change any of it in the editor and your change wins.
- **Brand colours are linked to Elementor's four built-in Global Colors**: Primary `#250762`, Secondary `#3299D5`, Text `#1C1B22`, Accent `#174FA2`. Change one in Site Settings › Global Colors and every page updates.
- **The Custom CSS only adds what Elementor can't do natively** (gradient card borders and gradient text, the purple glows, pills and stage logos, FAQ and tab styling, the overlapping buttons). Its colours read from your Global Colors.
- **The templates don't depend on the Site Settings import.** They look right as long as the four Global Colors above are set and the Custom CSS is in place.

## 1. Site Settings

File: `first-search-site-settings.zip` (Elementor Website Kit, current export format 3.0)

**Import it here:** *Elementor › Tools › Import / Export* (in newer versions: *Templates › Website Templates*, or the **Import** button on *Elementor › Website Templates*). Not in *Templates › Saved Templates*: that screen only takes page templates and will reject this file. Choose **Site Settings** when asked what to import.

It sets:
- **Global Colors** and **Global Fonts** (lists below)
- **Typography**: body text Poppins 18px / 1.6, headings Poppins
- **Layout**: content width 1240px, default container padding **0** (no hidden spacing), 20px gaps
- **Background**: page background `#F8F7F7`, as in the HTML
- **Custom CSS**: the contents of `site-settings.css` (needs Elementor Pro)
- **Features**: *Flexbox Container*, *Nested Elements* and *Menu*

**If the import doesn't take, set these four things by hand. That's all the templates need:**
1. *Site Settings › Global Colors*: Primary `#250762`, Secondary `#3299D5`, Text `#1C1B22`, Accent `#174FA2`
2. *Site Settings › Custom CSS*: paste `site-settings.css`
3. *Site Settings › Layout*: Container Padding `0` on all sides
4. *Elementor › Settings › Features*: *Flexbox Container* and *Nested Elements* set to Active

### Global Colors

| Name | Value |
|---|---|
| Primary | `#250762` |
| Secondary | `#3299D5` |
| Text | `#1C1B22` |
| Accent | `#174FA2` |
| Body text | `#2F2E36` |
| Muted text | `#6B6A72` |
| Sky (small text) | `#1F78B4` |
| White | `#FFFFFF` |
| White 92% | `#FFFFFFEB` |
| White 80% | `#FFFFFFCC` |
| White 70% | `#FFFFFFB3` |
| Aqua | `#72CCD8` |
| Light sky (on purple) | `#8FD5EE` |
| Lilac (on purple) | `#D8D6EE` |
| Star gold | `#F4B400` |
| Deep purple | `#1A0446` |
| Page background | `#F8F7F7` |
| Soft grey | `#F4F4F6` |
| Blue tint | `#EEF0F9` |
| Grey | `#D9D8D7` |
| Line | `#E3E2EA` |

### Global Fonts

The 24 most-used text styles from the approved HTML, with their tablet and phone sizes, ready to pick when you build new sections. The templates set these values on each widget directly, so they don't depend on this list.

| Name |
|---|
| Step number · 120px 800 |
| Big number · 86.5px 700 |
| H1 · 72px 700 |
| H2 · 52px 700 |
| Big number label · 29px 400 |
| H3 · 28px 700 |
| Button · 22px 600 |
| Hero lead · 22px 400 |
| FAQ answer · 21px 400 |
| H3 · 21px 700 |
| Body · 20px 400 |
| Button · 20px 500 italic |
| Card title · 20px 700 |
| Eyebrow · 19.5px 600 |
| H3 · 19px 600 |
| Lead · 19px 400 |
| Button · 18px 500 italic |
| Button · 16px 500 italic |
| Card text · 16px 400 |
| FAQ question · 16px 700 |
| H4 · 16px 700 |
| Label · 15.5px 600 |
| List · 15.5px 400 lh 1.45 |
| List · 15.5px 400 lh 1.6 |

## 2. Where to change things later

| To change… | Go to |
|---|---|
| A brand colour everywhere | Site Settings › Global Colors |
| A text style on one widget | That widget › Style tab › Typography |
| A text style for new sections | Pick one of the Global Fonts from the list above |
| One widget's colour or size | That widget › Style tab (unlink the global, or pick another) |
| Spacing above/below a section | The section container › Layout › Padding (per device) |
| Space between items | The container › Layout › Gaps |
| Page background | Site Settings › Background |
| Decorative pieces (gradient borders, pills, glows) | Custom CSS (`site-settings.css`) |

## 3. CSS classes used by the templates

These are already applied in the templates. Add them under **Advanced › CSS Classes** when you build new sections.

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

## 4. Templates (header, footer and 30 pages)

Everything is in `elementor/templates/`. Do the steps in order.

### Step 1: images (automatic)
Every image and background in the templates is hosted in the public GitHub repo, at a fixed version that never changes. When you import a template, Elementor downloads each image into your Media Library and points the page at your own copy. You don't need to upload anything first.
- Each image has a fixed ID, so Elementor imports it **once** and reuses it in every later template. The Media Library doesn't fill up with duplicates.
- If an image still comes in as a grey placeholder, your host is blocking WordPress from downloading files. Ask the host to allow outgoing requests to `raw.githubusercontent.com`. Or upload `elementor/upload/first-search/` to `wp-content/uploads/first-search/` and swap the images in by hand.
- If you imported templates before this change, delete them and import them again to pick up the images.

### Step 2: Site Settings first
Import `first-search-site-settings.zip` (section 1 above) **before** the templates, or set the four things listed there by hand. The templates need *Flexbox Container* switched on, the four Global Colors and the Custom CSS.
If you already imported templates while *Flexbox Container* was off, they were saved empty: delete them and import them again.

### Step 3: import
Go to **Templates › Saved Templates › Import Templates** and import the files one at a time. They are not a zip.

**Site parts**

| File | Where it goes |
|---|---|
| `header.json` | Theme Builder › Header › display on **Entire Site** |
| `footer.json` | Theme Builder › Footer › display on **Entire Site** |

**Main pages** (`pages/`): for each one, create the WordPress page, choose Edit with Elementor, then use the folder icon › My Templates › Insert. When Elementor asks whether to **apply the template's page settings**, choose **Yes**. That sets the page layout to **Elementor Full Width** and hides the WordPress page title, so every section runs edge to edge like the HTML. If you missed the prompt, open the page's settings (gear icon) and set Page Layout to *Elementor Full Width* and turn on *Hide Title*.

> Seeing a grey or white strip down the left and right of the page? That's the theme's boxed page layout. Switch the page to *Elementor Full Width* as described above.

| File | Page | Suggested URL |
|---|---|---|
| `01-home.json` | Home | `/` |
| `02-about-us.json` | About Us | `/about-us/` |
| `03-why-choose-us.json` | Why Choose Us | `/why-choose-us/` |
| `04-services.json` | Services overview | `/services/` |
| `05-events.json` | Events | `/events/` |
| `06-resources.json` | Resources | `/resources/` |
| `07-befirst-training.json` | BeFirst Training | `/befirst-training/` |
| `08-contact-us.json` | Contact Us | `/contact-us/` |

**Service pages** (`services/`): 12 complete pages, each with its own copy, framework wheel, stage tabs, included list, 90-day plan, related services, resources and FAQ. Make each one a child page of Services.

| File | Suggested URL |
|---|---|
| `01-branding-content-creation.json` | `/services/branding-content-creation/` |
| `02-website.json` | `/services/website/` |
| `03-analytics.json` | `/services/analytics/` |
| `04-crm.json` | `/services/crm/` |
| `05-seo.json` | `/services/seo/` |
| `06-advertising.json` | `/services/advertising/` |
| `07-social-media.json` | `/services/social-media/` |
| `08-local-ties.json` | `/services/local-ties/` |
| `09-lead-generation.json` | `/services/lead-generation/` |
| `10-marketing-automation.json` | `/services/marketing-automation/` |
| `11-loyalty.json` | `/services/loyalty/` |
| `12-reviews-referrals.json` | `/services/reviews-referrals/` |

**Framework stage pages** (`framework/`): the four core pillars, each with its own self-check, services and metrics.

| File | Suggested URL |
|---|---|
| `1-firstbrand.json` | `/firstbrand/` |
| `2-firstthought.json` | `/firstthought/` |
| `3-firstchoice.json` | `/firstchoice/` |
| `4-firstreferral.json` | `/firstreferral/` |

**Individual (single) templates** (`singles/`): these are Theme Builder › Single templates. Each holds sample content so you can see the design. Turn the sample text into Dynamic Tags (Post Title, Post Date, Featured Image, custom fields) as you set up each post type.

| File | Display condition | Notes |
|---|---|---|
| `single-blog-post.json` | Posts | **Delete the "Sample article" HTML widget** (class `fs-sample-content`). The Post Content widget above it pulls in the real post. |
| `single-podcast-episode.json` | Podcast post type, or the category Podcast | Paste the episode player embed (Buzzsprout, Spotify) into the placeholder |
| `single-video.json` | Video post type, or the category Video | Set the Video widget to a dynamic YouTube/Vimeo URL field |
| `single-event.json` | Events post type | Countdown, agenda and registration form are included |
| `single-case-study.json` | Case study post type | Results bar chart is an HTML widget, so edit the numbers in it |

If you'd rather use plain pages than Theme Builder for these, insert them into a page the same way as the main pages.

**Location page** (`location/`): `location-page-seo-portsmouth-sample.json` is one service + town page. Make one copy per combination and follow `location-pages-seo-guide.md` in the repo root.

### Step 4: after importing
- **Header menu:** this uses the Menu widget (Elementor Pro 3.16 or later, with the *Menu* feature enabled under Elementor › Settings › Features). The mega-menu panels are built in already. Check the link URLs.
- **Links:** these are placeholders such as `/about-us/`, `/services/seo/`, `/firstbrand/`, `/events/` and `/contact-us/`. Update them to your real slugs.
- **Forms:** the newsletter, contact and event forms are Elementor Pro Form widgets. Set their Actions After Submit (email, webhook to GoHighLevel, and so on).
- **GoHighLevel embeds** (calendar, quiz, podcast player) are HTML widgets with placeholder boxes. Paste your embed code over them, and add the CSS from `/gohighlevel/` in GoHighLevel.
- **Bracketed text** like `[XX]`, `[Client name]` and `[from $X]` marks copy you need to fill in.
- **Resources page:** the Posts and Taxonomy Filter widgets need categories called Blog, Case Study, Podcast and Video, or your own equivalents.

### Rebuilding
`python3 elementor/build/build_all.py` (Python 3, no dependencies) regenerates every template plus `first-search-site-settings.zip`.
- `build/data/proto-styles.json` holds the typography, colours and section spacing measured from the approved HTML at 1440 / 1024 / 390px.
- `build/styler.py` writes those values into the templates as native Elementor settings (colours linked to the four built-in Global Colors) and builds the Global Fonts list for the Site Settings file.
- `elementor/preview/` has HTML renders of every template, used for QA. They mimic Elementor's container defaults, global styles and per-widget settings, but they're not a substitute for checking the real site.
