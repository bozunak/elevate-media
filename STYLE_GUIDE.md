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

## 8. Reels (used by every Reel run; how many run per day is set in section 10)
Reels are how the page reaches non-followers, so each Reel is its OWN idea made for video — not a slideshow of a carousel.
1. Idea: pick a topic/hook from section 1's rotation (and section 7's learnings) that suits motion: a bold claim, a fast list, a "most people vs. the rich" contrast, a surprising number. Check `posts/log.jsonl` so it doesn't repeat a recent carousel or Reel hook — including Reels already posted earlier today (each same-day Reel must use a different topic category and different footage). Lean on section 9's emotional one-liner hooks (purpose, ambition, comebacks, family, peace) as well as money and luxury hooks. Verify every fact and number (web search, Python) exactly as for carousels.
2. Script: 4–6 scenes, 1.8–3.5 s each, 10–15 s total. Scene 1 = the hook, on screen from frame one, ≤ 8 words. Middle scenes = 1 short line each (≤ 10 words) that builds tension or gives the steps. Last scene = the payoff + "Follow @ElevatexWealth", written so the loop back to the hook feels natural.
3. Footage: real Pexels stock VIDEO that matches the photo rules in section 2 (young attractive adults 20s–30s, luxury, classy, no sinful-looking tattoos, nothing explicit, no visible brand logos as the subject): yachts, supercars, villas, infinity pools, rooftops, first class, sunrise workouts, city skylines at night. Find candidates with WebSearch restricted to pexels.com ("pexels video …"); the id is the number at the end of the pexels.com/video/... URL. Download with `python3 /home/claude/elevate-media/pexels_video.py ID clip.mp4 [--vertical]` (some newer ids aren't downloadable — just try others). Grab a frame from each clip with ffmpeg and look at it with the Read tool before using it. Prefer vertical (9:16) clips and clips with movement; use a different clip per scene where possible.
4. Build: write a spec (see the header of `elevate_reel_v2.py`) and run `python3 /home/claude/elevate-media/elevate_reel_v2.py spec.json out.mp4`. Gold words go in [[double brackets]]. Then grab 3–4 frames with ffmpeg, combine them into one preview, and look at it with the Read tool: text readable, not covering faces, footage on-brand. Fix and re-render if needed. If footage can't be found at all, fall back to `elevate_reel.py` with the most recent carousel's slides.
4b. COVER (Brian's rule: every Reel cover must be great, enticing and luxury — never black, blank or a random frame). Add a `"cover"` entry to the spec choosing the single most luxurious, sharpest, best-lit moment of the footage (yacht at sunset, supercar, villa pool, attractive couple dressed up, skyline at night) and the hook as cover text (≤ 8 words, 1–2 gold words). The builder writes `<out>_cover.jpg`. Look at it with the Read tool: photo bright and appealing, people meet section 2's rules, text readable and inside the middle of the frame. If it isn't stunning, pick another moment or clip and rebuild the cover.
5. Save as `reels/<YYYY-MM-DD>-<slot>.mp4` plus `reels/<YYYY-MM-DD>-<slot>_cover.jpg` (slot = r1…r5, given by the run), append a line to `posts/log.jsonl` ({date, slot:"<slot>", topic, hook, pexels_video_ids, reel_media_id}), commit and push (pull --rebase first).
6. Publish with Windsor.ai `execute_action`: connector `instagram`, action `create_video_post`, account `17841433578299003`, params `{"video_url": URL, "caption": <hook line + 2–4 short lines with the specifics + "Follow @ElevatexWealth for more" + disclaimer line if money returns are shown + 5–8 hashtags incl. #Elevate #reels>, "share_to_feed": true, "cover_url": "https://raw.githubusercontent.com/bozunak/elevate-media/<commit sha>/reels/<YYYY-MM-DD>-<slot>_cover.jpg"}` (use the full commit sha, not main — main can 404 for a few minutes after a push; check it returns 200 image/jpeg first; always send cover_url, never thumb_offset).
   - URL to try first: `https://cdn.jsdelivr.net/gh/bozunak/elevate-media@<commit sha>/reels/<file>.mp4` (serves video/mp4). If Instagram rejects it, retry once with `https://raw.githubusercontent.com/bozunak/elevate-media/main/reels/<file>.mp4`.
   - If both fail, send Brian the MP4 and caption (SendUserFile + SendUserMessage) with the error.
7. On success send Brian one short message: "Reel posted ✅ <hook>" with the media id.

## 9. Inspiration pages (Brian adds to this list)
Study these pages' patterns — topics, hook formulas, cover layouts, pacing — never copy their wording, images or graphics, and re-verify any fact they state.
- @wealth — pop-culture + money curiosity hooks, celebrity/luxury news angles, yellow headline band, circle cut-ins with arrows, 3–5 paragraph factual captions.
- @explaining — "Explaining everything": surprising facts about everyday things, white headline with lime key words, very short punchy covers.

### Data notes (from Windsor instagram_public; refreshed weekly by the inspiration review)
_Last update 2026-11-11 — last 30 days, ~500 posts per page._
- **Reels dominate.** @wealth posts ~16/day, ~98% Reels; median Reel ≈ 363K likes vs ≈ 25K for carousels (about 14×). @explaining's carousels hold up better (median ≈ 18K vs ≈ 5K for Reels), but its biggest hits (500K–900K) are still Reels.
- **@wealth's top hooks are one-sentence emotional truths, not money facts:** pressure/ambition ("Nobody feels pressure on the couch…"), comeback ("Your story isn't over just because one chapter went wrong"), "one decision" framing, family/parents ("One day you'd give anything to see your parents' name light up your phone"), and people/boundaries ("Some people will never water your life…"). These pull 4–6M likes.
- **Caption formula (both pages):** bold one-line hook with two emojis → short 1–2 sentence paragraphs that widen the lesson → a closing "maxim" line → "Follow ➡️ … every time you open Instagram" → 3–5 hashtags. Often there's a balancing line ("not guaranteed", "doesn't mean…") that keeps it credible.
- **Money posts that work** frame a concept as a life lesson: compound interest, costly vs expensive, multiple income streams, earning vs owning, generational wealth.
- **@explaining's winners** are awe/nature/science moments and underdog stories (rejected 11 times → astronaut).
- **Apply to Elevate:** lean the Reel hooks toward @wealth's emotional-truth one-liners (fits our faith-warm tone: purpose, family, perseverance, peace); keep luxury visuals. Carousels stay for money lessons and luxury listicles.


## 10. Posting cadence (Brian lets the growth review tune this — only the growth review edits it)
Brian wants @wealth-style volume, with Reels as the main engine, and has handed the decision on how many posts to run per day to the growth data. Each scheduled Reel run reads the line below and posts only if its slot is listed; otherwise it ends immediately and silently.

ACTIVE_REEL_SLOTS: r2, r3, r4

Slots (ET post time): r1 10:00 AM · r2 1:30 PM · r3 4:30 PM · r4 9:00 PM · r5 11:00 PM. Carousels stay at am 7:30 AM and pm 7:00 PM daily, plus mid 12:45 PM on weekends/holidays.

Rules for the growth review (Sundays only, at most one change per week):
- Start: 3 Reels/day (r2, r3, r4). Never fewer than 2, never more than 5.
- Add one slot (in order r1, then r5) when, over the last 7 days, the median non-follower reach per Reel is no more than 20% below the week before AND followers grew. More volume only pays if each Reel still gets shown.
- Remove the most recently added slot when the median reach per Reel fell more than 30% in the week after an increase, or the account lost followers.
- If Reels keep beating carousels by 3x+ on follows or non-follower reach for 2 weeks, recommend (to Brian) swapping a carousel slot for a Reel; don't change the carousel schedule yourself.
- If the data says more than 5 Reels a day would help, say so to Brian.
- Log each change here as one line: date, old → new, the numbers behind it.

Change log:
- 2026-11-11: start at 3 Reels/day (Brian approved scaling toward @wealth's volume, decided by data).
