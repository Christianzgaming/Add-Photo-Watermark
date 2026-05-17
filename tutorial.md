# 📸 Watermark Tool — Complete Tutorial

A Python script that **auto-detects all your photos**, adds a custom watermark to the bottom-right corner, converts them to any image format, and optionally enhances them to HD quality — all in one command.

---

## 📋 Table of Contents

1. [Requirements](#1-requirements)
2. [Installation](#2-installation)
3. [Folder Setup](#3-folder-setup)
4. [Basic Usage](#4-basic-usage)
5. [Adding a Custom Watermark](#5-adding-a-custom-watermark)
6. [Changing the Watermark Color](#6-changing-the-watermark-color)
7. [Adjusting Size & Opacity](#7-adjusting-size--opacity)
8. [Converting to a Different Format](#8-converting-to-a-different-format)
9. [HD Enhancement](#9-hd-enhancement)
10. [Full Command Example](#10-full-command-example)
11. [All Options Reference](#11-all-options-reference)
12. [Output Folder](#12-output-folder)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Requirements

- Python 3.10 or newer
- Pillow library

Check your Python version:

```bash
python --version
```

---

## 2. Installation

Install the only dependency needed — **Pillow**:

```bash
pip install Pillow
```

That's it. No other libraries required.

---

## 3. Folder Setup

Place `watermark.py` **in the same folder** as your photos. The script will automatically find all images there.

```
📁 your-folder/
  ├── watermark.py        ← script goes here
  ├── photo1.jpg
  ├── photo2.png
  ├── selfie.webp
  └── vacation.jpeg
```

After running, a new subfolder is created automatically:

```
📁 your-folder/
  ├── watermark.py
  ├── photo1.jpg
  ├── photo2.png
  ├── selfie.webp
  ├── vacation.jpeg
  └── 📁 watermarked/     ← all output goes here
        ├── photo1.jpg
        ├── photo2.png
        ├── selfie.webp
        └── vacation.jpeg
```

> ✅ Your original photos are **never modified**. Only the copies inside `watermarked/` are changed.

---

## 4. Basic Usage

Open a terminal, navigate to your folder, and run:

```bash
python watermark.py
```

This will process all PNG, JPG, JPEG, and WebP images in the folder using the default watermark text `© Watermark`.

---

## 5. Adding a Custom Watermark

Use `--text` (or `-t`) to set your own watermark name or credit:

```bash
python watermark.py --text "© Juan dela Cruz"
```

```bash
python watermark.py --text "@KingSpice"
```

```bash
python watermark.py --text "Credits: Jane Santos"
```

```bash
python watermark.py --text "📷 Shot by KingSpice"
```

> Wrap your text in quotes if it contains spaces or special characters.

---

## 6. Changing the Watermark Color

Use `--color` (or `-c`) to pick a color:

**Preset colors:**

```bash
python watermark.py --text "@KingSpice" --color white
python watermark.py --text "@KingSpice" --color black
python watermark.py --text "@KingSpice" --color gray
python watermark.py --text "@KingSpice" --color yellow
python watermark.py --text "@KingSpice" --color red
python watermark.py --text "@KingSpice" --color cyan
```

**Custom hex color:**

```bash
python watermark.py --text "@KingSpice" --color "#ff6600"
python watermark.py --text "@KingSpice" --color "#ffffff"
```

| Color name | Preview |
|------------|---------|
| `white` | Best on dark photos |
| `black` | Best on light/bright photos |
| `yellow` | High visibility on any photo |
| `gray` | Subtle, professional look |
| `red` | Bold and eye-catching |
| `cyan` | Modern, clean look |

---

## 7. Adjusting Size & Opacity

### Font Size

Use `--size` (or `-s`) to control how big the watermark text is (in pixels):

```bash
python watermark.py --text "@KingSpice" --size 20    # small
python watermark.py --text "@KingSpice" --size 32    # default
python watermark.py --text "@KingSpice" --size 50    # large
python watermark.py --text "@KingSpice" --size 80    # very large
```

### Opacity (Transparency)

Use `--opacity` (or `-a`) to control how visible the watermark is. Range is `0` (invisible) to `255` (fully solid):

```bash
python watermark.py --text "@KingSpice" --opacity 80     # very transparent
python watermark.py --text "@KingSpice" --opacity 160    # default (semi-transparent)
python watermark.py --text "@KingSpice" --opacity 220    # nearly solid
python watermark.py --text "@KingSpice" --opacity 255    # fully solid
```

### Edge Padding

Use `--padding` (or `-p`) to control the distance of the watermark from the bottom-right edge:

```bash
python watermark.py --text "@KingSpice" --padding 10   # close to the edge
python watermark.py --text "@KingSpice" --padding 20   # default
python watermark.py --text "@KingSpice" --padding 40   # more breathing room
```

### Drop Shadow

The watermark has a drop shadow by default for readability. Disable it with:

```bash
python watermark.py --text "@KingSpice" --no-shadow
```

---

## 8. Converting to a Different Format

Use `--format` (or `-f`) to convert **all output images** to a specific file format:

```bash
# Save all as PNG
python watermark.py --text "@KingSpice" --format png

# Save all as JPG
python watermark.py --text "@KingSpice" --format jpg

# Save all as WebP (smaller file size, great for web)
python watermark.py --text "@KingSpice" --format webp
```

**Format comparison:**

| Format | Best for | File size |
|--------|----------|-----------|
| `jpg` | Photos, social media | Small |
| `png` | Graphics, transparency | Medium–Large |
| `webp` | Web, modern apps | Smallest |
| `jpeg` | Same as jpg | Small |

> If you skip `--format`, each image keeps its original format.

---

## 9. HD Enhancement

Use `--enhance` (or `-e`) to improve the quality and sharpness of your photos before watermarking. Think of it like a built-in Remini-style enhancer.

```bash
python watermark.py --text "@KingSpice" --enhance 25    # light
python watermark.py --text "@KingSpice" --enhance 50    # moderate
python watermark.py --text "@KingSpice" --enhance 75    # strong
python watermark.py --text "@KingSpice" --enhance 100   # maximum HD
```

**What each level does:**

| Level | Effect |
|-------|--------|
| `0` | No enhancement (default) |
| `25` | Light sharpening + slight clarity boost |
| `50` | Moderate HD — sharper edges, more vivid colors |
| `75` | Strong HD — crisp, punchy, more contrast |
| `100` | **Maximum HD** — 2× upscale + full pipeline (sharpness, contrast, color, brightness, detail recovery) |

**What `--enhance 100` does step by step:**

1. Upscales the image to **2× its original size** using LANCZOS (best quality filter)
2. Applies a **3× sharpness boost** for crisp edges
3. Boosts **contrast by +50%** for deeper blacks and brighter whites
4. Increases **color saturation by +40%** for vivid, punchy output
5. Adds a slight **brightness lift** so it doesn't look flat
6. Runs an **Unsharp Mask** pass to recover fine texture details
7. Scales back to the **original resolution** — retaining all recovered detail

> 💡 Use `--enhance 100` on blurry or low-resolution photos for the best results.

---

## 10. Full Command Example

This is the full command combining all features:

```bash
python watermark.py --text "@KingSpice" --color yellow --size 20 --format webp --enhance 100
```

What this does:
- Finds all images in the same folder
- Enhances every photo to maximum HD quality
- Stamps `@KingSpice` in yellow at the bottom-right
- Converts all output files to WebP format
- Saves everything to the `watermarked/` folder

More real-world examples:

```bash
# Instagram-style credit, white text, PNG output
python watermark.py --text "📷 @KingSpice" --color white --size 28 --format png --enhance 75

# Photography watermark, semi-transparent, keep original format
python watermark.py --text "© KingSpice Photography" --color white --opacity 130 --size 24

# Bold yellow credit with HD enhance, WebP output
python watermark.py --text "@KingSpice" --color yellow --size 20 --opacity 200 --format webp --enhance 100

# Subtle gray watermark, no shadow, JPG output
python watermark.py --text "© KingSpice" --color gray --opacity 120 --no-shadow --format jpg
```

---

## 11. All Options Reference

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--text` | `-t` | `© Watermark` | Your watermark name or credit text |
| `--size` | `-s` | `32` | Font size in pixels |
| `--opacity` | `-a` | `160` | Text transparency — `0` invisible, `255` solid |
| `--color` | `-c` | `white` | Text color — preset name or `#rrggbb` hex |
| `--padding` | `-p` | `20` | Distance from right/bottom edges in pixels |
| `--no-shadow` | — | off | Disables the drop shadow behind the text |
| `--format` | `-f` | same as source | Output format — `png`, `jpg`, `jpeg`, `webp` |
| `--enhance` | `-e` | `0` | HD enhancement level — `0` to `100` |

Short flags work the same way:

```bash
python watermark.py -t "@KingSpice" -c yellow -s 20 -f webp -e 100
```

---

## 12. Output Folder

All processed images are saved inside a `watermarked/` folder that is automatically created next to `watermark.py`.

```
📁 your-folder/
  └── 📁 watermarked/
        ├── photo1.webp    ← watermarked + converted
        ├── photo2.webp
        └── selfie.webp
```

If you run the command again, files in `watermarked/` are overwritten with the new settings.

---

## 13. Troubleshooting

**`❌ Pillow is not installed`**
```bash
pip install Pillow
```

**`⚠️ No images found`**
Make sure `watermark.py` is in the same folder as your photos. Supported formats are `.png`, `.jpg`, `.jpeg`, `.webp`.

**`python` not recognized on Windows**
Try using `py` instead:
```bash
py watermark.py --text "@KingSpice" --enhance 100
```

**Watermark text is too small or too large**
Adjust with `--size`. For a 1080p photo, `--size 28` to `--size 40` is a good range.

**Output looks too sharp or over-processed**
Lower the enhance level — try `--enhance 50` or `--enhance 75` instead of `100`.

**Want no watermark, just HD enhancement?**
Set the text to a single space:
```bash
python watermark.py --text " " --opacity 0 --enhance 100
```

---

*Made with Python + Pillow — no internet connection required.*
