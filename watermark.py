#!/usr/bin/env python3
"""
Image Watermark Tool — Watermark + Format Converter + HD Enhance
Automatically detects ALL images (PNG, JPG, JPEG, WebP) in the same folder
as this script, optionally enhances them to HD quality (like Remini), adds a
watermark to the bottom-right corner, and saves the output.

── Basic usage ──────────────────────────────────────────────────────────────
    python watermark.py
    python watermark.py --text "© Your Name"

── With HD enhance ──────────────────────────────────────────────────────────
    python watermark.py --text "@KingSpice" --enhance 100
    python watermark.py --text "@KingSpice" --color yellow --size 20 --format webp --enhance 100

── Enhance levels ───────────────────────────────────────────────────────────
    --enhance 0    No enhancement (original quality)
    --enhance 25   Light sharpening + slight clarity boost
    --enhance 50   Moderate HD — sharper, more vivid
    --enhance 75   Strong HD — crisp, punchy
    --enhance 100  Maximum HD — full upscale 2× + deep sharpen + vivid colors

── All options ──────────────────────────────────────────────────────────────
    --text      / -t   Watermark label             (default: "© Watermark")
    --size      / -s   Font size in px             (default: 32)
    --opacity   / -a   Opacity 0-255               (default: 160)
    --color     / -c   white|black|gray|yellow|red|cyan|#rrggbb
    --padding   / -p   Edge padding px             (default: 20)
    --no-shadow        Disable drop shadow
    --format    / -f   Output format: png|jpg|jpeg|webp
    --enhance   / -e   HD enhance level 0-100      (default: 0 = off)

── Output ───────────────────────────────────────────────────────────────────
    Saved to a "watermarked/" subfolder next to this script.
    Originals are never modified.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
except ImportError:
    print("❌ Pillow is not installed. Run:  pip install Pillow")
    sys.exit(1)


# ── Default Configuration ─────────────────────────────────────────────────────

DEFAULT_TEXT    = "© Watermark"
DEFAULT_SIZE    = 32
DEFAULT_OPACITY = 160
DEFAULT_COLOR   = "white"
DEFAULT_PADDING = 20
DEFAULT_SHADOW  = True
DEFAULT_ENHANCE = 0            # 0 = off, 1-100 = HD level

# ─────────────────────────────────────────────────────────────────────────────

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}

FORMAT_MAP = {
    "png":  ("PNG",  ".png",  False),
    "jpg":  ("JPEG", ".jpg",  True),
    "jpeg": ("JPEG", ".jpeg", True),
    "webp": ("WEBP", ".webp", False),
}

COLOR_PRESETS = {
    "white":  (255, 255, 255),
    "black":  (0,   0,   0),
    "gray":   (180, 180, 180),
    "yellow": (255, 220, 0),
    "red":    (220, 50,  50),
    "cyan":   (0,   200, 220),
}


# ── HD Enhancement ────────────────────────────────────────────────────────────

def enhance_hd(img: Image.Image, level: int) -> Image.Image:
    """
    Multi-stage HD enhancement pipeline (0-100).

    Stage 1 (all levels > 0) : Sharpness + Contrast + Color boost
    Stage 2 (level >= 50)    : Detail filter pass (unsharp mask)
    Stage 3 (level == 100)   : 2× upscale with LANCZOS then downscale back
                               (recovers lost detail like AI upscalers do)

    level=0  → no change
    level=25 → light clarity
    level=50 → moderate HD sharpness + color
    level=75 → strong HD
    level=100→ maximum HD (upscale trick + full pipeline)
    """
    if level <= 0:
        return img

    # Normalise 1-100 to a 0.0-1.0 factor for scaling enhancer values
    t = level / 100.0   # 0.01 … 1.0

    # ── Stage 3 pre-step: 2× upscale for max quality (level 100 only) ─────
    original_size = img.size
    if level >= 100:
        big = img.resize(
            (img.width * 2, img.height * 2),
            Image.LANCZOS,
        )
        img = big

    # ── Stage 1: Sharpness, Contrast, Color saturation ────────────────────
    # Sharpness: 1.0 = original, 2.0 = doubled → we go up to ~3.0 at max
    sharpness_factor = 1.0 + t * 2.0          # 1.02 … 3.0
    img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)

    # Contrast: 1.0 = original, we add up to +0.5
    contrast_factor = 1.0 + t * 0.50          # 1.005 … 1.5
    img = ImageEnhance.Contrast(img).enhance(contrast_factor)

    # Color / Saturation: 1.0 = original, we add up to +0.4
    color_factor = 1.0 + t * 0.40             # 1.004 … 1.4
    img = ImageEnhance.Color(img).enhance(color_factor)

    # Brightness: very slight lift (avoids over-darkening)
    brightness_factor = 1.0 + t * 0.08        # 1.001 … 1.08
    img = ImageEnhance.Brightness(img).enhance(brightness_factor)

    # ── Stage 2: Unsharp mask for detail recovery (level >= 50) ───────────
    if level >= 50:
        radius    = 1 + int(t * 2)            # 1 … 3
        percent   = 80 + int(t * 120)         # 80 … 200
        threshold = max(1, 4 - int(t * 3))    # 4 … 1
        img = img.filter(ImageFilter.UnsharpMask(
            radius=radius,
            percent=percent,
            threshold=threshold,
        ))

    # ── Stage 3 post-step: downscale back to original size ────────────────
    if level >= 100:
        img = img.resize(original_size, Image.LANCZOS)

    return img


# ── Font loader ───────────────────────────────────────────────────────────────

def load_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    print("⚠️  No system font found — using Pillow's built-in font.")
    return ImageFont.load_default()


def resolve_color(color: str) -> tuple:
    if color.startswith("#") and len(color) == 7:
        return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    return COLOR_PRESETS.get(color.lower(), (255, 255, 255))


# ── Core processing ───────────────────────────────────────────────────────────

def process_image(
    src: Path,
    dst: Path,
    text: str,
    size: int,
    opacity: int,
    color: str,
    padding: int,
    shadow: bool,
    out_format: str | None,
    enhance_level: int,
) -> Path:
    """Enhance → watermark → convert → save."""

    img = Image.open(src).convert("RGBA")

    # ── Step 1: HD Enhancement ────────────────────────────────────────────────
    if enhance_level > 0:
        # Enhance works on RGB; convert, process, convert back
        rgb = img.convert("RGB")
        rgb = enhance_hd(rgb, enhance_level)
        img = rgb.convert("RGBA")

    # ── Step 2: Watermark overlay ─────────────────────────────────────────────
    W, H = img.size
    rgb_color = resolve_color(color)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = load_font(size)

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        ox, oy = -bbox[0], -bbox[1]
    except AttributeError:
        tw, th = draw.textsize(text, font=font)
        ox, oy = 0, 0

    x = W - tw - padding + ox
    y = H - th - padding + oy

    if shadow:
        sc = (0, 0, 0, min(opacity + 60, 255))
        for dx, dy in ((2, 2), (1, 2), (2, 1)):
            draw.text((x + dx - ox, y + dy - oy), text, font=font, fill=sc)

    draw.text((x - ox, y - oy), text, font=font, fill=(*rgb_color, opacity))
    img = Image.alpha_composite(img, overlay)

    # ── Step 3: Format conversion + save ─────────────────────────────────────
    if out_format:
        pil_fmt, new_ext, needs_rgb = FORMAT_MAP[out_format]
        dst = dst.with_suffix(new_ext)
    else:
        ext = src.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            pil_fmt, needs_rgb = "JPEG", True
        elif ext == ".webp":
            pil_fmt, needs_rgb = "WEBP", False
        else:
            pil_fmt, needs_rgb = "PNG", False

    if needs_rgb:
        img = img.convert("RGB")

    save_kwargs = {"quality": 95} if pil_fmt in ("JPEG", "WEBP") else {}
    img.save(dst, pil_fmt, **save_kwargs)
    return dst


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Auto-watermark + HD enhance + convert all images in this folder.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--text",      "-t", default=DEFAULT_TEXT,
                        help=f'Watermark text (default: "{DEFAULT_TEXT}")')
    parser.add_argument("--size",      "-s", default=DEFAULT_SIZE, type=int,
                        help=f"Font size px (default: {DEFAULT_SIZE})")
    parser.add_argument("--opacity",   "-a", default=DEFAULT_OPACITY, type=int,
                        metavar="0-255",
                        help=f"Opacity 0-255 (default: {DEFAULT_OPACITY})")
    parser.add_argument("--color",     "-c", default=DEFAULT_COLOR,
                        help="white|black|gray|yellow|red|cyan|#rrggbb"
                             f"  (default: {DEFAULT_COLOR})")
    parser.add_argument("--padding",   "-p", default=DEFAULT_PADDING, type=int,
                        help=f"Edge padding px (default: {DEFAULT_PADDING})")
    parser.add_argument("--no-shadow",       action="store_true",
                        help="Disable drop shadow behind text")
    parser.add_argument("--format",    "-f",
                        choices=list(FORMAT_MAP.keys()),
                        metavar="FORMAT",
                        help="Convert output to: png | jpg | jpeg | webp")
    parser.add_argument("--enhance",   "-e", default=DEFAULT_ENHANCE, type=int,
                        metavar="0-100",
                        help=(
                            "HD enhancement level 0-100  (default: 0 = off)\n"
                            "  25 = light sharpening\n"
                            "  50 = moderate HD (sharper + vivid)\n"
                            "  75 = strong HD\n"
                            " 100 = maximum HD (2× upscale + full pipeline)"
                        ))
    args = parser.parse_args()

    opacity       = max(0, min(255, args.opacity))
    enhance_level = max(0, min(100, args.enhance))
    shadow        = not args.no_shadow
    out_format    = args.format.lower() if args.format else None

    # ── Scan same folder as script ────────────────────────────────────────────
    here    = Path(__file__).parent.resolve()
    out_dir = here / "watermarked"
    out_dir.mkdir(exist_ok=True)

    images = sorted([
        f for f in here.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED
    ])

    if not images:
        print(f"\n⚠️  No images found in: {here}")
        print("   Supported: PNG, JPG, JPEG, WebP")
        print("   Place your photos in the same folder as this script.")
        sys.exit(0)

    # ── Print summary ─────────────────────────────────────────────────────────
    fmt_label = out_format.upper() if out_format else "same as source"
    hd_label  = (
        f"{enhance_level}% — "
        + ("light clarity" if enhance_level <= 25
           else "moderate HD" if enhance_level <= 50
           else "strong HD"   if enhance_level <= 75
           else "maximum HD (2× upscale + full pipeline)")
        if enhance_level > 0 else "off"
    )

    print(f"\n🖼️  Found {len(images)} image(s) in: {here}")
    print(f"   Watermark : \"{args.text}\"")
    print(f"   Color     : {args.color}  |  Size: {args.size}px  |  Opacity: {opacity}")
    print(f"   Output fmt: {fmt_label}")
    print(f"   HD Enhance: {hd_label}")
    print(f"   Saved to  : {out_dir}\n")

    ok = fail = 0
    for img_path in images:
        dst = out_dir / img_path.name
        try:
            final = process_image(
                src=img_path, dst=dst,
                text=args.text, size=args.size,
                opacity=opacity, color=args.color,
                padding=args.padding, shadow=shadow,
                out_format=out_format,
                enhance_level=enhance_level,
            )
            arrow = f"→ {final.name}" if final.name != img_path.name else ""
            print(f"  ✅ {img_path.name} {arrow}")
            ok += 1
        except Exception as e:
            print(f"  ❌ {img_path.name}  →  {e}")
            fail += 1

    print(f"\n✅ Done — {ok} processed, {fail} failed.")
    print(f"📁 Saved to: {out_dir}\n")


if __name__ == "__main__":
    main()
