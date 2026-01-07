# Hostinger Quick Start Guide

## 🚀 Quick Deployment Steps

### 1. Prepare Locally

**Windows:**
```bash
deploy_hostinger.bat
```

**Linux/Mac:**
```bash
chmod +x deploy_hostinger.sh
./deploy_hostinger.sh
```

This will:
- Build the React app
- Create a `production` folder with all necessary files
- Include `passenger_wsgi.py` and `.htaccess` for Hostinger

### 2. Upload to Hostinger

1. Log into Hostinger control panel
2. Go to **File Manager**
3. Navigate to your domain's `public_html` folder
4. Upload **all contents** from the `production` folder to `public_html`

Your structure should look like:
```
public_html/
├── build/          (React app files)
├── backend/
│   ├── production_app.py
│   └── production_requirements.txt
├── passenger_wsgi.py
└── .htaccess
```

### 3. Enable Python Support

1. In Hostinger control panel, go to **Advanced** → **Python**
2. Enable Python support for your domain
3. Set Python version to **3.8 or higher**

### 4. Install Dependencies

1. Open **Terminal** in Hostinger File Manager
2. Navigate to your domain folder:
   ```bash
   cd public_html
   ```
3. Install Python dependencies:
   ```bash
   pip install -r backend/production_requirements.txt
   ```

### 5. Test Your Deployment

1. Visit your domain: `https://yourdomain.com`
2. Test API: `https://yourdomain.com/api/health`
3. You should see the Portfolio Optimizer interface

## ✅ That's It!

Hostinger's Passenger WSGI will automatically detect and run your Flask application using `passenger_wsgi.py`. No manual start needed!

## 🔄 Updating Your App

1. Make changes locally
2. Run `deploy_hostinger.bat` (or `.sh`) again
3. Upload new files from `production` folder to `public_html`
4. Passenger will automatically reload (no restart needed)

## 🐛 Troubleshooting

### "Module not found" errors
- Ensure dependencies are installed: `pip install -r backend/production_requirements.txt`
- Check Python version matches (3.8+)

### Frontend not loading
- Check if `build` folder is uploaded correctly
- Verify `.htaccess` file is in `public_html`

### API not responding
- Check if `passenger_wsgi.py` is in `public_html`
- Verify Python support is enabled
- Check Hostinger error logs

## 📖 For Detailed Instructions

See `HOSTINGER_DEPLOYMENT.md` for comprehensive deployment guide.

