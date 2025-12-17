# Deploying Portfolio Optimizer to PythonAnywhere

This guide will walk you through deploying your Portfolio Optimizer application to PythonAnywhere.

## 📋 Prerequisites

1. A PythonAnywhere account (free or paid)
2. Your project files ready for deployment
3. Basic knowledge of PythonAnywhere's web interface

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Project Locally

1. **Build the React frontend:**
   ```bash
   npm run build
   ```
   This creates a `build` folder with static files.

2. **Verify the build folder exists:**
   - Check that `build/index.html` exists
   - Check that `build/static/` contains CSS and JS files

### Step 2: Upload Files to PythonAnywhere

#### Option A: Using Git (Recommended)

**Option A1: Using SSH (if you have SSH keys set up)**
1. In PythonAnywhere, open a Bash console
2. Clone your repository:
   ```bash
   cd ~
   git clone git@github.com:organiccertified/portfolio_optimizer.git
   cd portfolio_optimizer
   ```

**Option A2: Using HTTPS with Personal Access Token (Easier)**
1. Create a GitHub Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name (e.g., "PythonAnywhere")
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again!)

2. In PythonAnywhere, open a Bash console
3. Clone your repository (use the token as password when prompted):
   ```bash
   cd ~
   git clone https://github.com/organiccertified/portfolio_optimizer.git
   cd portfolio_optimizer
   ```
   When prompted for username: enter your GitHub username
   When prompted for password: paste your Personal Access Token

**Option A3: Set up SSH keys on PythonAnywhere**
If you prefer SSH, set up keys first:
1. In PythonAnywhere Bash console, generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location
   # Optionally set a passphrase (or press Enter for no passphrase)
   ```
2. Display your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
3. Copy the output and add it to GitHub:
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your key and save
4. Test the connection:
   ```bash
   ssh -T git@github.com
   ```
5. Now you can clone using SSH:
   ```bash
   cd ~
   git clone git@github.com:organiccertified/portfolio_optimizer.git
   cd portfolio_optimizer
   ```

#### Option B: Using File Upload
1. Go to **Files** tab in PythonAnywhere dashboard
2. Upload your project files:
   - Upload the entire `backend` folder
   - Upload the `build` folder (from `npm run build`)
   - Upload `backend/production_requirements.txt`

### Step 3: Install Python Dependencies

1. Open a **Bash console** in PythonAnywhere
2. Navigate to your project:
   ```bash
   cd ~/portfolioOptimizer  # or your project path
   ```
3. **Choose one installation method:**

   **Option A: With Virtual Environment (Recommended)**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   cd backend
   pip install -r production_requirements.txt
   # Note: NO --user flag when using virtualenv!
   ```

   **Option B: Without Virtual Environment (User Install)**
   ```bash
   cd backend
   pip install --user -r production_requirements.txt
   # Note: Use --user flag when NOT using virtualenv
   ```

### Step 4: Configure the Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose:
   - **Python 3.10** (or latest available)
   - **Flask**
   - Enter a name for your app (e.g., `portfolio-optimizer`)

### Step 5: Set Up WSGI Configuration

1. **Update wsgi.py with your username:**
   - Open `wsgi.py` in your project
   - Replace `yourusername` with your actual PythonAnywhere username
   - Example: If your username is `john`, change:
     ```python
     project_home = '/home/john/portfolioOptimizer'
     ```

2. **Upload wsgi.py to PythonAnywhere:**
   - Upload `wsgi.py` to your project root directory
   - Or copy its contents to the WSGI file in PythonAnywhere

3. **Configure in PythonAnywhere:**
   - In the **Web** tab, find **WSGI configuration file**
   - Click on it to edit
   - Replace the content with the code from your `wsgi.py`
   - Make sure the path matches your actual project location

### Step 6: Configure Static Files

1. In the **Web** tab, scroll to **Static files**
2. Add static file mappings:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/portfolioOptimizer/build/static/`
3. Add another mapping for the root:
   - **URL:** `/`
   - **Directory:** `/home/yourusername/portfolioOptimizer/build/`

### Step 7: Update React App for Production

The React app needs to use relative URLs instead of `localhost:5000`. 

**Option 1: Use the updated production build**
- The production app already uses relative URLs
- Make sure you're using `production_app.py` which serves static files

**Option 2: Update API calls manually**
- Replace `http://localhost:5000/api` with `/api` in all React files
- Rebuild: `npm run build`

### Step 8: Reload Web App

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Your app should now be live at: `https://yourusername.pythonanywhere.com`

## 📁 Project Structure on PythonAnywhere

Your project should look like this:
```
/home/yourusername/portfolio_optimizer/
├── backend/
│   ├── production_app.py
│   └── production_requirements.txt
├── build/
│   ├── index.html
│   └── static/
│       ├── css/
│       └── js/
├── wsgi.py
└── venv/ (optional)
```

**Note:** The repository name is `portfolio_optimizer` (with underscore), so the directory will be `portfolio_optimizer` after cloning.

## 🔧 Configuration Details

### WSGI File Location
The WSGI file should be at:
```
/home/yourusername/portfolio_optimizer/wsgi.py
```

### Flask App Path
The Flask app is at:
```
/home/yourusername/portfolio_optimizer/backend/production_app.py
```

### Static Files
Static files are served from:
```
/home/yourusername/portfolio_optimizer/build/
```

**Important:** Update `wsgi.py` with your actual PythonAnywhere username and the correct directory name (`portfolio_optimizer`).

## 🐛 Troubleshooting

### Issue: "Module not found" or "ModuleNotFoundError"
**Solution:**
1. **Check which Python version your web app uses:**
   - Go to **Web** tab → Your web app
   - Look at the Python version (e.g., Python 3.10)
   - Make sure you install packages for the SAME version

2. **Install for the correct Python version:**
   ```bash
   # Check your Python version
   python3.10 --version  # or python3.9, python3.11, etc.
   
   # Install using the SAME version as your web app
   python3.10 -m pip install --user flask-cors
   # OR if your web app uses 3.9:
   python3.9 -m pip install --user flask-cors
   ```

3. **Install all requirements:**
   ```bash
   cd ~/portfolio_optimizer/backend
   python3.10 -m pip install --user -r production_requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python3.10 -m pip list | grep flask-cors
   ```
   Should show `flask-cors` in the list

5. **If using virtualenv:**
   ```bash
   cd ~/portfolio_optimizer
   source venv/bin/activate
   pip install flask-cors
   # Make sure your WSGI file activates the venv!
   ```

6. **Check PythonAnywhere's help page:**
   - Visit: https://help.pythonanywhere.com/pages/DebuggingImportError/
   - This has specific instructions for PythonAnywhere

### Issue: "Can not perform a '--user' install. User site-packages are not visible in this virtualenv."
**Solution:**
This error occurs when you use `--user` flag inside a virtual environment. You have two options:

**Option 1: Remove --user flag (if using virtualenv)**
```bash
# Make sure virtualenv is activated
source venv/bin/activate
# Then install without --user
pip install -r production_requirements.txt
```

**Option 2: Don't use virtualenv (use --user)**
```bash
# Deactivate virtualenv first
deactivate
# Then install with --user
pip install --user -r production_requirements.txt
```

**Remember:** 
- ✅ Use `--user` when NOT in a virtualenv
- ❌ Don't use `--user` when IN a virtualenv

### Issue: "404 Not Found" for static files
**Solution:**
- Check static file mappings in Web tab
- Verify the build folder path is correct
- Ensure files were uploaded correctly

### Issue: "500 Internal Server Error" for API endpoints
**Solution:**
1. **Check PythonAnywhere error logs:**
   - Go to **Web** tab → **Error log**
   - Look for the actual error message (this will tell you what's wrong)
   - Common errors:
     - `ModuleNotFoundError`: Missing dependencies
     - `FileNotFoundError`: Missing build folder
     - `ImportError`: Wrong import path

2. **Verify dependencies are installed:**
   ```bash
   cd ~/portfolio_optimizer/backend
   pip list | grep flask
   pip list | grep flask-cors
   ```
   If missing, install: `pip install -r production_requirements.txt`

3. **Check if build folder exists:**
   ```bash
   cd ~/portfolio_optimizer
   ls -la build/
   ```
   If missing, you need to build the React app locally and upload it

4. **Check static folder path:**
   - In `production_app.py`, line 15: `static_folder='../build'`
   - This should point to: `/home/yourusername/portfolio_optimizer/build`
   - Verify the path is correct relative to where the app runs

5. **Test the app directly:**
   ```bash
   cd ~/portfolio_optimizer
   python3 backend/production_app.py
   ```
   This will show you the actual error

### Issue: "API calls failing" or "404 NOT FOUND" for API endpoints
**Solution:**
1. **Check if changes are deployed:**
   ```bash
   cd ~/portfolio_optimizer
   git pull  # Make sure you have the latest code
   ```

2. **Verify the WSGI file is using production_app.py:**
   - In PythonAnywhere Web tab, check WSGI configuration file
   - Should have: `from backend.production_app import app as application`
   - NOT: `from backend.optimized_app import app`

3. **Check PythonAnywhere error logs:**
   - Go to **Web** tab → **Error log**
   - Look for import errors or route errors

4. **Verify route ordering in production_app.py:**
   - API routes (`/api/*`) must be defined BEFORE the catch-all route (`/<path:path>`)
   - Check lines 256-333 should have API routes
   - Lines 334-344 should have static file serving

5. **Reload the web app:**
   - Go to **Web** tab
   - Click the green **Reload** button
   - Wait a few seconds for it to restart

6. **Test the API directly:**
   - Visit: `https://mojon.pythonanywhere.com/api/health`
   - Should return JSON, not 404

7. **Check CORS is enabled:**
   - In `production_app.py`, line 16 should have: `CORS(app)`

8. **Verify static folder path:**
   - In `production_app.py`, line 15: `static_folder='../build'`
   - Make sure `build` folder exists in project root

### Issue: "App not loading"
**Solution:**
1. Check error logs in **Web** tab → **Error log**
2. Verify WSGI file path is correct
3. Check that `production_app.py` exists and is accessible
4. Reload the web app

### Issue: "Permission denied (publickey)" when cloning with SSH
**Solution:**
This means SSH keys aren't set up on PythonAnywhere. You have two options:

**Option 1: Use HTTPS instead (Easier)**
```bash
git clone https://github.com/organiccertified/portfolio_optimizer.git
# Use your GitHub username and Personal Access Token when prompted
```

**Option 2: Set up SSH keys**
1. Generate SSH key on PythonAnywhere:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter for default location, optionally set passphrase
   ```
2. Display and copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
3. Add to GitHub:
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste the key and save
4. Test: `ssh -T git@github.com`
5. Now clone with SSH: `git clone git@github.com:organiccertified/portfolio_optimizer.git`

## 📝 Important Notes

1. **Free Account Limitations:**
   - Your app will sleep after inactivity
   - External URLs must be whitelisted (for API calls)
   - Limited CPU time

2. **API Endpoints:**
   - All API routes should start with `/api/`
   - The production app serves both static files and API

3. **CORS:**
   - CORS is enabled in `production_app.py`
   - Should work for same-origin requests

4. **Updates:**
   - After making changes, rebuild: `npm run build`
   - Upload new `build` folder
   - Reload web app in PythonAnywhere

## 🔄 Updating Your Deployment

1. Make changes to your code
2. Rebuild React app: `npm run build`
3. Upload new files (or pull from Git)
4. Reload web app in PythonAnywhere dashboard

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere error logs
2. Check server logs in Bash console
3. Verify all paths are correct
4. Test the Flask app locally first

## ✅ Verification Checklist

- [ ] React app built successfully (`build` folder exists)
- [ ] All files uploaded to PythonAnywhere
- [ ] Dependencies installed
- [ ] WSGI file configured correctly
- [ ] Static files mapped correctly
- [ ] Web app reloaded
- [ ] App accessible at your PythonAnywhere URL
- [ ] API endpoints working (`/api/health`)

