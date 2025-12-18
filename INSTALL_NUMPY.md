# Fix: ModuleNotFoundError: No module named 'numpy'

## Quick Fix

**The error shows numpy is missing. Install it now:**

### Step 1: Check Your Web App's Python Version

1. Go to **PythonAnywhere Dashboard** → **Web** tab
2. Look at your web app configuration
3. Note the Python version (e.g., Python 3.10, 3.9, 3.11)

### Step 2: Install NumPy

**In PythonAnywhere Bash console, run:**

```bash
# Replace 3.10 with YOUR web app's Python version
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user numpy
```

**Or install all requirements at once:**
```bash
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user -r production_requirements.txt
```

This will install:
- flask
- flask-cors
- numpy
- gunicorn

### Step 3: Verify Installation

```bash
python3.10 -m pip list | grep numpy
```

You should see: `numpy` in the output.

### Step 4: Reload Your Web App

1. Go to **Web** tab
2. Click the green **Reload** button
3. Wait 10-15 seconds

### Step 5: Test

Visit: `https://mojon.pythonanywhere.com/api/health`

Should return JSON now!

## If You Get "Command not found: python3.10"

Try:
- `python3.9 -m pip install --user numpy`
- `python3.11 -m pip install --user numpy`
- Or check which Python versions are available: `ls /usr/bin/python*`

## If You're Using a Virtual Environment

If you're using a virtualenv, activate it first:
```bash
cd ~/portfolio_optimizer
source venv/bin/activate
pip install numpy
# Make sure your WSGI file activates the venv!
```

