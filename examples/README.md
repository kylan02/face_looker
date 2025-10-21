# Face Looker Examples

This directory contains various implementation examples for the Face Looker project.

## 📁 Examples

### 1. Basic React Implementation (`react-basic/`)

The simplest way to implement face tracking in your React app.

**Features:**
- Basic FaceTracker component usage
- Debug mode demonstration
- Responsive design
- Touch support

**Files:**
- `App.jsx` - Main application component
- `App.css` - Styling

### 2. TypeScript Implementation (`typescript/`)

TypeScript version with full type safety.

**Features:**
- Full TypeScript types
- Type-safe props
- Better IDE autocomplete
- Production-ready code

### 3. Next.js Implementation (`nextjs/`)

Optimized for Next.js with server-side rendering considerations.

**Features:**
- Next.js Image optimization (optional)
- SSR-safe implementation
- App Router compatible
- Dynamic imports

### 4. Multiple Faces (`multiple-faces/`)

Example showing multiple face trackers on one page.

**Features:**
- Multiple independent face trackers
- Different configurations
- Performance optimization

### 5. Custom Styling (`custom-styling/`)

Advanced styling examples.

**Features:**
- Circular masks
- Border effects
- Animations
- Hover effects

## 🚀 Quick Start

1. **Generate your faces first:**
```bash
cd ../
python main.py --image ./my_face.jpg --out ./out
```

2. **Copy faces to your React project:**
```bash
cp -r ./out/faces /path/to/your-react-app/public/
```

3. **Copy the example you want:**
```bash
# For basic React
cp examples/react-basic/* /path/to/your-react-app/src/

# For TypeScript
cp examples/typescript/* /path/to/your-react-app/src/
```

4. **Install dependencies** (if needed):
```bash
npm install
# or
yarn install
```

## 💡 Tips

- Start with `react-basic` if you're new to the project
- Use `typescript` for production applications
- Check `custom-styling` for inspiration on making it unique
- `multiple-faces` shows how to handle multiple instances

## 🔧 Configuration

All examples assume:
- Face images in `/public/faces/`
- Default grid parameters (`-15` to `15`, step `3`)
- 256×256 image size

If you changed generation parameters, update the constants in `useGazeTracking.js`.

## 📚 Learn More

See the main [README.md](../README.md) for full documentation.

