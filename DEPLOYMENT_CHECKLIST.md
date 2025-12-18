# PythonAnywhere Deployment Checklist

## Current Issue: 500 Internal Server Error on `/api/stocks` and `/api/stats`

### Step 1: Check PythonAnywhere Error Logs
1. Go to PythonAnywhere Dashboard → **Web** tab
2. Click **Error log** link
3. Look for the actual error message - this will tell you exactly what's wrong
4. Common errors you might see:
   - `ModuleNotFoundError: No module named 'numpy'` → NumPy not installed
   - `AttributeError` → Code not updated
   - `ImportError` → Wrong import path

### Step 2: Deploy Updated Code

**Option A: Using Git (Recommended)**
```bash
# On your local machine, commit and push:
git add backend/production_app.py backend/production_requirements.txt
git commit -m "Fix target_return strategy and add numpy dependency"
git push origin main

# On PythonAnywhere Bash console:
cd ~/portfolio_optimizer
git pull origin main
```

**Option B: Manual Upload**
1. Go to PythonAnywhere → **Files** tab
2. Navigate to `backend/` folder
3. Upload the updated `production_app.py` file
4. Upload the updated `production_requirements.txt` file

### Step 3: Install NumPy on PythonAnywhere

**Check Python version first:**
```bash
# On PythonAnywhere Bash console
cd ~/portfolio_optimizer
python3.10 --version  # Replace 3.10 with your web app's Python version
```

**Install NumPy:**

**If using virtualenv:**
```bash
cd ~/portfolio_optimizer
source venv/bin/activate
cd backend
pip install numpy>=1.21.0
```

**If NOT using virtualenv:**
```bash
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user numpy>=1.21.0
# Replace 3.10 with your Python version
```

**Or install all requirements:**
```bash
cd ~/portfolio_optimizer/backend
# With virtualenv:
source ../venv/bin/activate
pip install -r production_requirements.txt

# Without virtualenv:
python3.10 -m pip install --user -r production_requirements.txt
```

### Step 4: Verify NumPy Installation
```bash
# On PythonAnywhere Bash console
python3.10 -c "import numpy; print('NumPy version:', numpy.__version__)"
# Should print: NumPy version: 1.21.0 or higher
```

### Step 5: Test the App Directly
```bash
# On PythonAnywhere Bash console
# IMPORTANT: Run from project root, NOT from backend directory
cd ~/portfolio_optimizer
python3.10 backend/production_app.py
# This will show any import errors or runtime errors
# Press Ctrl+C to stop

# OR test the import:
python3.10 -c "import sys; sys.path.insert(0, '.'); from backend.production_app import app; print('Import successful!')"
```

### Step 6: Reload Web App
1. Go to PythonAnywhere Dashboard → **Web** tab
2. Click the green **Reload** button
3. Wait 10-15 seconds for the app to restart

### Step 7: Test Endpoints
1. **Health check:**
   - Visit: `https://mojon.pythonanywhere.com/api/health`
   - Should return JSON with `"status": "healthy"`

2. **Stocks endpoint:**
   - Visit: `https://mojon.pythonanywhere.com/api/stocks`
   - Should return JSON with stocks array

3. **Stats endpoint:**
   - Visit: `https://mojon.pythonanywhere.com/api/stats`
   - Should return JSON with stats

## Troubleshooting

### If you see "ModuleNotFoundError: No module named 'numpy'"
**Solution:** Install NumPy (see Step 3 above)

### If you see "AttributeError" or "NameError"
**Solution:** The code hasn't been updated. Make sure you've deployed the latest `production_app.py`

### If you see "ImportError"
**Solution:** Check that your WSGI file is using `from backend.production_app import app as application`

### If errors persist after all steps
1. Check the error log again (Step 1)
2. Copy the exact error message
3. Test the app directly (Step 5) to see the full traceback
4. Verify all files are in the correct location:
   ```bash
   cd ~/portfolio_optimizer
   ls -la backend/production_app.py
   ls -la backend/production_requirements.txt
   cat backend/production_requirements.txt  # Should show numpy>=1.21.0
   ```

## Quick Fix Script for PythonAnywhere

Run this in PythonAnywhere Bash console:

```bash
cd ~/portfolio_optimizer

# Pull latest code
git pull origin main

# Install/update numpy
cd backend
python3.10 -m pip install --user numpy>=1.21.0

# Verify installation
python3.10 -c "import numpy; print('NumPy OK:', numpy.__version__)"

# Test import
python3.10 -c "from backend.production_app import app; print('Import OK')"

echo "Done! Now reload your web app in the Dashboard."
```

