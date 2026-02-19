# Deployment Guide for ExoHabit AI

This guide covers multiple deployment options for your ExoHabit AI application.

## Table of Contents
1. [Option 1: Render (Recommended - Free)](#option-1-render-recommended---free)
2. [Option 2: Heroku](#option-2-heroku)
---

## Option 1: Render (Recommended - Free)

Render is a modern cloud platform with a generous free tier.

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to GitHub
2. Add a `Procfile` to your project root:

```bash
# Create Procfile (no extension)
echo "web: cd backend && gunicorn app:app" > Procfile
```

3. Update `requirements.txt` in the root to include gunicorn:

```bash
cd backend
pip freeze > ../requirements.txt
```

Then add gunicorn to requirements.txt:
```
gunicorn==21.2.0
```

4. Add `runtime.txt` to specify Python version:

```bash
echo "python-3.9.18" > runtime.txt
```

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: exohabit-ai
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
5. Click "Create Web Service"
6. Your app will be deployed at `https://exohabit-ai.onrender.com`

---

## Option 2: Heroku

Heroku is user-friendly but no longer offers a free tier (requires credit card).

### Step 1: Install Heroku CLI

```bash
# Windows (with Chocolatey)
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Prepare Your App

1. Login to Heroku:
```bash
heroku login
```

2. Create a Heroku app:
```bash
heroku create exohabit-ai
```

3. Add necessary files:

**runtime.txt** (in project root):
```
python-3.9.18
```

**Procfile** (in project root):
```
web: cd backend && gunicorn app:app
```

4. Install gunicorn and update requirements:
```bash
pip install gunicorn
cd backend
pip freeze > ../requirements.txt
```

### Step 3: Deploy

```bash
# Add and commit changes
git add .
git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
git push heroku main

# Open your app
heroku open
```

---

