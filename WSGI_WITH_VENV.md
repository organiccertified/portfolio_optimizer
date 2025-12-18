# WSGI Configuration with Virtual Environment

## Updated WSGI File

The `wsgi.py` file has been updated to automatically detect and use your virtual environment. It will:

1. Look for the venv at `/home/mojon/portfolio_optimizer/venv`
2. Automatically detect the Python version (python3.10, python3.9, etc.)
3. Add the venv's site-packages to the Python path

## Steps to Use

### 1. Make sure NumPy is installed in your venv

```bash
# In PythonAnywhere Bash console
cd ~/portfolio_optimizer
source venv/bin/activate
cd backend
pip install -r production_requirements.txt
```

### 2. Update your WSGI file in PythonAnywhere

1. Go to **Web** tab → **WSGI configuration file**
2. Copy the entire contents of `wsgi.py` from your project
3. Paste it into the WSGI file editor
4. Click **Save**

### 3. Verify PythonAnywhere is using the venv

In PythonAnywhere **Web** tab:
- Check that your web app's Python version matches your venv
- The WSGI file will automatically use the venv's packages

### 4. Reload your web app

- Go to **Web** tab
- Click the green **Reload** button
- Wait 10-15 seconds

### 5. Test

Visit: `https://mojon.pythonanywhere.com/api/health`

## How It Works

The WSGI file now:
- Automatically finds your venv
- Detects the Python version (python3.10, python3.9, etc.)
- Adds the venv's site-packages to `sys.path`
- This makes all packages installed in the venv available

## If You're NOT Using a Virtualenv

If you're not using a virtualenv, the WSGI file will skip the venv setup and work normally. Just make sure packages are installed with `--user` flag:

```bash
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user -r production_requirements.txt
```

