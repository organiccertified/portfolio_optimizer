# WSGI configuration file for PythonAnywhere
# This file should be placed in your project root directory
# Project path: /home/mojon/portfolio_optimizer/
# URL: mojon.pythonanywhere.com
# Repository: git@github.com:organiccertified/portfolio_optimizer.git

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
# IMPORTANT: This must be AFTER setting up the paths!
from backend.production_app import app as application

# For debugging (remove in production if needed)
if __name__ == "__main__":
    application.run()
