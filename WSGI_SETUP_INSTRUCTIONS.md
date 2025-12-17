# WSGI Setup Instructions for PythonAnywhere

## ✅ Use Your Custom App

**You MUST use:**
```python
from backend.production_app import app as application
```

**NOT the default PythonAnywhere Flask app!**

## Why?

1. **Default PythonAnywhere Flask app** = Just a template/example
2. **Your production_app.py** = Has all your API routes, static file serving, CORS, etc.

## Step-by-Step Setup

### 1. Go to PythonAnywhere Web Tab
- Click on **Web** tab
- Find your web app

### 2. Click on "WSGI configuration file"
- This will open the WSGI file editor

### 3. Replace ALL Content

**Delete everything** in the WSGI file and replace with this:

```python
# WSGI configuration file for PythonAnywhere
import sys
import os

# Add your project directory to the Python path
project_home = '/home/mojon/portfolio_optimizer'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the backend directory to the Python path
backend_path = os.path.join(project_home, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Change to the project directory
os.chdir(project_home)

# Import the Flask application
from backend.production_app import app as application

# For debugging (remove in production if needed)
if __name__ == "__main__":
    application.run()
```

### 4. Click "Save"

### 5. Reload Your Web App
- Go back to **Web** tab
- Click the green **Reload** button
- Wait 10-15 seconds

## What NOT to Use

❌ **Don't use the default PythonAnywhere template:**
```python
from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello():
    return 'Hello from Flask!'
```

This is just an example and won't have your API routes or frontend!

## Verify It's Working

1. **Test API:**
   - Visit: `https://mojon.pythonanywhere.com/api/health`
   - Should return JSON with status: "healthy"

2. **Test Frontend:**
   - Visit: `https://mojon.pythonanywhere.com/`
   - Should show your React app

## Troubleshooting

### If you get import errors:
- Make sure `flask-cors` is installed: `python3.10 -m pip install --user flask-cors`
- Check that `backend/production_app.py` exists

### If routes don't work:
- Make sure you're using `production_app.py`, not `optimized_app.py`
- Check that API routes are defined before static routes in `production_app.py`


