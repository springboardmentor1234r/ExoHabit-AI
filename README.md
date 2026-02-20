# 🌌 ExoHabit-AI — Exoplanet Habitability Prediction System
## 🚀 Project Overview

ExoHabit-AI is a full-stack machine learning web application designed to analyze exoplanet and stellar data to predict the habitability potential of distant planets.
The system combines scientific feature engineering, machine learning, and an interactive dashboard to provide meaningful insights into which exoplanets could potentially support life.

## 🎯 Key Objectives

Predict whether an exoplanet is Habitable or Not Habitable

Compute a Habitability Score & Percentage

Rank exoplanets based on habitability

Visualize planetary and stellar relationships through a dashboard

Provide an end-to-end ML + Web solution

## 🧠 Features

✅ Habitability prediction using engineered scientific features

✅ Habitability score normalization (0–100%)

✅ Dynamic ranking of exoplanets

✅ Interactive dashboard with visual analytics

✅ User-friendly web interface

✅ Modular Flask backend

## 🛠️ Tech Stack
🔹 Programming & ML

Python

NumPy

Pandas

Scikit-learn

🔹 Web Framework

Flask

🔹 Frontend

HTML5

CSS3

JavaScript

🔹 Visualization

Matplotlib

Seaborn

Chart.js

## 📂 Project Structure
exoplanet_project/
│
├── app.py
├── model.pkl
├── scaler.pkl
├── cleaned_exoplanet_data.csv
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── predict.html
│   ├── result.html
│   ├── rankings.html
│   └── dashboard.html
│
├── static/
   └── css/
      └── style.css

        
##  📊 Machine Learning Pipeline
🔹 Input Features

Planet Radius

Planet Mass

Equilibrium Temperature

Orbital Period

Host Star Temperature

🔹 Feature Engineering

A custom Habitability Score is calculated using scientific heuristics:

Temperature closeness to Earth

Planet mass suitability

Planet radius suitability

🔹 Output

Habitable / Not Habitable

Habitability Score

Habitability Percentage (0–100%)

## 📈 Dashboard Visualizations

The dashboard provides:

📊 Feature importance plot

📉 Habitability score distribution

🔬 Star temperature vs habitability scatter plot

📌 User planet comparison with dataset average

## 🧪 Milestones & Project Status
✅ Phase 0: Project Initialization

Environment setup

Dataset collection

Initial planning

✅ Milestone 1: Data Exploration & Analysis

Dataset inspection

Statistical analysis

Missing value detection

✅ Milestone 2: Data Preprocessing & Feature Engineering

Cleaning raw data

Handling missing values

Creating habitability score

Label engineering

✅ Milestone 3: Model Development

Model training

Probability prediction

Model serialization (model.pkl)

✅ Milestone 4: Visualization & Dashboard

Feature importance plots

Habitability distribution charts

Correlation analysis

Interactive dashboard integration

## 🖥️ How to Run the Project
1️⃣ Install dependencies
- pip install -r requirements.txt
2️⃣ Run Flask app
- python app.py
3️⃣ Open browser
- http://127.0.0.1:5000/

## 🧾 Pages Description

Home Page – Project introduction

Predict Page – Input planetary data

Result Page – Prediction + score + percentage

Rankings Page – Sorted exoplanet list

Dashboard Page – Visual analytics

## 📌 Sample Prediction Output
Status: Habitable 🌍
Habitability Score: 2.1
Model Confidence: 100%

## 🌟 Conclusion
ExoHabit-AI demonstrates how machine learning, data science, and web development can be combined to solve real scientific problems.
This project showcases skills in ML modeling, feature engineering, visualization, and full-stack development.
