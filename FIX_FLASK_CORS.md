# Fix: ModuleNotFoundError: No module named 'flask_cors'

## Quick Fix Steps

### 1. Check Your Web App's Python Version
- Go to **PythonAnywhere Dashboard** → **Web** tab
- Look at your web app configuration
- Note the Python version (e.g., Python 3.10, 3.9, 3.11)

### 2. Open Bash Console
- Click on **Bash** tab in PythonAnywhere dashboard
- Or go to **Consoles** → **Bash**

### 3. Install flask-cors for the Correct Python Version

**Replace `3.10` with YOUR web app's Python version:**

```bash
# Install flask-cors
python3.10 -m pip install --user flask-cors

# Also install flask if not already installed
python3.10 -m pip install --user flask

# Or install all requirements at once
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user -r production_requirements.txt
```

### 4. Verify Installation
```bash
python3.10 -m pip list | grep flask-cors
```

You should see: `flask-cors` in the output.

### 5. Reload Your Web App
- Go to **Web** tab
- Click the green **Reload** button
- Wait 10-15 seconds

### 6. Test
Visit: `https://mojon.pythonanywhere.com/api/health`

## Common Issues

### Issue: "Command not found: python3.10"
**Solution:** Try:
- `python3.9 -m pip install --user flask-cors`
- `python3.11 -m pip install --user flask-cors`
- Or check which Python versions are available: `ls /usr/bin/python*`

### Issue: "Permission denied"
**Solution:** Make sure you're using `--user` flag:
```bash
python3.10 -m pip install --user flask-cors
```

### Issue: Still getting error after installation
**Solution:**
1. Check you're using the EXACT Python version your web app uses
2. Verify installation: `python3.10 -m pip list | grep flask-cors`
3. Check PythonAnywhere help: https://help.pythonanywhere.com/pages/DebuggingImportError/

## Alternative: Make CORS Optional

If you can't install flask-cors, we can make it optional. But this is NOT recommended as CORS is needed for API to work properly.

## Still Having Issues?

1. Check PythonAnywhere's official help:
   https://help.pythonanywhere.com/pages/DebuggingImportError/

2. Verify your Python version matches:
   - Web tab → Your web app → Check Python version
   - Bash console → `python3.10 --version` (use your version)

3. Try installing in a virtual environment:
   ```bash
   cd ~/portfolio_optimizer
   python3.10 -m venv venv
   source venv/bin/activate
   pip install flask-cors flask
   ```
   Then update your WSGI file to activate the venv.

