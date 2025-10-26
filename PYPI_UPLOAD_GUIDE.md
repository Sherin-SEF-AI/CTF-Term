# PyPI Upload Guide - CTF Terminal

## 📦 Packages Ready for Upload

**Location**: `dist/`
- `ctf_term-0.1.0-py3-none-any.whl` (26 KB)
- `ctf_term-0.1.0.tar.gz` (27 KB)

## 🚀 Quick Upload (Choose One Method)

### Method 1: Using the Helper Script

```bash
cd /home/vision2030/Desktop/ctf
./upload_to_pypi.sh
```

### Method 2: Direct Upload to TestPyPI (Recommended First)

```bash
cd /home/vision2030/Desktop/ctf
twine upload --repository testpypi dist/*
```

**TestPyPI URL**: https://test.pypi.org/
**Sign up**: https://test.pypi.org/account/register/

### Method 3: Direct Upload to Production PyPI

```bash
cd /home/vision2030/Desktop/ctf
twine upload dist/*
```

**PyPI URL**: https://pypi.org/
**Sign up**: https://pypi.org/account/register/

## 🔐 Credentials Setup

### Option 1: Use Twine Prompt
When you run `twine upload`, it will prompt for:
- Username: Your PyPI username
- Password: Your PyPI password (or API token)

### Option 2: Use API Token (Recommended)
1. Go to PyPI Account Settings → API tokens
2. Create a new API token
3. Use token as password when prompted

### Option 3: Create ~/.pypirc file
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## 📝 Complete Upload Process

### Step 1: Create PyPI Account
- Visit: https://pypi.org/account/register/
- Verify email
- Go to Account Settings → API tokens → Create API token

### Step 2: Upload to TestPyPI First
```bash
cd /home/vision2030/Desktop/ctf
twine upload --repository testpypi dist/*
```

### Step 3: Test Installation from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ ctf-term
ctf version
```

### Step 4: Upload to Production PyPI
```bash
twine upload dist/*
```

### Step 5: Test Installation from PyPI
```bash
pip install ctf-term
ctf version
ctf init
```

## ✅ Verification Checklist

After uploading, verify:

- [ ] Package appears on PyPI: https://pypi.org/project/ctf-term/
- [ ] Description shows correctly
- [ ] Author information visible
- [ ] Installation works: `pip install ctf-term`
- [ ] CLI works: `ctf version`
- [ ] All features functional

## 🎯 Expected PyPI Page Info

- **Name**: ctf-term
- **Version**: 0.1.0
- **Author**: Sherin Joseph Roy
- **License**: MIT
- **Description**: A terminal-based CTF (Capture The Flag) engine with CLI and TUI interfaces for cybersecurity training
- **Homepage**: https://github.com/Sherin-SEF-AI/CTF-Term
- **Keywords**: ctf, capture-the-flag, cybersecurity, security-training, cli, tui, terminal

## 📊 Package Metrics

```
Package Size: ~26-27 KB
Install Size: ~2-3 MB (with dependencies)
Python Version: >=3.10
Dependencies: 6 packages
```

## 🐛 Troubleshooting

### "Invalid authentication credentials"
- Check your username/password
- Use API token instead of password
- Verify API token has upload permissions

### "HTTPError 400: Bad Request"
- Package name might already exist
- Version already published
- Check metadata in pyproject.toml

### "HTTPError 403: Forbidden"
- Account not verified
- Need to verify email address
- Check API token permissions

## 🔄 Updating Package

When releasing new versions:

1. Update version in `pyproject.toml`
2. Commit changes: `git commit -m "Bump version to 0.1.1"`
3. Create tag: `git tag v0.1.1`
4. Rebuild: `python3 -m build`
5. Upload: `twine upload dist/*`
6. Push tags: `git push --tags`

## 🌐 Post-Upload

After successful upload:

1. Add PyPI badge to README.md
2. Create GitHub release
3. Update documentation
4. Share on social media

### Badge Markdown
```markdown
[![PyPI version](https://badge.fury.io/py/ctf-term.svg)](https://badge.fury.io/py/ctf-term)
```

## 📞 Support

For issues with uploading, check:
- PyPI Help: https://pypi.org/help/
- Twine Docs: https://twine.readthedocs.io/
- Python Packaging Guide: https://packaging.python.org/

## 🎉 Success!

Once uploaded, users worldwide can install with:
```bash
pip install ctf-term
```

**Congratulations! Your CTF Terminal is now on PyPI!** 🚀

