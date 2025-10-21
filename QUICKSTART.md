# ⚡ Quick Start Guide

Get up and running with Face Looker in 5 minutes!

## 🎯 Goal

Create an interactive face that follows your cursor in a React app.

## 📝 Prerequisites

- [ ] Python 3.7+ installed
- [ ] Node.js installed (for React)
- [ ] Replicate account (free tier works!)
- [ ] A 512×512 photo of a face

## 🚀 Steps

### 1. Get Your Replicate API Token (2 minutes)

1. Go to https://replicate.com/
2. Sign up (free)
3. Go to https://replicate.com/account/api-tokens
4. Copy your API token
5. Save it:

```bash
export REPLICATE_API_TOKEN=your_token_here
```

### 2. Clone and Setup (1 minute)

```bash
# Clone the repo
git clone https://github.com/yourusername/face_looker.git
cd face_looker

# Quick setup (auto-installs dependencies)
./generate.sh my_face.jpg
```

Or manual setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Generate Face Images (2-5 minutes)

**Automatic (recommended):**
```bash
./generate.sh my_face.jpg
```

**Manual:**
```bash
python main.py --image my_face.jpg --out ./out
```

⏰ This takes 2-5 minutes depending on your settings. Grab a coffee!

### 4. Use in React (30 seconds)

```bash
# Copy faces to your React project
cp -r ./out /path/to/your-react-app/public/faces

# Copy React files
cp useGazeTracking.js /path/to/your-react-app/src/hooks/
cp FaceTracker.jsx /path/to/your-react-app/src/components/
cp FaceTracker.css /path/to/your-react-app/src/components/
```

### 5. Add to Your App (30 seconds)

```jsx
import FaceTracker from './components/FaceTracker';

function App() {
  return (
    <div style={{ width: '400px', height: '400px' }}>
      <FaceTracker />
    </div>
  );
}
```

## ✅ Done!

Your face should now follow the cursor! 🎉

## 🎛️ Customization

### Smoother transitions (more images):
```bash
python main.py --image my_face.jpg --out ./out --step 2.5
```

### Faster generation (fewer images):
```bash
python main.py --image my_face.jpg --out ./out --step 5
```

### Circular face:
```css
.face-tracker {
  border-radius: 50%;
  overflow: hidden;
}
```

## 🐛 Troubleshooting

### "REPLICATE_API_TOKEN not set"
```bash
export REPLICATE_API_TOKEN=your_actual_token
```

### Images not loading in React
- Check that faces are in `public/faces/`
- Verify `basePath="/faces/"` matches your structure
- Check browser console for 404 errors

### Face not following cursor
- Click on the face area first (might need focus)
- Check that configuration matches in `useGazeTracking.js`
- Verify all images generated successfully

## 📚 Next Steps

- Read the full [README.md](./README.md) for advanced usage
- Check [examples/](./examples/) for more implementations
- Customize styling in `FaceTracker.css`
- Try different grid densities

## 💰 Cost

- Default settings: ~$0.01 (121 images)
- Smoother (step 2.5): ~$0.02 (169 images)
- Free tier usually covers initial testing!

## 🆘 Need Help?

- Check the [README.md](./README.md)
- Open an issue on GitHub
- See [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**Estimated total time:** 5-10 minutes
**Cost:** ~$0.01-0.02
**Difficulty:** Easy ⭐

Ready? Let's go! 🚀

