# Contributing to Face Looker

Thanks for your interest in contributing! 🎉

## 🐛 Bug Reports

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages (if any)

## 💡 Feature Requests

We welcome feature ideas! Please open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternative solutions you've considered

## 🔧 Pull Requests

### Setup for Development

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/face_looker.git
cd face_looker
```

3. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Testing

Before submitting a PR:
1. Test your changes with different parameters
2. Verify React implementation still works
3. Check that existing functionality isn't broken
4. Test on both Python 3.7+ and latest version

### Documentation

- Update README.md if you add features
- Add examples for new functionality
- Include code comments for complex logic

### Commit Messages

Use clear, descriptive commit messages:
```
Add support for custom image formats

- Added PNG and JPEG output options
- Updated save_resized_webp to handle multiple formats
- Added --format argument to CLI
```

### Submitting

1. Push to your fork:
```bash
git push origin feature/your-feature-name
```

2. Open a Pull Request with:
   - Clear description of changes
   - Why the change is needed
   - Any breaking changes
   - Screenshots (if UI changes)

## 📝 Example Contributions

Good first contributions:
- Add more examples
- Improve documentation
- Fix typos
- Add tests
- Performance improvements

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers
- Focus on the best solution, not winning arguments

## ❓ Questions?

Open an issue with the "question" label or reach out to the maintainers.

Thank you for contributing! 🙏

