#!/usr/bin/env python3
"""Elevate Reel maker: turns a carousel's slide images into a 9:16 Reel (1080x1920, 30 fps, H.264 + AAC).

Usage: python3 elevate_reel.py OUT.mp4 slide1.jpg slide2.jpg ... [--music path.mp3]

Each slide sits on a blurred, darkened copy of itself with a slow push-in, ~3 s per slide
(cover 3.5 s, last slide 4 s), short fades between slides. If --music is not given and the
repo has a music/ folder with .mp3/.m4a files, one is picked at random; otherwise the Reel
gets a silent audio track (Instagram requires audio streams to be valid, not present).
"""
import sys, os, random, subprocess, tempfile, pathlib, glob
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = os.path.expanduser("~/.elevate_fonts/Anton-Regular.ttf")


def frame(slide_path, out_png):
    s = Image.open(slide_path).convert("RGB")
    bg = s.copy().resize((int(s.width * H / s.height), H))
    x0 = (bg.width - W) // 2
    bg = bg.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)
    fg = s.resize((W, int(s.height * W / s.width)))
    top = (H - fg.height) // 2
    bg.paste(fg, (0, top))
    d = ImageDraw.Draw(bg)
    try:
        f = ImageFont.truetype(FONT, 46)
        t = "@ELEVATEXWEALTH"
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, top + fg.height + 60), t, font=f, fill=(242, 184, 75))
    except OSError:
        pass
    bg.save(out_png, quality=95)


def clip(png, out, dur):
    frames = int(dur * FPS)
    vf = (f"scale=2160:-1,zoompan=z='min(1+0.0009*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s={W}x{H}:fps={FPS},fade=t=in:st=0:d=0.25,fade=t=out:st={dur-0.25:.2f}:d=0.25,format=yuv420p")
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-vf", vf, "-frames:v", str(frames),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
                   check=True)
    os.replace(tmp, out)


def main():
    args = sys.argv[1:]
    music = None
    if "--music" in args:
        i = args.index("--music"); music = args[i + 1]; del args[i:i + 2]
    out, slides = args[0], args[1:]
    if music is None:
        tracks = glob.glob(str(pathlib.Path(__file__).parent / "music" / "*.mp3")) + \
                 glob.glob(str(pathlib.Path(__file__).parent / "music" / "*.m4a"))
        music = random.choice(tracks) if tracks else None
    tmpd = tempfile.mkdtemp()
    parts = []
    for n, sp in enumerate(slides):
        dur = 3.5 if n == 0 else (4.0 if n == len(slides) - 1 else 3.0)
        png = f"{tmpd}/f{n}.jpg"; frame(sp, png)
        mp4 = f"{tmpd}/c{n}.mp4"; clip(png, mp4, dur); parts.append((mp4, dur))
    lst = f"{tmpd}/list.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p, _ in parts))
    total = sum(d for _, d in parts)
    video = f"{tmpd}/video.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)
    audio_in = ["-stream_loop", "-1", "-i", music] if music else ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    afilter = ["-af", f"afade=t=in:d=0.8,afade=t=out:st={total-1.2:.2f}:d=1.2"] if music else []
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, *audio_in, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", *afilter, "-t", f"{total:.2f}",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    print(out, f"{total:.1f}s", "music:" + (os.path.basename(music) if music else "silent"))


if __name__ == "__main__":
    main()
