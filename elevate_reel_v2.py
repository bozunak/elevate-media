#!/usr/bin/env python3
"""Elevate native Reel builder (v2): real stock footage + bold on-screen text.

Usage: python3 elevate_reel_v2.py spec.json OUT.mp4

spec.json:
{
  "scenes": [                      # 4-6 scenes, 1.8-3.5 s each, ~10-15 s total
    {"clip": "a.mp4", "start": 2.0, "dur": 2.2,
     "text": "Rich people in their 20s [[never]] do this", "size": 104, "pos": "center"},
    ...
  ],
  "music": "optional/path.mp3"      # else a random track from music/ in this repo, else silent
}
Text: wrap gold words in [[double brackets]]. pos: "center" (default), "upper" or "lower".
The first scene is the hook (show it immediately; keep it <= 8 words). The last scene should be
the payoff + "Follow @ElevatexWealth" so the loop invites a rewatch.
"""
import json, os, sys, subprocess, tempfile, random, glob, re, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
GOLD, WHITE = (242, 184, 75), (255, 255, 255)
FONT = os.path.expanduser("~/.elevate_fonts/Anton-Regular.ttf")
INTER = os.path.expanduser("~/.elevate_fonts/Inter.ttf")


def ensure_fonts():
    import urllib.request
    os.makedirs(os.path.dirname(FONT), exist_ok=True)
    for path, url in [(FONT, "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf"),
                      (INTER, "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf")]:
        if not os.path.exists(path) or os.path.getsize(path) < 10000:
            urllib.request.urlretrieve(url, path)


def tokens(text):
    out = []
    for part in re.split(r"(\[\[.+?\]\])", text):
        if not part:
            continue
        gold = part.startswith("[[")
        for w in part.strip("[]").split():
            out.append((w.upper(), gold))
    return out


def overlay(text, size, pos, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(img)
    words, maxw, lines, cur, curw = tokens(text), W - 140, [], [], 0
    space = d.textlength(" ", font=f)
    for w, g in words:
        ww = d.textlength(w, font=f)
        if cur and curw + space + ww > maxw:
            lines.append((cur, curw)); cur, curw = [], 0
        curw += (space if cur else 0) + ww; cur.append((w, g, ww))
    if cur:
        lines.append((cur, curw))
    lh = int(size * 1.08)
    block = lh * len(lines)
    y0 = {"upper": 330, "lower": H - 520 - block}.get(pos, (H - block) // 2 - 60)
    # soft dark band behind the text for readability
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle((0, y0 - 60, W, y0 + block + 60), fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img, band.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img)
    for i, (ln, lw) in enumerate(lines):
        x, y = (W - lw) / 2, y0 + i * lh
        for w, g, ww in ln:
            d.text((x, y), w, font=f, fill=GOLD if g else WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
            x += ww + space
    # brand mark
    fi = ImageFont.truetype(FONT, 40)
    t = "ELEVATE"
    tw = d.textlength(t, font=fi)
    bx, by = (W - tw) / 2 - 28, H - 300
    d.rounded_rectangle((bx, by, bx + tw + 56, by + 66), radius=33, outline=GOLD, width=3, fill=(11, 11, 12, 200))
    d.text((bx + 28, by + 9), t, font=fi, fill=WHITE, spacing=4)
    img.save(path)


def scene(clip, start, dur, ov, out):
    frames = round(dur * FPS)
    vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
          f"eq=brightness=-0.06:saturation=1.08,setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0,"
          f"fade=t=in:st=0:d=0.15,fade=t=out:st={dur-0.15:.2f}:d=0.15,format=yuv420p[o]")
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", f"{dur+0.5:.2f}", "-i", clip,
                    "-i", ov, "-filter_complex", vf, "-map", "[o]", "-frames:v", str(frames), "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
                   check=True)
    os.replace(tmp, out)


def main():
    spec, out = json.load(open(sys.argv[1])), sys.argv[2]
    ensure_fonts()
    tmpd = tempfile.mkdtemp()
    parts, total = [], 0.0
    for i, s in enumerate(spec["scenes"]):
        ov = f"{tmpd}/ov{i}.png"
        overlay(s["text"], s.get("size", 100), s.get("pos", "center"), ov)
        mp4 = f"{tmpd}/s{i}.mp4"
        scene(s["clip"], s.get("start", 0), s["dur"], ov, mp4)
        parts.append(mp4); total += s["dur"]
    lst = f"{tmpd}/list.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    video = f"{tmpd}/v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)
    music = spec.get("music")
    if not music:
        tracks = [p for e in ("mp3", "m4a") for p in glob.glob(str(pathlib.Path(__file__).parent / "music" / f"*.{e}"))]
        music = random.choice(tracks) if tracks else None
    ain = ["-stream_loop", "-1", "-i", music] if music else ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    af = ["-af", f"afade=t=in:d=0.5,afade=t=out:st={total-1:.2f}:d=1"] if music else []
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, *ain, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", *af, "-t", f"{total:.2f}",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    print(out, f"{total:.1f}s", "music:" + (os.path.basename(music) if music else "silent"))


if __name__ == "__main__":
    main()
