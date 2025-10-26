# CTF Terminal - PyPI Deployment Guide

## 📦 Package Created Successfully!

The pip package has been built and is ready for distribution.

### Build Output
- **Source Distribution**: `dist/ctf_term-0.1.0.tar.gz`
- **Wheel Distribution**: `dist/ctf_term-0.1.0-py3-none-any.whl`

## 🚀 Publishing to PyPI

### Prerequisites
1. PyPI account: https://pypi.org/account/register/
2. Install twine: `pip install twine`
3. Have your credentials ready

### Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ ctf-term
```

### Publish to Production PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Verify installation
pip install ctf-term

# Test the CLI
ctf version
```

## 📋 PyPI Checklist

- [x] Package name: `ctf-term`
- [x] Version: `0.1.0`
- [x] Author metadata in `pyproject.toml`
- [x] Keywords for discoverability
- [x] README.md included
- [x] LICENSE file included
- [x] Repository URL configured
- [x] All dependencies specified
- [x] Entry point configured (`ctf` command)

## 📊 Package Information

### Metadata
- **Name**: ctf-term
- **Version**: 0.1.0
- **Author**: Sherin Joseph Roy
- **License**: MIT
- **Python**: >=3.10
- **Repository**: https://github.com/Sherin-SEF-AI/CTF-Term

### Dependencies
- typer[all]>=0.9.0
- rich>=13.0.0
- pyyaml>=6.0
- textual>=0.58.0
- tomli (Python <3.11)
- tomli-w>=1.0.0

### Keywords
ctf, capture-the-flag, cybersecurity, security-training, cli, tui, terminal, textual, typer, python, pentesting, hacking, challenges, flags, scoreboard, leaderboard

## 🔄 Updating the Package

When making changes:

1. Update version in `pyproject.toml`
2. Commit changes: `git commit -m "Release v0.1.1"`
3. Create tag: `git tag v0.1.1`
4. Push: `git push && git push --tags`
5. Rebuild: `python3 -m build`
6. Upload: `twine upload dist/*`

## 📝 Post-Publishing

After publishing to PyPI:

1. Update README with PyPI badge
2. Add to GitHub repository description
3. Create release notes on GitHub
4. Share on social media (LinkedIn, X, Mastodon)
5. Submit to awesome-lists (awesome-ctf, awesome-python)

## 🌐 Installation Methods

### From PyPI
```bash
pip install ctf-term
```

### From GitHub
```bash
pip install git+https://github.com/Sherin-SEF-AI/CTF-Term.git
```

### From Source
```bash
git clone https://github.com/Sherin-SEF-AI/CTF-Term.git
cd CTF-Term
pip install -e .
```

## 📚 Documentation

- **README**: Complete usage guide
- **AUTHORS**: Author information
- **CONTRIBUTING**: Contribution guidelines
- **FEATURES**: Planned features

## 🔗 Links

- **GitHub**: https://github.com/Sherin-SEF-AI/CTF-Term
- **PyPI**: https://pypi.org/project/ctf-term/
- **Author**: https://sherinjosephroy.link
- **Company**: https://deepmost.ai

## ✅ Verification

After publishing, verify:

```bash
# Install from PyPI
pip install ctf-term

# Check version
ctf version

# Initialize
ctf init

# Import challenges
ctf import-pack ~/.ctf/packs/sample.yml

# List challenges
ctf list

# View scoreboard
ctf scoreboard

# Launch TUI
ctf tui
```

## 🎉 Success!

Once published, users can install with:
```bash
pip install ctf-term
```

And use it with:
```bash
ctf init
ctf list
ctf tui
```

