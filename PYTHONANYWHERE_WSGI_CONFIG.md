# PythonAnywhere WSGI Configuration

## Your Configuration

- **Username:** mojon
- **Project Path:** `/home/mojon/portfolio_optimizer/`
- **URL:** `mojon.pythonanywhere.com`

## WSGI File Setup

### 1. Copy wsgi.py to PythonAnywhere

The `wsgi.py` file in your project root is already configured with your path:
```python
project_home = '/home/mojon/portfolio_optimizer'
```

### 2. Configure in PythonAnywhere Dashboard

1. Go to **Web** tab in PythonAnywhere
2. Find **WSGI configuration file** link
3. Click on it to edit
4. Replace the entire content with the contents of `wsgi.py` from your project
5. Make sure it has:
   ```python
   project_home = '/home/mojon/portfolio_optimizer'
   from backend.production_app import app as application
   ```

### 3. Static Files Configuration

In **Web** tab → **Static files**, add these mappings:

1. **URL:** `/static/`
   **Directory:** `/home/mojon/portfolio_optimizer/build/static/`

2. **URL:** `/`
   **Directory:** `/home/mojon/portfolio_optimizer/build/`

### 4. Reload Web App

- Click the green **Reload** button
- Wait 10-15 seconds

## Verify Setup

1. **Check paths exist:**
   ```bash
   cd ~/portfolio_optimizer
   ls -la backend/production_app.py
   ls -la build/
   ls -la wsgi.py
   ```

2. **Test API:**
   - Visit: `https://mojon.pythonanywhere.com/api/health`
   - Should return JSON

3. **Test Frontend:**
   - Visit: `https://mojon.pythonanywhere.com/`
   - Should show your React app

## Troubleshooting

### If you get import errors:
- Make sure `flask-cors` is installed: `python3.10 -m pip install --user flask-cors`
- Check Python version matches your web app

### If static files don't load:
- Verify build folder exists: `ls -la ~/portfolio_optimizer/build/`
- Check static file mappings in Web tab

### If API returns 404:
- Check route ordering in `production_app.py` (API routes must be before static routes)
- Reload web app

