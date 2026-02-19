# Deployment Configuration

This directory contains deployment configuration files for hosting the backend API.

## Files

- `Procfile` — Process definition for Heroku/Render (runs Gunicorn)

## Deploying the Backend

1. Push the `backend/` directory to a hosting platform (Render, Railway, Heroku).
2. Set the root directory to `backend/`.
3. The platform will use `requirements.txt` from `backend/` and the `Procfile` from this directory.

## Deploying the Frontend

The frontend is a static Vite build:

```bash
npm run build
```

Deploy the contents of `dist/` to any static host (Vercel, Netlify, GitHub Pages).
