#!/bin/bash
# Render public/assets/share-card.png from scripts/share_card.html. Run from the repo root.
set -e
python3 -m http.server 8767 --bind 127.0.0.1 >/dev/null 2>&1 & pid=$!
trap 'kill $pid 2>/dev/null' EXIT
sleep 1
tmp="$(mktemp -d)/card.png"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1200,630 --screenshot="$tmp" http://127.0.0.1:8767/scripts/share_card.html >/dev/null 2>&1
magick "$tmp" -filter Lanczos -resize 1200x630 public/assets/share-card.png
magick identify -format 'share-card.png %wx%h\n' public/assets/share-card.png
