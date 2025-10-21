
#!/usr/bin/env python3
"""
Generate a grid of gaze images using Replicate's fofr/expression-editor model,
varying only pupil_x and pupil_y (range: -15..15), then resize outputs to 256px.
Outputs are saved as WebP files with easy-to-parse filenames and a CSV index.

Usage examples:
  export REPLICATE_API_TOKEN=your_token_here
  pip install replicate pillow tqdm
  python main.py --image ./me_512.jpg --out ./out --min -15 --max 15 --step 3

Notes:
- Only pupil_x and pupil_y are changed. All other model inputs use defaults.
- Input image can be a local file path or a URL.
- Each output is resized to 256x256 using Lanczos filter.
- A CSV index (index.csv) mapping filenames to (pupil_x,pupil_y) is created.
"""

import argparse
import io
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple, List

import replicate
from PIL import Image
from tqdm import tqdm

MODEL_VERSION = "bf913bc90e1c44ba288ba3942a538693b72e8cc7df576f3beebe56adc0a92b86"

@dataclass(frozen=True)
class GazePoint:
    px: float
    py: float

def frange(start: float, stop: float, step: float) -> Iterable[float]:
    """Like range() but for floats, inclusive of stop when it lands exactly."""
    x = start
    # Protect against infinite loops from improper step sign
    if step == 0:
        raise ValueError("step must be non-zero")
    cmp = (lambda a, b: a <= b) if step > 0 else (lambda a, b: a >= b)
    while cmp(x, stop + (1e-9 if step > 0 else -1e-9)):
        yield round(x, 6)  # avoid ugly float strings
        x += step

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def build_gaze_grid(vmin: float, vmax: float, step: float) -> List[GazePoint]:
    """Build a square grid of (pupil_x, pupil_y)."""
    xs = list(frange(vmin, vmax, step))
    ys = list(frange(vmin, vmax, step))
    grid = [GazePoint(px=x, py=y) for y in ys for x in xs]
    return grid

def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://") or s.startswith("data:")

def run_expression_editor(image_input, pupil_x: float, pupil_y: float):
    """
    Calls Replicate model with pupil_x, pupil_y, rotate_pitch, and rotate_yaw adjusted.
    Returns a list of file-like objects per Replicate SDK (we expect 1).
    """
    # Clamp pupil values
    clamped_px = float(clamp(pupil_x, -15, 15))
    clamped_py = float(clamp(pupil_y, -15, 15))
    
    # Add pitch and yaw based on pupil position for more exaggerated look
    # Scale factor: convert pupil range (-15 to 15) to rotation range
    # Yaw follows horizontal pupil movement (left/right)
    rotate_yaw = (clamped_px / 15.0) * 10.0  # Max ±10 degrees
    # Pitch follows vertical pupil movement (up/down) - INVERTED
    rotate_pitch = -(clamped_py / 15.0) * 10.0  # Max ±10 degrees, inverted
    
    input_payload = {
        "image": image_input,
        "pupil_x": clamped_px,
        "pupil_y": clamped_py,
        "rotate_yaw": float(clamp(rotate_yaw, -20, 20)),
        "rotate_pitch": float(clamp(rotate_pitch, -20, 20)),
    }
    return replicate.run(
        f"fofr/expression-editor:{MODEL_VERSION}",
        input=input_payload
    )

def save_resized_webp(file_like, out_path: Path, size: int = 256, quality: int = 95):
    """
    Read the webp bytes from Replicate, resize to square `size`, and save as webp.
    """
    raw = file_like.read()
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="WEBP", quality=quality, method=6)

def sanitize_val(v: float) -> str:
    """
    Make a safe string piece for filename from a float, preserving sign and major decimals.
    E.g., -12.5 -> "m12p5"; 3 -> "3"; 0.0 -> "0"
    """
    s = f"{v}".replace("-", "m").replace(".", "p")
    return s

def filename_for(px: float, py: float, size: int = 256) -> str:
    """Create consistent filename embedding gaze values and size."""
    return f"gaze_px{sanitize_val(px)}_py{sanitize_val(py)}_{size}.webp"

def write_index(csv_path: Path, rows: List[Tuple[str, float, float]]):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("filename,pupil_x,pupil_y\n")
        for name, px, py in rows:
            f.write(f"{name},{px},{py}\n")

def main():
    parser = argparse.ArgumentParser(description="Generate gaze images with varying pupil_x/y using Replicate.")
    parser.add_argument("--image", required=True, help="Path to local image (512x512 recommended) or URL")
    parser.add_argument("--out", default="./out", help="Output directory")
    parser.add_argument("--min", dest="vmin", type=float, default=-15.0, help="Minimum value for pupil_x/y")
    parser.add_argument("--max", dest="vmax", type=float, default=15.0, help="Maximum value for pupil_x/y")
    parser.add_argument("--step", type=float, default=3.0, help="Step size for grid sampling")
    parser.add_argument("--size", type=int, default=256, help="Resize dimension (square) for outputs")
    parser.add_argument("--skip-existing", action="store_true", help="Skip generation if target file already exists")
    args = parser.parse_args()

    # Validate token presence early
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("ERROR: REPLICATE_API_TOKEN not set in environment.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Prepare image input for Replicate
    if is_url(args.image):
        image_input = args.image
    else:
        p = Path(args.image)
        if not p.exists():
            print(f"ERROR: image path not found: {p}", file=sys.stderr)
            sys.exit(1)
        image_input = open(p, "rb")

    # Build grid and iterate
    grid = build_gaze_grid(args.vmin, args.vmax, args.step)
    index_rows: List[Tuple[str, float, float]] = []

    for gp in tqdm(grid, desc="Generating", unit="img"):
        fname = filename_for(gp.px, gp.py, args.size)
        target = out_dir / fname
        if args.skip_existing and target.exists():
            index_rows.append((fname, gp.px, gp.py))
            continue

        try:
            output_files = run_expression_editor(image_input, gp.px, gp.py)
            if not output_files:
                print(f"WARNING: No output for ({gp.px}, {gp.py}). Skipping.", file=sys.stderr)
                continue

            # Replicate returns a list; we take first
            save_resized_webp(output_files[0], target, size=args.size, quality=95)
            index_rows.append((fname, gp.px, gp.py))
        except Exception as e:
            print(f"ERROR generating ({gp.px}, {gp.py}): {e}", file=sys.stderr)

    # Write CSV index
    write_index(out_dir / "index.csv", index_rows)

    # Helpful note for selecting nearest gaze later
    print(f"Done. Wrote {len(index_rows)} images to {out_dir.resolve()} and index.csv")

if __name__ == "__main__":
    main()
