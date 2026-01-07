# 🚀 Deploying Portfolio Optimizer to Hostinger

This guide will help you deploy the Portfolio Optimizer to Hostinger hosting.

## 📋 Prerequisites

- Hostinger hosting account with Python support
- File Manager access or FTP client
- Basic knowledge of web hosting

## 🛠️ Step 1: Prepare Production Build

### **Option A: Use Hostinger Deployment Script (Recommended)**

**Windows:**
```bash
# Run the Hostinger deployment script
deploy_hostinger.bat
```

**Linux/Mac:**
```bash
# Make script executable
chmod +x deploy_hostinger.sh

# Run the Hostinger deployment script
./deploy_hostinger.sh
```

This script will:
- Build the React application
- Create the production folder structure
- Copy all necessary files including `passenger_wsgi.py` and `.htaccess`
- Prepare everything for upload

### **Option B: Use General Production Build Script**
```bash
# Run the production build script (Windows)
build_production.bat
```

### **Option C: Manual Build**
```bash
# 1. Install dependencies
npm install

# 2. Build React app
npm run build

# 3. Create production folder
mkdir production
mkdir production/backend
mkdir production/build

# 4. Copy files
cp -r build/* production/build/
cp backend/production_app.py production/backend/
cp backend/production_requirements.txt production/backend/
cp passenger_wsgi.py production/
cp .htaccess production/
```

## 🌐 Step 2: Hostinger Setup

### **2.1 Access File Manager**
1. Log into your Hostinger control panel
2. Go to **File Manager**
3. Navigate to your domain's `public_html` folder

### **2.2 Upload Files**
1. Upload all contents from the `production` folder to `public_html`
2. Your structure should look like:
   ```
   public_html/
   ├── build/          (React app files)
   ├── backend/
   │   ├── production_app.py
   │   └── production_requirements.txt
   └── index.html      (if not in build folder)
   ```

## 🐍 Step 3: Python Environment Setup

### **3.1 Enable Python Support**
1. In Hostinger control panel, go to **Advanced** → **Python**
2. Enable Python support for your domain
3. Set Python version to 3.8 or higher

### **3.2 Install Dependencies**
1. Open **Terminal** in File Manager
2. Navigate to your domain folder:
   ```bash
   cd public_html
   ```
3. Install Python dependencies:
   ```bash
   pip install -r backend/production_requirements.txt
   ```

## ⚙️ Step 4: Configure Web Server

### **4.1 Upload Configuration Files**
The deployment scripts will create these files automatically. Upload them to your `public_html` folder:

1. **`.htaccess`** - Apache configuration for URL rewriting
2. **`passenger_wsgi.py`** - Passenger WSGI configuration for Flask

These files are already created in your project root and will be copied to the `production` folder when you run the deployment script.

**Note:** The `.htaccess` file handles React Router routing and API routes. The `passenger_wsgi.py` file is automatically detected by Hostinger's Passenger application server.

## 🚀 Step 5: Start the Application

### **5.1 Automatic Start (Recommended)**
Hostinger's Passenger WSGI will automatically detect and run your Flask application using the `passenger_wsgi.py` file. No manual start is needed!

The application will be automatically served when:
- `passenger_wsgi.py` is in your `public_html` folder
- Python support is enabled in Hostinger control panel
- Dependencies are installed

### **5.2 Manual Testing (Optional)**
If you want to test the app manually in Terminal:
```bash
cd public_html
python backend/production_app.py
```

**Note:** For production, Passenger WSGI handles everything automatically. You don't need to manually start the app.

## 🔧 Step 6: Configure Domain

### **6.1 Set Default Document**
1. Go to **Advanced** → **Default Document**
2. Set `index.html` as the default document

### **6.2 Configure Subdomain (Optional)**
If you want to use a subdomain like `portfolio.yourdomain.com`:
1. Create subdomain in Hostinger control panel
2. Point it to the same `public_html` folder
3. Update the subdomain settings

## 📱 Step 7: Test Your Deployment

### **7.1 Test Frontend**
1. Visit your domain: `https://yourdomain.com`
2. You should see the Portfolio Optimizer interface
3. Test the optimization functionality

### **7.2 Test API**
1. Visit: `https://yourdomain.com/api/health`
2. You should see: `{"status":"healthy","message":"Portfolio Optimizer API is running"}`

## 🛠️ Troubleshooting

### **Common Issues:**

1. **"Module not found" errors**
   - Ensure all dependencies are installed
   - Check Python path configuration

2. **"Permission denied" errors**
   - Set proper file permissions (755 for directories, 644 for files)
   - Check file ownership

3. **"Port already in use" errors**
   - Kill existing Python processes
   - Use a different port if needed

4. **Frontend not loading**
   - Check if `build` folder is uploaded correctly
   - Verify `.htaccess` configuration

5. **API not responding**
   - Check if Python app is running
   - Verify WSGI configuration
   - Check server logs

### **Debug Steps:**

1. **Check Python logs:**
   ```bash
   tail -f /path/to/your/app.log
   ```

2. **Test Python app directly:**
   ```bash
   python backend/production_app.py
   ```

3. **Check file permissions:**
   ```bash
   ls -la public_html/
   ```

## 🔒 Security Considerations

### **Production Security:**
1. **Environment Variables**: Use environment variables for sensitive data
2. **HTTPS**: Ensure SSL certificate is enabled
3. **CORS**: Configure CORS for your specific domain
4. **Rate Limiting**: Consider implementing rate limiting
5. **Input Validation**: All inputs are validated on the backend

### **Recommended Settings:**
```python
# In production_app.py
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

## 📊 Performance Optimization

### **For Better Performance:**
1. **Enable Gzip**: Compress responses
2. **Use CDN**: For static assets
3. **Database Caching**: Consider Redis for caching
4. **Load Balancing**: For high traffic

### **Hostinger Optimizations:**
1. Enable **Cloudflare** for better performance
2. Use **SSD hosting** for faster I/O
3. Enable **HTTP/2** support
4. Configure **browser caching**

## 🔄 Updates and Maintenance

### **Updating the App:**
1. Make changes to your local code
2. Run `deploy_hostinger.bat` (Windows) or `./deploy_hostinger.sh` (Linux/Mac) to rebuild
3. Upload new files from the `production` folder to Hostinger's `public_html`
4. Passenger WSGI will automatically reload the application (no manual restart needed)

### **Monitoring:**
1. Check application logs regularly
2. Monitor server resources
3. Set up uptime monitoring
4. Track API usage

## 📞 Support

### **If you need help:**
1. Check Hostinger documentation
2. Contact Hostinger support
3. Review application logs
4. Test locally first

### **Useful Commands:**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check running processes
ps aux | grep python

# Check disk space
df -h

# Check memory usage
free -h
```

## 🎉 Success!

Once deployed, your Portfolio Optimizer will be available at:
- **Frontend**: `https://yourdomain.com`
- **API**: `https://yourdomain.com/api/health`

The application includes:
- ✅ Advanced portfolio optimization
- ✅ Expected return targeting
- ✅ Multiple selection strategies
- ✅ Real-time caching
- ✅ Responsive design
- ✅ Production-ready security

**Happy Deploying! 🚀📈**







