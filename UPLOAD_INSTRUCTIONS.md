# Upload CTF Terminal to PyPI - Instructions

## 🚀 Quick Upload Steps

### Step 1: Create PyPI Account (if you don't have one)
1. Go to: https://pypi.org/account/register/
2. Create account and verify email

### Step 2: Get API Token (Recommended - More Secure)
1. Go to: https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: "ctf-term-upload"
4. Scope: "Entire account" or "project:ctf-term"
5. Copy the token (you won't see it again!)

### Step 3: Upload to PyPI

Open terminal and run:

```bash
cd /home/vision2030/Desktop/ctf
twine upload dist/*
```

When prompted:
- **Username**: `__token__` (for API token) or your PyPI username
- **Password**: Your API token or PyPI password

## 📋 Alternative: Using the Script

```bash
cd /home/vision2030/Desktop/ctf
./upload_pypi_now.sh
```

Follow the prompts and enter your credentials.

## ✅ Verify Upload

After upload completes:

1. **Check PyPI**: https://pypi.org/project/ctf-term/
2. **Test installation**:
   ```bash
   pip install ctf-term
   ctf version
   ```

## 🎯 Complete Command Reference

```bash
# Navigate to project
cd /home/vision2030/Desktop/ctf

# Verify packages are ready
ls -lh dist/

# Upload to production PyPI
twine upload dist/*

# Enter credentials when prompted
```

## 📊 What Gets Uploaded

- **Package**: ctf-term v0.1.0
- **Size**: ~26-27 KB
- **Type**: Source distribution (.tar.gz) + Wheel (.whl)
- **Python**: >=3.10
- **License**: MIT

## 🌐 After Upload

Your package will be available at:
- **PyPI**: https://pypi.org/project/ctf-term/
- **Install**: `pip install ctf-term`

## 💡 Need Help?

If you encounter issues:
- Check: https://pypi.org/help/
- Verify: Account is confirmed
- Test: Upload to TestPyPI first

## 🎉 Success!

Once uploaded, users worldwide can:
```bash
pip install ctf-term
ctf init
ctf list
ctf tui
```

