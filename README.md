# befirstsearch.com homepage mockup

A high-fidelity, single-file mockup of the new First Search Marketing homepage, built for internal review. Open `index.html` in a browser. The CSS and JS are inline; images live in `assets/img/`.

Use the **Highlight placeholders** button (bottom-left) to see everything that still needs real content. Placeholder links show a short "Mockup:" message instead of navigating.

## Sections
1. Hero with the typing "search everywhere" demo
2. Trust strip
3. The problem (static)
4. The FirstSearch Framework: interactive wheel and panel (the signature section)
5. FirstSearch Guarantee, stats and stories
6. How it works
7. Two ways to work with us
8. FAQ (with FAQPage JSON-LD)
9. Final CTA
10. Footer

The design plan (tokens, type scale, section layouts) is the HTML comment at the top of `index.html`.

## Notes from the build
- `--blue` (#2E98D4) is 3.2:1 on white, so it's only used for large type, icons and graphics. Small text, links and the active framework segment use `--blue-ink` (#1D78B0, 4.8:1) to meet WCAG AA.
- The logo and Chris's photo are extracted from the Welcome Kit PDF. Replace them with originals (`logo.svg`, a proper headshot) before launch.
- All stats, the guarantee wording, prices, the spots counter and the case study are sample values marked as placeholders.
