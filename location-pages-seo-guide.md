# Location pages: SEO and AI-search guide

One template, one page per **service × town** (for example, "SEO in Portsmouth, NH"). The prototype is `location.html`. Use the bar at the top to switch between three examples, show the SEO structure, or view the schema.

## How the location pages avoid competing with your service pages

| | Main service page | Location page |
|---|---|---|
| Targets | "SEO services", "local SEO agency" | "SEO Portsmouth NH", "SEO company near Portsmouth" |
| URL | `/services/seo/` | `/services/seo/portsmouth-nh/` (a child of the service page) |
| H1 and title | SEO Services | SEO Services in Portsmouth, NH |
| Content | Everything about the service | What's different about this service **in this town**, plus a short summary that links up to the main page |
| Schema | Service | Service with `areaServed` = the town, plus BreadcrumbList |

Rules that keep Google from confusing them:
1. **Each page has its own canonical** (itself). Never point a location page's canonical at the service page, or the service page's at a location page.
2. **Don't copy the service page.** The "What's included" section is a six-item summary with a link up. At least 60% of each location page should be unique: local context, the local review, the local case study and local FAQs.
3. **Link both ways.** The service page gets an "Areas we serve" list linking down to each town. Each town page links up (breadcrumb, "About our SEO service", "See everything included"). It also links across to the same service in nearby towns and to other services in the same town.
4. **Only real towns, only real content.** Build a page only where you serve clients and can write something specific. Twenty thin pages that differ only by town name can hurt the whole site.
5. **One address.** The schema and footer use the real Hampton office. Never add a fake or virtual address in a town; it breaks Google's guidelines.

## What makes it AI-search friendly

- **Answer first.** The first paragraph is a 40–60 word direct answer: who, what, where, and why you. AI tools like ChatGPT, Perplexity and Google's AI Overviews tend to quote this kind of passage.
- **Key facts box.** Service, area served, nearest office, pricing, timeline and guarantee as a short labelled list that's easy to extract.
- **Questions as headings.** FAQs are written the way people ask them, with FAQPage schema.
- **Trust signals.** "Reviewed by Chris Mitchell, Owner" plus an updated date (WebPage `reviewedBy` and `dateModified` in the schema), a real local review and real local numbers.
- **Clear entities.** The schema states who provides the service (your business), what it is, where it's offered, and where the page sits in the site.

## Rollout plan

1. Start with your strongest service in the 3–5 towns you already have clients in.
2. Write the local context, FAQs and proof for each one yourself, or have us draft them from client notes. The bracketed placeholders show what each needs.
3. Add the "Areas we serve" links on the service page, and submit the new URLs in Google Search Console.
4. Review in 60–90 days. Expand to more towns or services where pages are getting impressions.

## WordPress build

- A **Location** custom post type with ACF fields (service, town, state, nearby towns, answer summary, key facts, local context, review, case study, FAQ, updated date, reviewer).
- **One** Elementor Theme Builder "Single" template.
- Permalinks set to `/services/{service}/{town-state}/`.
- Schema through Rank Math schema templates (or a small PHP snippet in the template).
- Breadcrumbs through Rank Math, visible on these pages.
