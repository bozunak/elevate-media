#!/usr/bin/env python3
"""Find and download a Pexels video file by its numeric id (from the pexels.com/video/... page URL).
Usage: python3 pexels_video.py ID OUT.mp4 [--vertical]
Tries the usual file-name patterns on videos.pexels.com, preferring 1080p (smaller, enough for Reels)."""
import sys, subprocess
vid, out = sys.argv[1], sys.argv[2]
vertical = "--vertical" in sys.argv
dims_v = [("hd", 1080, 1920), ("uhd", 2160, 3840), ("hd", 720, 1280), ("sd", 540, 960), ("uhd", 1440, 2560)]
dims_h = [("hd", 1920, 1080), ("uhd", 3840, 2160), ("uhd", 2560, 1440), ("hd", 1280, 720), ("uhd", 4096, 2160), ("hd", 2048, 1080), ("sd", 960, 540)]
order = (dims_v + dims_h) if vertical else (dims_h + dims_v)
for q, w, h in order:
    for fps in (30, 25, 24, 60, 50):
        for url in (f"https://videos.pexels.com/video-files/{vid}/{vid}-{q}_{w}_{h}_{fps}fps.mp4",
                    f"https://videos.pexels.com/video-files/{vid}/{vid}_{w}_{h}_{fps}fps.mp4"):
            r = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-I", "-w", "%{http_code}", url], capture_output=True, text=True)
            if r.stdout.strip() == "200":
                subprocess.run(["curl", "-sS", "-o", out, url], check=True)
                print(out, url); sys.exit(0)
print("not found", vid); sys.exit(1)
