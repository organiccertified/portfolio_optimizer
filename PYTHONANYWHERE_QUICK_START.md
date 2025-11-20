# PythonAnywhere Quick Start Guide

## 🚀 Quick Deployment Steps

### 1. Prepare Locally
```bash
# Build React app
npm run build

# Update wsgi.py with your username
# Change: /home/yourusername/portfolioOptimizer
# To: /home/YOURACTUALUSERNAME/portfolioOptimizer
```

### 2. Upload to PythonAnywhere

**Option A: Git (Recommended)**

**Using HTTPS (Easier - Recommended):**
```bash
# In PythonAnywhere Bash console
cd ~
git clone https://github.com/organiccertified/portfolio_optimizer.git
cd portfolio_optimizer
# When prompted, use your GitHub username and Personal Access Token as password
```

**Using SSH (if keys are set up):**
```bash
# In PythonAnywhere Bash console
cd ~
git clone git@github.com:organiccertified/portfolio_optimizer.git
cd portfolio_optimizer
```

**To set up SSH keys on PythonAnywhere:**
1. Generate key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Display key: `cat ~/.ssh/id_ed25519.pub`
3. Add to GitHub: Settings → SSH and GPG keys → New SSH key
4. Test: `ssh -T git@github.com`

**Option B: File Upload**
- Upload via Files tab in PythonAnywhere dashboard
- Upload: `backend/`, `build/`, `wsgi.py`

### 3. Install Dependencies

**Option A: With Virtual Environment (Recommended)**
```bash
cd ~/portfolio_optimizer
python3.10 -m venv venv
source venv/bin/activate
cd backend
pip install -r production_requirements.txt
# Note: NO --user flag when using virtualenv!
```

**Option B: Without Virtual Environment**
```bash
cd ~/portfolio_optimizer/backend
pip install --user -r production_requirements.txt
# Note: Use --user flag when NOT using virtualenv
```

### 4. Configure Web App

1. Go to **Web** tab → **Add a new web app**
2. Choose: **Python 3.10** + **Flask**
3. Edit **WSGI configuration file**:
   - Copy contents from `wsgi.py`
   - Update username in the path
4. Set **Static files**:
   - URL: `/static/` → Directory: `/home/yourusername/portfolioOptimizer/build/static/`
   - URL: `/` → Directory: `/home/yourusername/portfolioOptimizer/build/`
5. Click **Reload** button

### 5. Test
Visit: `https://yourusername.pythonanywhere.com`

## 📁 Required Files Structure
```
~/portfolio_optimizer/
├── backend/
│   ├── production_app.py
│   └── production_requirements.txt
├── build/
│   ├── index.html
│   └── static/
├── wsgi.py
```

## ⚙️ WSGI File Path
Update this line in `wsgi.py`:
```python
project_home = '/home/YOURUSERNAME/portfolio_optimizer'
```

## 🔧 Static Files Mapping
In Web tab → Static files:
- `/static/` → `/home/yourusername/portfolio_optimizer/build/static/`
- `/` → `/home/yourusername/portfolio_optimizer/build/`

## 🐛 Common Issues

**404 for static files:**
- Check static file mappings
- Verify build folder path

**Module not found:**
- If using virtualenv: `pip install -r backend/production_requirements.txt` (no --user)
- If NOT using virtualenv: `pip install --user -r backend/production_requirements.txt`
- Check Python version matches

**App not loading:**
- Check error log in Web tab
- Verify wsgi.py path is correct
- Reload web app

## 📝 Notes

- Free accounts: App sleeps after inactivity
- Update code: Rebuild (`npm run build`), upload, reload
- API endpoints: All start with `/api/`

For detailed instructions, see `PYTHONANYWHERE_DEPLOYMENT.md`

