#!/usr/bin/env python3
"""Elevate (@ElevatexWealth) carousel renderer.
Usage: python3 elevate_render.py spec.json OUTDIR
spec.json = {"slides":[{...}, ...]}  (1080x1350 PNGs, Instagram 4:5)
Slide keys:
  photo: local jpg path (required)       pos: CSS object-position (default "center")
  split: [path2, pos2]  -> second photo side-by-side with `photo` (optional)
  photo_h: px height of photo area (default 830)
  circle: {"src": path, "pos": "center", "size": 330, "x": 690, "y": 470}   (optional)
  arrow: {"x": 430, "y": 250}  curved white arrow (optional)
  pills: [{"text": "...", "x": 32, "y": 740, "gold": true}]                  (optional)
  stats: [{"label": "GRACE AT 65", "value": "$524,963", "side": "left"}]      (optional)
  headline: text; wrap gold words in [[double brackets]]   (required)
  size: headline px (default 84)
  sub: smaller paragraph under headline (optional, plain text)
  footnote: tiny disclaimer at bottom (optional)
"""
import json, sys, os, re, pathlib, html, urllib.request

GOLD = "#F2B84B"
FONT_DIR = pathlib.Path(os.path.expanduser("~/.elevate_fonts"))
FONTS = {
    "Anton-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf",
    "Inter.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
}

def fonts():
    FONT_DIR.mkdir(exist_ok=True)
    for name, url in FONTS.items():
        p = FONT_DIR / name
        if not p.exists() or p.stat().st_size < 10000:
            urllib.request.urlretrieve(url, p)
    return (f"@font-face{{font-family:Anton;src:url('file://{FONT_DIR}/Anton-Regular.ttf')}}"
            f"@font-face{{font-family:Inter;src:url('file://{FONT_DIR}/Inter.ttf')}}")

def esc(t): return html.escape(t, quote=False)
def gold(t): return re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span style="color:{GOLD}">{m.group(1)}</span>', esc(t))
def url(p): return "file://" + str(pathlib.Path(p).resolve())

ARROW = ('<svg width="260" height="200" viewBox="0 0 260 200" style="position:absolute;left:{x}px;top:{y}px">'
         '<path d="M10 30 C 110 0, 210 60, 225 170" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>'
         '<path d="M195 150 L227 182 L250 140" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
LOGO = (f'<div style="display:flex;align-items:center;gap:18px;width:100%;margin-top:-24px;position:relative">'
        f'<div style="flex:1;height:3px;background:{GOLD}"></div>'
        f'<div style="display:flex;align-items:center;gap:10px;background:#0B0B0C;padding:8px 16px;border:2px solid {GOLD};border-radius:999px">'
        f'<svg width="26" height="22" viewBox="0 0 26 22"><path d="M2 20 L13 9 L24 20" fill="none" stroke="{GOLD}" stroke-width="3.5" stroke-linejoin="round"/>'
        f'<path d="M6 11 L13 4 L20 11" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/></svg>'
        f'<span style="font-family:Anton;font-size:24px;letter-spacing:3px">ELEVATE</span></div>'
        f'<div style="flex:1;height:3px;background:{GOLD}"></div></div>')

def slide_html(s, ff):
    ph = s.get("photo_h", 830)
    img = lambda p, pos: f'<img src="{url(p)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}">'
    if s.get("split"):
        photo = (f'<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;gap:6px;background:#0B0B0C">'
                 f'<div style="overflow:hidden">{img(s["photo"], s.get("pos","center"))}</div>'
                 f'<div style="overflow:hidden">{img(s["split"][0], s["split"][1])}</div></div>')
    else:
        photo = f'<div style="position:absolute;inset:0">{img(s["photo"], s.get("pos","center"))}</div>'
    if s.get("arrow"): photo += ARROW.format(**s["arrow"])
    c = s.get("circle")
    if c:
        sz = c.get("size", 330)
        photo += (f'<div style="position:absolute;left:{c.get("x",690)}px;top:{c.get("y",470)}px;width:{sz}px;height:{sz}px;border-radius:50%;'
                  f'overflow:hidden;border:8px solid #fff;box-shadow:0 12px 40px rgba(0,0,0,.45)">{img(c["src"], c.get("pos","center"))}</div>')
    for p in s.get("pills", []):
        bg, fg = (GOLD, "#0B0B0C") if p.get("gold") else ("#fff", "#0B0B0C")
        photo += (f'<div style="position:absolute;left:{p["x"]}px;top:{p["y"]}px;background:{bg};color:{fg};font-family:Anton;'
                  f'font-size:34px;letter-spacing:1px;padding:10px 22px;border-radius:10px">{esc(p["text"])}</div>')
    for st in s.get("stats", []):
        side = "left:40px" if st.get("side", "left") == "left" else "right:40px"
        col = GOLD if st.get("side", "left") == "left" else "#D6D6D6"
        photo += (f'<div style="position:absolute;{side};bottom:60px;background:rgba(11,11,12,.88);border-radius:18px;padding:22px 28px;display:flex;flex-direction:column;gap:4px">'
                  f'<span style="font-size:24px;font-weight:700;color:{col}">{esc(st["label"])}</span>'
                  f'<span style="font-family:Anton;font-size:72px;line-height:1">{esc(st["value"])}</span></div>')
    sub = f'<p style="margin:22px 0 0;font-size:32px;line-height:1.4;text-align:center;color:#D6D6D6">{gold(s["sub"])}</p>' if s.get("sub") else ""
    foot = f'<p style="margin:auto 0 0;font-size:17px;line-height:1.45;text-align:center;color:#9A9A9A">{esc(s["footnote"])}</p>' if s.get("footnote") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}
body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="width:1080px;height:1350px;overflow:hidden;background:#0B0B0C;color:#fff;font-family:Inter,sans-serif;display:flex;flex-direction:column">
<div style="height:{ph}px;position:relative;overflow:hidden;flex-shrink:0">{photo}</div>
<div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:0 56px 44px">{LOGO}
<h1 style="margin:30px 0 0;font-family:Anton;font-weight:400;font-size:{s.get('size',84)}px;line-height:1.04;text-align:center;text-transform:uppercase;letter-spacing:.5px">{gold(s['headline'])}</h1>
{sub}{foot}</div></div></body></html>"""

def main(spec_path, out):
    from playwright.sync_api import sync_playwright
    spec = json.load(open(spec_path)); os.makedirs(out, exist_ok=True)
    ff = fonts(); paths = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(spec["slides"], 1):
            h = pathlib.Path(out) / f"slide{i}.html"; h.write_text(slide_html(s, ff))
            pg.goto(url(h)); pg.wait_for_timeout(400)
            # shrink headline if it overflows the band
            pg.evaluate("""()=>{const h=document.querySelector('h1');const band=h.parentElement;
              let fs=parseFloat(getComputedStyle(h).fontSize);
              while(band.scrollHeight>band.clientHeight+1&&fs>48){fs-=2;h.style.fontSize=fs+'px';}}""")
            png = pathlib.Path(out) / f"slide{i}.png"; pg.screenshot(path=str(png), type="png"); paths.append(str(png))
        b.close()
    print("\n".join(paths))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
