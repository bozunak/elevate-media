# Elevate (@ElevatexWealth) — post style guide

Every scheduled run follows this guide exactly. Brian edits it to change the page's rules.

## 0. Read section 7 first
Section 7 holds what the page's own Instagram data says is working. Apply it when choosing the topic, hook style, cover layout and photos — it overrides the general examples below, but never Brian's rules (audience, photo standards, tone, tattoos).

## 1. The page (follow exactly)
- Display name "Elevate", handle @ElevatexWealth. Modeled on @wealth and @explaining: swipeable 5–7 slide carousels (1080x1350), each slide a full-bleed REAL photo on top and a black band at the bottom with the Elevate logo on a gold line and a huge condensed uppercase headline (key words in gold).
- Topics rotate across **wealth, money habits, investing basics, career/income, health & fitness, luxury lifestyle, travel, mindset/discipline, relationships & family, generosity**. Mix evergreen lessons with timely hooks (a current money/market/news story, verified by web search the same day).
- Audience: ages 20–40. Feel: luxury, sexy, aspirational, addictive ("like a digital cigarette") — every slide must make someone stop scrolling and want that life.
- Underlying tone consistent with Christian values (freedom, greatness, peace, love, warmth, strength, faithfulness, generosity, stewardship) WITHOUT preaching, quoting scripture, or calling the page Christian. One warm "heart" slide per post carries this.
- **Cover slide = the hook**, @wealth style: one striking luxury hero photo + optional white-bordered circle cut-in(s) with a white curved arrow, and a curiosity/benefit headline with a specific number or bold claim (e.g. "The $200 habit that made one friend $281,000 richer", "Why rich people in their 20s never buy new cars", "This 10-minute morning routine is worth more than a raise"). Celebrities/icons may be referenced IN TEXT with verified facts (cite the source in your notes) — but NEVER use photos of real celebrities or brand logos as the subject.
- Last slide: share/save/follow call to action with "@ElevatexWealth".

## 2. Photo rules (Brian's explicit standards)
- Only real-looking photos from **Pexels** (free commercial license). Find candidates with WebSearch restricted to pexels.com; the numeric ID is the end of the page URL. Download with:
  `curl -sS -o ID.jpg "https://images.pexels.com/photos/ID/pexels-photo-ID.jpeg?auto=compress&cs=tinysrgb&w=1600"` (skip any result under 1 KB).
- People must be attractive, stylish adult men/women in their **20s–30s**, in luxury or aspirational settings: yachts, villas, infinity pools, rooftops at golden hour, supercars, first class/private jets, sleek apartments, upscale dinners, fit people training at sunrise, elegant outfits, swimwear by a pool or on a yacht.
- REJECT: older or unglamorous people, anyone who could be under 18, ordinary home-office/laptop stock, cheesy wooden-mannequin or piggy-bank props, cartoons/illustrations, anything explicit or provocative (sexy = classy and aspirational, never sexual).
- **NO "sinful-looking" tattoos**: reject anyone with large, crude, dark, occult, sexual or gang-style tattoos, and any neck, chest, face or throat tattoos. Small, tasteful tattoos are fine; when in doubt, pick someone with no visible tattoos. Zoom in to check before using a photo.
- ALWAYS look at every candidate before using it: build a contact sheet with PIL and open it with the Read tool. Pick the most striking image per slide; don't reuse the same photo twice in a post.

## 3. Writing rules
- Plain English, confident and energetic, short punchy lines. Headline ≤ 12 words. Sub-text ≤ 25 words.
- Every number must be real: verify facts with web search, run any math in Python. Hypothetical examples must say so on the last slide's footnote.
- Education only: no individualized investment advice, no specific buy/sell calls, no guarantees, no promises of returns. Money posts that show returns need a footnote like "Hypothetical example... Not a guarantee of future results. Education only, not investment advice."
- Caption: hook line with 1–2 emojis → 3–5 short paragraphs with specifics → "Follow @ElevatexWealth to rise a little every time you open Instagram." → disclaimer line if money/returns are mentioned → 5–8 relevant hashtags (always include #Elevate).

## 4. Avoid repeats
Read `posts/log.jsonl` in this repository (one JSON line per post: date, slot, topic, hook, pexels_ids). Pick a topic, hook and photos that differ from the last 60 entries, and never reuse a Pexels ID from the last 30 days. When publishing (section 6, step 2), append this post's line to `posts/log.jsonl` in the same commit.

## 5. Build the slides
Write a `spec.json`, then run `python3 /home/claude/elevate-media/elevate_render.py spec.json out` (work in a scratch folder outside the repo). It renders 1080x1350 PNGs with the house style (Anton/Inter fonts are fetched from raw.githubusercontent.com; Chromium is available through Playwright). Headline gold words go in [[double brackets]]. Typical layout: cover photo_h 880 and size ~100; content slides photo_h 800–840, size 80–84; use `split` for two-person comparisons, `stats` for number overlays, `pills` for labels, `circle` + `arrow` on the cover. After rendering, open a combined preview of all slides with the Read tool and fix anything that looks off (cropped faces, unreadable text, weak cover) before publishing.

The renderer is `elevate_render.py` in this repository; run it from the repo folder.


## 6. Publish (fully automatic — Brian has pre-approved every post; never wait for review)
1. Convert each PNG to RGB JPEG (quality 92), named `elevate-<YYYYMMDD>-<slot>-<n>.jpg`, in slide order.
2. Copy them into `/home/claude/elevate-media/posts/<YYYY-MM-DD>-<slot>/`, then: `git -C /home/claude/elevate-media pull --rebase origin main`, commit with `-c user.name="Elevate Bot" -c user.email="bozunak@users.noreply.github.com"`, and `git push origin HEAD:main`.
3. Check every `https://raw.githubusercontent.com/bozunak/elevate-media/main/posts/<YYYY-MM-DD>-<slot>/<file>` returns HTTP 200 with content-type image/jpeg (retry every 15 s for up to 3 minutes).
4. Publish with the Windsor.ai connector (load its tools with ToolSearch "windsor"): `execute_action` with connector `instagram`, action `create_carousel_post`, account `17841433578299003`, params `{"image_urls": [...in slide order...], "caption": "..."}` (2–10 images, caption ≤ 2,200 characters).
5. If the push or the publish fails, retry once. If it still fails, send Brian the PNGs (SendUserFile, in order) plus the caption and the error (SendUserMessage) so he can post it manually in Meta Business Suite.
6. On success, send Brian one short SendUserMessage: "Posted ✅ <slot>: <cover hook>" with the media id. Finish with a 2-line summary: topic, hook, published or not.

## 7. What's working (auto-updated by the daily growth review — do not edit by hand)
_Not enough data yet (fewer than 10 posts with 48+ hours of insights). Until then, rotate topics and cover styles evenly so the review can compare them._
