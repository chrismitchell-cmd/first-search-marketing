# GoHighLevel styling for befirstsearch.com

Paste-in CSS that makes GoHighLevel's standard forms, quizzes and calendars match the website. It uses the same colours, fonts, input fields and buttons.

| File | Paste it into |
|---|---|
| `ghl-forms.css` | Sites › Forms › open the form › **Styles** panel › **Custom CSS** |
| `ghl-quiz.css` | Sites › Quizzes (or Surveys) › open it › **Styles** panel › **Custom CSS** (includes the form styles, so paste this one file only) |
| `ghl-calendar.css` | Calendars › Calendar settings › open the calendar › Widget / Customizations › **Custom CSS**. No field there? Put the calendar on a GHL site page and paste it into that page's Settings › Custom CSS. |

## Important

- **Paste the CSS inside GoHighLevel, not into WordPress or Elementor.** Embedded GHL pieces load in an iframe, and CSS on the WordPress page can't reach inside an iframe.
- **Set the basics in GHL's own style settings first:**
  - Background: transparent or white
  - Font: Poppins
  - Button colour: #282060
  - Field corner radius: 12

  The CSS polishes what those settings can't do.
- **On the WordPress page, put the embed inside a gradient-frame card.** Use the same card as the contact page, and give the iframe `width: 100%` and no border.
- GHL changes its class names from time to time. Most rules target plain HTML elements (inputs, buttons, labels), so they keep working. If one piece doesn't change, right-click it, choose **Inspect**, and add its class to the matching rule.
