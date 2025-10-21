#!/usr/bin/env python3
"""
Generate only the missing face images for the portfolio.
This script identifies which images are missing and generates only those.
"""

import os
import sys
from pathlib import Path
from main import build_gaze_grid, filename_for, run_expression_editor, save_resized_webp, is_url

def find_missing_images(portfolio_dir, vmin=-15, vmax=15, step=2.5, size=256):
    """Find which images are missing from the portfolio directory."""
    portfolio_path = Path(portfolio_dir)
    if not portfolio_path.exists():
        print(f"ERROR: Portfolio directory not found: {portfolio_path}")
        return []
    
    # Generate expected filenames for step=2.5
    grid = build_gaze_grid(vmin, vmax, step)
    missing_files = []
    
    print(f"Checking {len(grid)} expected files in {portfolio_path}")
    
    for gp in grid:
        fname = filename_for(gp.px, gp.py, size)
        file_path = portfolio_path / fname
        if not file_path.exists():
            missing_files.append((gp.px, gp.py, fname))
            print(f"  MISSING: {fname}")
        else:
            print(f"  EXISTS: {fname}")
    
    return missing_files

def generate_missing_images(image_path, portfolio_dir, vmin=-15, vmax=15, step=2.5, size=256):
    """Generate only the missing images."""
    
    # Check for API token
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("ERROR: REPLICATE_API_TOKEN not set in environment.")
        print("Please set your Replicate API token:")
        print("export REPLICATE_API_TOKEN=your_token_here")
        return False
    
    # Find missing images
    print("🔍 Scanning for missing images...")
    missing = find_missing_images(portfolio_dir, vmin, vmax, step, size)
    
    if not missing:
        print("✅ All images are present! No missing files found.")
        return True
    
    print(f"📊 Found {len(missing)} missing images out of {13*13} total expected.")
    print("Missing images:")
    for _, _, fname in missing:
        print(f"  - {fname}")
    
    # Prepare image input for Replicate
    if is_url(image_path):
        image_input = image_path
    else:
        p = Path(image_path)
        if not p.exists():
            print(f"ERROR: Image path not found: {p}")
            return False
        image_input = open(p, "rb")
    
    # Generate missing images
    print(f"\n🎨 Generating {len(missing)} missing images...")
    success_count = 0
    
    for i, (px, py, fname) in enumerate(missing, 1):
        print(f"[{i}/{len(missing)}] Generating {fname} (px={px}, py={py})...")
        
        try:
            output_files = run_expression_editor(image_input, px, py)
            if not output_files:
                print(f"  ⚠️  WARNING: No output for ({px}, {py}). Skipping.")
                continue
            
            # Save to portfolio directory
            target_path = Path(portfolio_dir) / fname
            save_resized_webp(output_files[0], target_path, size=size, quality=95)
            success_count += 1
            print(f"  ✅ Saved: {fname}")
            
        except Exception as e:
            print(f"  ❌ ERROR generating {fname}: {e}")
            continue
    
    print(f"\n🎉 Generation complete!")
    print(f"✅ Successfully generated: {success_count}/{len(missing)} images")
    print(f"📁 Images saved to: {portfolio_dir}")
    
    return success_count == len(missing)

def main():
    """Main function to run the missing image generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate missing face images for portfolio")
    parser.add_argument("--image", default="./my_face.jpg", help="Path to source image")
    parser.add_argument("--portfolio", default="/Users/kylanoconnor/Desktop/projects/kylan_portfolio_site/public/faces", help="Portfolio faces directory")
    parser.add_argument("--min", dest="vmin", type=float, default=-15.0, help="Minimum value for pupil_x/y")
    parser.add_argument("--max", dest="vmax", type=float, default=15.0, help="Maximum value for pupil_x/y")
    parser.add_argument("--step", type=float, default=2.5, help="Step size for grid sampling")
    parser.add_argument("--size", type=int, default=256, help="Resize dimension for outputs")
    
    args = parser.parse_args()
    
    print("🚀 Missing Face Image Generator")
    print("=" * 50)
    print(f"📸 Source image: {args.image}")
    print(f"📁 Portfolio dir: {args.portfolio}")
    print(f"📐 Grid: {args.vmin} to {args.vmax}, step {args.step}")
    print(f"🖼️  Size: {args.size}x{args.size}")
    print()
    
    success = generate_missing_images(
        args.image, 
        args.portfolio, 
        args.vmin, 
        args.vmax, 
        args.step, 
        args.size
    )
    
    if success:
        print("\n🎯 All missing images generated successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some images failed to generate. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
