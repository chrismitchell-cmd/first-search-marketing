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
