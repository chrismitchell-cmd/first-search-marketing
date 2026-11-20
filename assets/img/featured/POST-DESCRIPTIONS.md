# Featured images and descriptions for posts

All images are 1600 × 900 WebP, matching the Resources card shape.
Each category has its own background so the type is clear on the grid:

| Category | Background | Base colour |
|---|---|---|
| Case studies | Brand purple | `#250762` |
| Blog | Royal blue | `#0A2670` |
| Videos | Deep teal | `#043A4E` |
| Podcast | Midnight | `#0A0E1E` |

Regenerate the images or make new ones with
`elementor/build/assets_src/featured_images.py`. For a new podcast
episode, call `podcast(label=..., white=[...], grad=[...], name=...)` at
the bottom of the script.

**Where each field goes in WordPress:**

- **Featured image:** Post editor, right sidebar, *Featured image*.
- **Alt text:** Media Library, select the image, *Alternative Text*.
- **Excerpt:** Post editor, right sidebar, *Excerpt*. This is the text shown on the Resources card.
- **SEO title and meta description:** Your SEO plugin box (Yoast or Rank Math), below the editor.

---

## 1. Case study: Progressive Dental Care

**Featured image:** `featured-progressive-dental-care.webp`

**Alt text:**
Progressive Dental Care case study by First Search Marketing. From 12 to 100+ leads a month, #17 to #2 in the map pack, 75 to 239 reviews.

**Excerpt (Resources card):**
How a South Portland, ME dental practice went from 12 to 100+ digital leads a month after a rebrand, a new website and a full marketing system, while climbing from #17 to #2 in the Google map pack.

**SEO title:**
Progressive Dental Care Case Study | 8x More Leads | First Search Marketing

**Meta description (about 155 characters):**
See how Progressive Dental Care grew from 12 to 100+ leads a month, jumped from #17 to #2 in the map pack and reached 239 Google reviews.

---

## 2. Blog: Top 2027 marketing trends to scale your business

**Featured image:** `featured-top-2027-marketing-trends.webp`

**Alt text:**
Chris Mitchell in front of the First Search framework wheel. Top 2027 marketing trends to scale your business.

**Excerpt (Resources card):**
Seven marketing trends that will matter most in 2027, from AI answers and the map pack to short video and speed to lead, and how to turn them into one system that grows your business.

**SEO title:**
Top 2027 Marketing Trends to Scale Your Business | First Search Marketing

**Meta description:**
Seven 2027 marketing trends for growing businesses: AI search, the map pack, short video, speed to lead, owned audiences and referrals, plus where to start.

---

## 3. Video: First Search Marketing in two minutes

**Featured image:** `featured-first-search-in-two-minutes.webp`

**Alt text:**
Chris Mitchell in front of the First Search framework wheel. First Search Marketing in two minutes, video.

**Excerpt (Resources card):**
Everything First Search Marketing does in two minutes: our agency, coaching and training paths, the four-stage framework, and the beliefs and values behind how we work.

**SEO title:**
First Search Marketing in Two Minutes | Video

**Meta description:**
A quick two-minute look at First Search Marketing: agency, coaching and training, our firstbrand-to-firstreferral framework, and the values behind it.

---

## 4. Podcast (template for future episodes)

**Featured image:** `featured-podcast-template.webp`. It's a placeholder: set the episode number and title in the script and re-run it for each episode.

**Alt text pattern:**
First Search Marketing podcast, episode [number]: [episode title].

**Excerpt pattern:**
In episode [number], [host] and [guest] talk about [topic] and [the one takeaway listeners can use this week].
