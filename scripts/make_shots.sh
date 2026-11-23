#!/bin/bash
# Build the two web versions of a product screenshot from its full-resolution PNG source.
#   scripts/make_shots.sh <name> <source.png>
# Writes public/assets/site/img/<name>.webp      (1600px wide, for inline display)
#    and public/assets/site/img/<name>-full.webp (native resolution, for large screens and the full-size viewer).
# High quality on purpose: UI text must stay sharp. Never upscale a source.
set -e
name="$1"; src="$2"; out="public/assets/site/img"; tmp="$(mktemp -d)"
w=$(magick identify -format '%w' "$src")
[ "$w" -lt 2400 ] && echo "WARNING: $src is only ${w}px wide; capture at 2560px or more" >&2
magick "$src" -filter Lanczos -resize 1600x -unsharp 0x0.5+0.5+0.02 "$tmp/inline.png"
cwebp -quiet -q 92 -sharp_yuv -m 6 "$tmp/inline.png" -o "$out/$name.webp"
cwebp -quiet -q 92 -sharp_yuv -m 6 "$src" -o "$out/$name-full.webp"
rm -rf "$tmp"
for f in "$out/$name.webp" "$out/$name-full.webp"; do
  printf '%s %sx%s %sK\n' "$(basename "$f")" "$(magick identify -format '%w' "$f")" "$(magick identify -format '%h' "$f")" "$(( $(stat -f%z "$f") / 1024 ))"
done
