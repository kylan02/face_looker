#!/bin/bash
# Quick start script for generating face images

set -e

echo "🎭 Face Looker - Quick Start Generator"
echo "======================================"
echo ""

# Check if REPLICATE_API_TOKEN is set
if [ -z "$REPLICATE_API_TOKEN" ]; then
    echo "❌ Error: REPLICATE_API_TOKEN not set!"
    echo ""
    echo "Please set your Replicate API token:"
    echo "  export REPLICATE_API_TOKEN=your_token_here"
    echo ""
    echo "Get your token at: https://replicate.com/account/api-tokens"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if image is provided
if [ -z "$1" ]; then
    echo "❌ Error: No image provided!"
    echo ""
    echo "Usage: ./generate.sh <image_path> [output_dir] [step]"
    echo ""
    echo "Examples:"
    echo "  ./generate.sh my_face.jpg"
    echo "  ./generate.sh my_face.jpg ./faces"
    echo "  ./generate.sh my_face.jpg ./faces 2.5"
    exit 1
fi

IMAGE=$1
OUTPUT=${2:-./out}
STEP=${3:-3}

# Check if image exists
if [ ! -f "$IMAGE" ]; then
    echo "❌ Error: Image not found: $IMAGE"
    exit 1
fi

echo ""
echo "⚙️  Configuration:"
echo "   Image: $IMAGE"
echo "   Output: $OUTPUT"
echo "   Step: $STEP"
echo ""

# Calculate number of images
IMAGES=$(echo "scale=0; ((15 - (-15)) / $STEP + 1) ^ 2" | bc)
echo "📊 Will generate approximately $IMAGES images"
echo ""

# Confirm
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Run generation
echo ""
echo "🚀 Starting generation..."
echo ""

python main.py \
    --image "$IMAGE" \
    --out "$OUTPUT" \
    --step "$STEP" \
    --skip-existing

echo ""
echo "✅ Done! Images saved to: $OUTPUT"
echo ""
echo "📋 Next steps:"
echo "   1. Copy faces to your React project:"
echo "      cp -r $OUTPUT /path/to/your-react-app/public/faces"
echo ""
echo "   2. Copy React components:"
echo "      cp useGazeTracking.js /path/to/your-react-app/src/hooks/"
echo "      cp FaceTracker.jsx /path/to/your-react-app/src/components/"
echo ""
echo "   3. Use in your app:"
echo "      import FaceTracker from './components/FaceTracker'"
echo ""

