# Installation Command Summary

## ✅ Updated Installation Commands

All documentation now uses the standard installation command **without version pinning**:

```bash
pip install ctf-term
```

This will install the **latest version** available on PyPI.

## 📦 Installation Methods

### 1. Standard Installation (Recommended)
```bash
pip install ctf-term
```

### 2. Using pipx (Isolated Environment)
```bash
pipx install ctf-term
```

### 3. From GitHub Source
```bash
pip install git+https://github.com/Sherin-SEF-AI/CTF-Term.git
```

### 4. From Local Source
```bash
git clone https://github.com/Sherin-SEF-AI/CTF-Term.git
cd CTF-Term
pip install -e .
```

## 🔄 Installing Specific Versions

If you need a specific version:

```bash
pip install ctf-term==0.1.0
```

Or version range:

```bash
pip install "ctf-term>=0.1.0"
```

## ✅ Files Updated

- ✅ README.md - Added pip install option
- ✅ All documentation files - Using `pip install ctf-term`
- ✅ Upload scripts - Updated to standard command
- ✅ All guides - Consistent installation instructions

## 🎯 Usage After Installation

```bash
# Check version
ctf version

# Initialize
ctf init

# List challenges
ctf list

# Launch TUI
ctf tui
```

## 📊 Installation Command Coverage

All files checked:
- ✅ Uses `pip install ctf-term` (latest version)
- ✅ No version pinning installed
- ✅ Consistent across all documentation
- ✅ Updated in GitHub repository

