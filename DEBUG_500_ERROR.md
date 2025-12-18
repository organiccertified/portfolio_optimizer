# Debugging 500 Internal Server Error on PythonAnywhere

## Step 1: Check the Error Log (MOST IMPORTANT!)

**This will tell you exactly what's wrong:**

1. Go to **PythonAnywhere Dashboard** → **Web** tab
2. Click on **Error log** (or **Server log**)
3. Look for the most recent error message
4. **Copy the full error traceback** - this is the key!

Common errors you might see:
- `ModuleNotFoundError: No module named 'numpy'`
- `ModuleNotFoundError: No module named 'flask_cors'`
- `ImportError: cannot import name 'CORS' from 'flask_cors'`
- `FileNotFoundError: [Errno 2] No such file or directory: '/home/mojon/portfolio_optimizer/build'`

## Step 2: Verify Dependencies Are Installed

**Check which Python version your web app uses:**
- Go to **Web** tab → Your web app
- Note the Python version (e.g., Python 3.10)

**Install all dependencies for that version:**
```bash
# In PythonAnywhere Bash console
cd ~/portfolio_optimizer/backend

# Check your Python version first
python3.10 --version

# Install all requirements
python3.10 -m pip install --user -r production_requirements.txt
```

**Verify installations:**
```bash
python3.10 -m pip list | grep -E "flask|numpy"
```

You should see:
- `flask`
- `flask-cors`
- `numpy`

## Step 3: Test the Import Directly

**Test if the app can be imported:**
```bash
cd ~/portfolio_optimizer
python3.10 -c "from backend.production_app import app; print('Import successful!')"
```

If this fails, you'll see the exact error.

## Step 4: Check File Paths

**Verify the project structure:**
```bash
cd ~/portfolio_optimizer
ls -la backend/production_app.py
ls -la build/
ls -la wsgi.py
```

All should exist.

## Step 5: Verify WSGI Configuration

1. Go to **Web** tab → **WSGI configuration file**
2. Make sure it has:
   ```python
   project_home = '/home/mojon/portfolio_optimizer'
   from backend.production_app import app as application
   ```

## Step 6: Common Fixes

### Fix 1: Missing numpy
```bash
python3.10 -m pip install --user numpy
```

### Fix 2: Missing flask-cors
```bash
python3.10 -m pip install --user flask-cors
```

### Fix 3: Wrong Python version
- Check your web app's Python version
- Install packages for THAT version (not just `python3`)

### Fix 4: Virtual environment issue
If you're using a virtualenv:
```bash
cd ~/portfolio_optimizer
source venv/bin/activate
pip install -r backend/production_requirements.txt
# Make sure your WSGI file activates the venv!
```

### Fix 5: Build folder missing
If the error mentions the build folder:
```bash
# You need to build the React app locally and upload it
# Or clone the repository which should include the build folder
cd ~/portfolio_optimizer
ls -la build/
```

## Step 7: Reload Web App

After making changes:
1. Go to **Web** tab
2. Click the green **Reload** button
3. Wait 10-15 seconds

## Step 8: Test the API

```bash
# Test health endpoint
curl https://mojon.pythonanywhere.com/api/health

# Or visit in browser:
# https://mojon.pythonanywhere.com/api/health
```

## Still Not Working?

**Share the error log output** and I can help you fix the specific issue!

The error log is the key - it will show exactly what's failing.

