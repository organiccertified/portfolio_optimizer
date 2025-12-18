#!/usr/bin/env python3
"""
Quick diagnostic script to test imports on PythonAnywhere.
Run this from the project root: python3.10 test_imports.py
"""

import sys
import os

print("=" * 60)
print("PythonAnywhere Import Diagnostic Script")
print("=" * 60)
print()

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check current directory
print(f"Current directory: {os.getcwd()}")
print()

# Check project structure
print("Checking project structure...")
project_root = os.path.expanduser('~/portfolio_optimizer')
if os.path.exists(project_root):
    print(f"✅ Project root exists: {project_root}")
    os.chdir(project_root)
else:
    print(f"❌ Project root not found: {project_root}")
    print("   Trying current directory...")
    project_root = os.getcwd()

backend_path = os.path.join(project_root, 'backend')
if os.path.exists(backend_path):
    print(f"✅ Backend directory exists: {backend_path}")
else:
    print(f"❌ Backend directory not found: {backend_path}")

build_path = os.path.join(project_root, 'build')
if os.path.exists(build_path):
    print(f"✅ Build directory exists: {build_path}")
else:
    print(f"⚠️  Build directory not found: {build_path} (frontend may not work)")

print()

# Test standard library imports
print("Testing standard library imports...")
try:
    import json
    print("✅ json")
except ImportError as e:
    print(f"❌ json: {e}")

try:
    import random
    print("✅ random")
except ImportError as e:
    print(f"❌ random: {e}")

try:
    import time
    print("✅ time")
except ImportError as e:
    print(f"❌ time: {e}")

try:
    from datetime import datetime
    print("✅ datetime")
except ImportError as e:
    print(f"❌ datetime: {e}")

try:
    from typing import Dict, List, Optional, Tuple
    print("✅ typing")
except ImportError as e:
    print(f"❌ typing: {e}")

try:
    import logging
    print("✅ logging")
except ImportError as e:
    print(f"❌ logging: {e}")

print()

# Test Flask imports
print("Testing Flask imports...")
try:
    from flask import Flask, request, jsonify, send_from_directory
    print("✅ flask")
    print(f"   Flask version: {Flask.__version__ if hasattr(Flask, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"❌ flask: {e}")
    print("   Install with: python3.10 -m pip install --user flask")

try:
    from flask_cors import CORS
    print("✅ flask-cors")
except ImportError as e:
    print(f"❌ flask-cors: {e}")
    print("   Install with: python3.10 -m pip install --user flask-cors")

print()

# Test NumPy import
print("Testing NumPy import...")
try:
    import numpy as np
    print("✅ numpy")
    print(f"   NumPy version: {np.__version__}")
except ImportError as e:
    print(f"❌ numpy: {e}")
    print("   Install with: python3.10 -m pip install --user numpy")

print()

# Test importing the production app
print("Testing production_app import...")
try:
    # Add project root to path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Add backend to path
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    # Change to project root
    os.chdir(project_root)
    
    from backend.production_app import app
    print("✅ Successfully imported production_app!")
    print(f"   App name: {app.name}")
    print(f"   Static folder: {app.static_folder}")
except ImportError as e:
    print(f"❌ Failed to import production_app: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Error importing production_app: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print()
print("If any imports failed, install them with:")
print("  python3.10 -m pip install --user <package-name>")
print()
print("Or install all at once:")
print("  cd ~/portfolio_optimizer/backend")
print("  python3.10 -m pip install --user -r production_requirements.txt")

