#!/bin/bash
# Usage: shot.sh <outdir> <name> <path> <desktop|mobile> [height]
# Writes <outdir>/<name>-N.png tiles of a full-page screenshot of http://localhost:8765<path>.
# mobile = true 375px layout (page loaded in a 375px iframe), desktop = 1440px.
out="$1"; name="$2"; path="$3"; mode="$4"; h="${5:-6000}"
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$out"
if [ "$mode" = "mobile" ]; then
  w="$out/_wrap_$name.html"
  echo "<html><body style='margin:0;background:#888'><iframe src='http://localhost:8765$path' style='width:375px;height:${h}px;border:0;display:block'></iframe></body></html>" > "$w"
  "$C" --headless=new --disable-gpu --hide-scrollbars --window-size=520,$h --screenshot="$out/$name.png" "file://$w" >/dev/null 2>&1
  magick "$out/$name.png" -crop 375x${h}+0+0 +repage -crop 375x2200 +repage "$out/$name-%d.png"
else
  "$C" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,$h --screenshot="$out/$name.png" "http://localhost:8765$path" >/dev/null 2>&1
  magick "$out/$name.png" -crop 1440x1750 +repage -resize 1000x "$out/$name-%d.png"
fi
rm -f "$out/$name.png" "$out/_wrap_$name.html"
ls "$out" | grep "^$name-" | tr '\n' ' '
