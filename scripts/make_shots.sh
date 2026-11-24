#!/bin/bash
# Build the two web versions of a product screenshot from its full-resolution PNG source.
#   scripts/make_shots.sh <name> <source.png>
# Writes public/assets/site/img/<name>.webp      (1600px wide, for inline display)
#    and public/assets/site/img/<name>-full.webp (native resolution, for large screens and the full-size viewer).
#   scripts/make_shots.sh --sizes <name> <width> [<width> ...]
# Writes public/assets/site/img/<name>-<width>.webp for each width, scaled down from the existing
#    <name>-full.webp with the same settings. For slots that are drawn small (the homepage hero stack);
#    list them in the image's srcset. The 1600px and full-size files are left as they are.
# High quality on purpose: UI text must stay sharp. Never upscale a source.
set -e
if [ "$1" = "--sizes" ]; then
  name="$2"; shift 2; out="public/assets/site/img"; src="$out/$name-full.webp"; tmp="$(mktemp -d)"
  full=$(magick identify -format '%w' "$src")
  for w in "$@"; do
    [ "$w" -ge "$full" ] && { echo "ERROR: ${w}px would upscale $src (${full}px)" >&2; exit 1; }
    magick "$src" -filter Lanczos -resize "${w}x" -unsharp 0x0.5+0.5+0.02 "$tmp/$w.png"
    cwebp -quiet -q 92 -sharp_yuv -m 6 "$tmp/$w.png" -o "$out/$name-$w.webp"
    printf '%s %sx%s %sK\n' "$name-$w.webp" "$(magick identify -format '%w' "$out/$name-$w.webp")" "$(magick identify -format '%h' "$out/$name-$w.webp")" "$(( $(stat -f%z "$out/$name-$w.webp") / 1024 ))"
  done
  rm -rf "$tmp"; exit 0
fi
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
