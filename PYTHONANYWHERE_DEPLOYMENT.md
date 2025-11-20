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
1. In PythonAnywhere, open a Bash console
2. Clone your repository:
   ```bash
   cd ~
   git clone https://github.com/organiccertified/portfolio_optimizer.git
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
3. Create a virtual environment (recommended):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   cd backend
   pip install --user -r production_requirements.txt
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

### Issue: "Module not found"
**Solution:**
- Make sure all dependencies are installed
- Check that you're using the correct Python version
- Verify the virtual environment is activated (if using one)

### Issue: "404 Not Found" for static files
**Solution:**
- Check static file mappings in Web tab
- Verify the build folder path is correct
- Ensure files were uploaded correctly

### Issue: "API calls failing"
**Solution:**
- Check that API routes are prefixed with `/api/`
- Verify CORS is enabled in `production_app.py`
- Check PythonAnywhere error logs

### Issue: "App not loading"
**Solution:**
1. Check error logs in **Web** tab → **Error log**
2. Verify WSGI file path is correct
3. Check that `production_app.py` exists and is accessible
4. Reload the web app

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

