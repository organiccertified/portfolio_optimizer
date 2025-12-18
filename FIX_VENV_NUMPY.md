# Fix: Can not perform a '--user' install in virtualenv

## The Problem

You're in a virtual environment (see `(venv)` in your prompt), and you tried to use `--user` flag. Virtual environments don't allow `--user` installs.

## Solution: Remove `--user` Flag

Since you're already in a virtualenv, just install without `--user`:

```bash
# You're already in the venv (venv) prefix shows it
cd ~/portfolio_optimizer/backend
pip install numpy
```

**Or install all requirements at once:**
```bash
cd ~/portfolio_optimizer/backend
pip install -r production_requirements.txt
```

## Verify Installation

```bash
pip list | grep numpy
```

You should see `numpy` in the output.

## Important: Make Sure Your WSGI File Uses the Virtualenv

Your WSGI file needs to activate the virtualenv. Check your WSGI configuration in PythonAnywhere:

1. Go to **Web** tab → **WSGI configuration file**
2. Make sure it activates the venv at the top:

```python
# Activate virtualenv
activate_this = '/home/mojon/portfolio_optimizer/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Then the rest of your WSGI config...
import sys
import os

project_home = '/home/mojon/portfolio_optimizer'
# ... rest of config
```

## After Installing

1. **Reload your web app:**
   - Go to **Web** tab
   - Click the green **Reload** button
   - Wait 10-15 seconds

2. **Test:**
   - Visit: `https://mojon.pythonanywhere.com/api/health`

## Alternative: Don't Use Virtualenv

If you prefer not to use a virtualenv:

```bash
# Deactivate the venv first
deactivate

# Then install with --user
cd ~/portfolio_optimizer/backend
python3.10 -m pip install --user numpy
```

But using a virtualenv is recommended!

