# ExoHabit-AI 🌌

## 🚀 Project Overview
**ExoHabit-AI** is a Machine Learning web application that predicts the habitability score of exoplanets, ranks them, and provides analytical insights through interactive dashboards and downloadable reports.
The system:

-Predicts habitability score using trained ML model

-Classifies planets as Highly Habitable / Potentially Habitable /Non-Habitable

-Generates ranking among planets

-Displays feature importance

-Exports PDF reports

---

## 🛠️ Tech Stack
* **Language:** Python 
* **Machine Learning:** Scikit-learn / Pandas / NumPy / Xgboost / Joblib
* **Web Framework:** Flask
* **Frontend:** HTML / CSS 
* **Visualization:** Matplotlib / Seaborn
* **Backend:** Flask / Gunicorn(Production Server)
* **Report Generation:** ReportLab
* **Deployment:** Render
---

## 📈 Project Status
- [x] **Phase 0:** Project Initialization & Environment Setup (Completed)
- [x] **Milestone 1:** Data Collection and Management, Data Preprocessing & Feature Engineering  (Completed)
- [x] **Milestone 2:** ML Dataset Preparation, ML Model Development and Evaluation (Completed)
- [x] **Milestone 3:** Backend API(Flask Integration), Frontend UI Development (Completed)
- [x] **Milestone 4:** Visualization & Dashboard, Deployment and Submission (Completed)
---

## 🌍 Live Demo

🔗 Live Application:
https://exohabit.onrender.com

---


## 📊 Features

✅ 1. Habitability Prediction

+Input planetary parameters

+Generates:

           -Habitability score
           
           -Classification
           
           -Rank among planets

✅ 2. Ranking System

+Planets are ranked based on predicted habitability score.

+Ranking logic:

          Higher score → Higher rank

          Automatically recalculated on each prediction

✅ 3. Dashboard Analytics

+Feature Importance Visualization

+Habitability Score Distribution Chart

✅ 4. PDF Report Generation

+Downloadable prediction report

---

## 📁 Project Structure(to run application)

    exohabit-ai/
    │
    ├── backend
    |   ├──app.py
    |   └──static/
    |      ├──style.css
    |
    ├── model/
    │   ├── feature_order.pkl
    │   └── xgboost_model.pkl
    |   └── scaler.pkl
    │
    ├── frontend/
    │   ├── dashboard.html
    │   └── index.html
    │
    ├── requirements.txt
    ├── Procfile
    └── README.md

---
## 🎓 Deployment Guide

Phase: Deploy on Render

1.Create Procfile in project root:

      web: gunicorn backend.app:app
      
2.Go to dashboard.render.com

3.Click New + → Web Service

4.Connect your GitHub repository

5.Configure:

    Name: exohabit
    Runtime: Python 3
    Build Command: pip install -r backend/requirements.txt
    Start Command: gunicorn backend.app:app

6.Click Create Web Service

7.Copy the live URL (https://exohabit.onrender.com)

---

## 🚀 Quick Start

Local Development

1.Install required dependencies/libraries (in terminal run below command)

    pip install -r requirements.txt

2.To run the application(in terminal run below command)

     python backend/app.py

Visit  http://127.0.0.1:5000  in your browser.
