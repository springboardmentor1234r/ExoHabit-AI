# Deployment Guide for ExoHabit AI

This guide covers multiple deployment options for your ExoHabit AI application.

## Table of Contents
1. [Option 1: Render (Recommended - Free)](#option-1-render-recommended---free)
2. [Option 2: Heroku](#option-2-heroku)
3. [Option 3: PythonAnywhere](#option-3-pythonanywhere)
4. [Option 4: Docker](#option-4-docker)
5. [Option 5: AWS Elastic Beanstalk](#option-5-aws-elastic-beanstalk)

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

## Option 3: PythonAnywhere

PythonAnywhere is beginner-friendly and offers a free tier.

### Step 1: Sign Up

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account
3. Go to the Dashboard

### Step 2: Upload Your Code

1. Open a Bash console from the Dashboard
2. Clone your repository:
```bash
git clone https://github.com/yourusername/ExoHabit-AI.git
cd ExoHabit-AI
```

3. Create a virtual environment:
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Web App

1. Go to the **Web** tab
2. Click "Add a new web app"
3. Select "Manual configuration"
4. Choose Python 3.9

5. In the **Code** section:
   - **Source code**: `/home/yourusername/ExoHabit-AI`
   - **Working directory**: `/home/yourusername/ExoHabit-AI`

6. In **WSGI configuration file**:
   - Click the link to edit the WSGI file
   - Replace the content with:

```python
import sys
path = '/home/yourusername/ExoHabit-AI'
if path not in sys.path:
    sys.path.append(path)

from backend.app import app as application
```

7. **Virtualenv**: `/home/yourusername/ExoHabit-AI/venv`

8. Click **Reload** to start your app

---

## Option 4: Docker

Docker provides a containerized deployment that works anywhere.

### Step 1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Change to backend directory and run
WORKDIR /app/backend
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Step 2: Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
.git
.gitignore
.github
.pytest_cache
.coverage
htmlcov
.DS_Store
```

### Step 3: Build and Run Locally

```bash
# Build the image
docker build -t exohabit-ai .

# Run the container
docker run -p 5000:5000 exohabit-ai

# Access at http://localhost:5000
```

### Step 4: Deploy to Docker Hub + Cloud Provider

1. **Push to Docker Hub**:
```bash
docker tag exohabit-ai yourusername/exohabit-ai
docker login
docker push yourusername/exohabit-ai
```

2. **Deploy to any cloud provider** (AWS ECS, Google Cloud Run, DigitalOcean, etc.)

**Example - Deploy to DigitalOcean App Platform**:
```bash
# Install doctl CLI
# Create app spec file
```

---

## Option 5: AWS Elastic Beanstalk

AWS offers a free tier for 12 months.

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB Application

```bash
cd ExoHabit-AI
eb init -p python-3.9 exohabit-ai
```

### Step 3: Create Configuration Files

**Procfile**:
```
web: cd backend && gunicorn app:app
```

**.ebextensions/python.config**:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: backend.app:app
```

### Step 4: Deploy

```bash
# Create environment and deploy
eb create exohabit-ai-env

# Open in browser
eb open

# To update
ebt deploy
```

---

## Environment Variables

If your app needs environment variables (for production secrets):

### Local Development
Create `.env` file in backend folder:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### Production Platforms

**Render**: Go to Dashboard → Environment → Add Environment Variables

**Heroku**: `heroku config:set SECRET_KEY=your-secret-key`

**PythonAnywhere**: Go to Web tab → Environment variables

**AWS EB**: `eb setenv SECRET_KEY=your-secret-key`

---

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Ensure Flask static folder is correctly configured
   - Check that files are committed to git

2. **Model files not found**
   - Ensure `.joblib` files are not in `.gitignore`
   - Commit model files: `git add *.joblib`

3. **Port binding errors**
   - Use `0.0.0.0` not `localhost` or `127.0.0.1`
   - Use environment variable for port: `port = int(os.environ.get('PORT', 5000))`

4. **Memory issues**
   - Reduce model size or use lighter models
   - Upgrade to paid tier for more memory

### Update Flask app for production

Add this to the bottom of `backend/app.py`:

```python
if __name__ == '__main__':
    load_model()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Static files (CSS, JS) are loading
- [ ] ML model loads successfully
- [ ] Prediction API works (`/predict` endpoint)
- [ ] All sections of website display correctly
- [ ] Mobile responsiveness works
- [ ] Add custom domain (optional)
- [ ] Set up monitoring (optional)

---

## Recommended: Render (Best Free Option)

For most users, **Render** is recommended because:
- ✅ Generous free tier
- ✅ Easy GitHub integration
- ✅ Automatic deployments on git push
- ✅ HTTPS by default
- ✅ Good performance
- ✅ No credit card required

**Quick Deploy to Render**:
1. Push to GitHub
2. Connect repo on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `cd backend && gunicorn app:app`
5. Deploy!

---

## Support

If you encounter issues:
1. Check the platform's documentation
2. Review application logs in the deployment dashboard
3. Test locally with production settings first
4. Check that all files are committed to git

Good luck with your deployment! 🚀
