# Quiz results page: brand settings

Your quiz's page code includes the results page settings (Quiz builder › **Results** tab), but not the results page's own layout code. So for now, set the brand through these built-in settings. They are reliable, and GoHighLevel applies them itself. Once I have the results page code (see the bottom of this file), I'll add the matching CSS to `ghl-quiz.css`. The quiz and its results share the same Custom CSS box.

| Section | Setting | Now | Change to |
|---|---|---|---|
| Layout | Background | #FFFFFF | #FFFFFF (keep) |
| Header | Heading text "Your Marketing Score" | 32px, sans-serif, #250762 | Poppins, Bold, **#282060** |
| Overall score | Background | #FFFFFF | #FFFFFF (keep) |
| Overall score | Text "Your journey to long-term digital success starts here!" | #250762 | **#282060** |
| Category scores | Section background | #4B9DD6 | **#282060** (purple band, like the website's "How it works") |
| Category scores | Category card background | #FFFFFF | #FFFFFF (keep) |
| Call to action | Background | #250762 | **#282060** |
| Call to action | Button colour / text | #4B9DD6 / white | **#3299D5** / white |
| Footer | Text and icons | default | **#282060** |
| Score tiers | Low / Medium / High colours | #F04438 / #F79009 / #12B76A | Keep. Red, amber and green read instantly as poor, OK and good. |

Fonts: wherever the results editor offers a font, pick **Poppins** for headings and **Inter** for body text.

## Problems found in the quiz settings (worth fixing now)

1. **The results button goes to a placeholder for most people.**
   - For Low scores, the call-to-action button goes to the Blueprint store page.
   - For Medium and High scores, it goes to `www.example.com`, as does the "overall" button.
   - The button text is "Subscribe" in some places and "Purchase the First Search Marketing Blueprint" in others.
2. **Leftover chiropractor template text:**
   - The Low-tier CTA says "…what it means for your **posture and spinal health**".
   - The auto-responder subject is "**Chiropractor Assessment**".
   - The quiz name still includes "Chiropractor Assessment Quiz".
3. **Hidden stray text:** the FirstBrand "Medium" result ends with white text that reads "k you for taking the time to complete this quiz.". It's invisible on white, but screen readers and the PDF results will show it.
4. **Mismatched contact field names.** The questions save into contact fields named after old questions (for example, the brand identity question saves to "do_you_experience_back_pain…"). Answers are stored correctly, but contact records and reports will show the wrong question names. Rename the fields under Settings › Custom Fields.

## To finish the results page CSS

Complete the quiz once so the results page shows. Then right-click the page, choose **Inspect**, right-click the top `<html>` line, choose **Copy › Copy outerHTML**, paste it into a text file and upload it.
