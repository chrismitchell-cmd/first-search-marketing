# First Search Marketing — Homepage Redesign

A static, responsive rebuild of the befirstsearch.com homepage. It keeps the current page's section order and copy and applies the new brand system from the 2026 Welcome Kit and the social/ad graphics.

Open `index.html` in a browser to preview it. Full-page screenshots are in `docs/`.

## Section flow (same as the live site)
1. Header: About · Services ▾ · Why Choose Us · Contact · **Free 30-Min Consultation**
2. Hero: *First Search Marketing LLC. / Digital Marketing Agency* + **Schedule Free 1-Hour Consultation**
3. Benefits: More Awareness · More Web Traffic · More Customers
4. Services: "What We Do… SEO" typewriter + 6 service cards
5. About: "What's it like having us as your digital marketing agency?"
6. Stats: 250+ projects · 65+ clients · 12+ years
7. Three Ways We Can Work With You (expanding panels)
8. Why Choose Us: ROI · Family Owned · Local Business
9. Testimonials
10. Highlights band + footer (newsletter, services, contact)

## Brand elements applied
| Element | Source |
|---|---|
| Colours: indigo `#250762`, sky `#3299D5`, cyan `#5ADCE4`, royal `#034EAF` | Sampled from the Welcome Kit |
| Heavy uppercase Poppins headlines with a blue→indigo gradient and soft shadow | Kit page titles |
| Gradient stripe across the top of the page | Top of every kit page |
| "In Front Of The Right PEOPLE \| On The Right CHANNEL \| At The Right TIME" band | Kit cover |
| Team lineup in the hero, team cards with titles | Kit cover and Meet the Team page |
| Cyan→blue gradient outlines on cards, gradient pill buttons, indigo icon tiles | Kit cards and buttons |
| FirstSearch Framework wheel | Kit Framework page |
| Dark indigo sections with blue glow and a faint grid | Social/ad graphics |

All tokens live at the top of `assets/css/styles.css`.

## Before going live
- **Links**: service and page URLs (`/services/seo/`, `/about/`, `/contact/`, …) are assumed. Match them to the real slugs.
- **Social icons** in the footer point to `#`. Add the Facebook, Instagram and LinkedIn URLs.
- **Newsletter form** has `action="#"`. Connect it to the current email/CRM endpoint.
- **Testimonials** are static copies of the visible Trustindex reviews. Replace them with the Trustindex widget embed to keep them in sync.
- **Images** were extracted from the Welcome Kit PDF. Swap in the original logo (SVG) and photo files for the sharpest result.
