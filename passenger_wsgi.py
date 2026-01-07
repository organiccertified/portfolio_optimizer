"""
Passenger WSGI configuration file for Hostinger deployment.

This file is used by Hostinger's Passenger application server to run
the Flask application. Place this file in your public_html directory
along with the backend folder and build folder.

Hostinger uses Passenger WSGI, which automatically detects this file
and uses it to serve your Flask application.
"""

import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Add the project root to Python path
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Change to the project directory
os.chdir(project_root)

# Import the Flask application
# IMPORTANT: This must be AFTER setting up the paths!
try:
    from backend.production_app import app as application
except ImportError:
    # Fallback: try importing directly if backend is in path
    from production_app import app as application

# For debugging (remove in production if needed)
if __name__ == "__main__":
    application.run()

