<div align="center">

# 🪐 ExoHabit AI (https://exohabit-ai-3ni1.onrender.com)

### *Exploring the Cosmos, One Exoplanet at a Time*

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20Here-00d4ff?style=for-the-badge)](https://exohabit-ai.onrender.com)
[![License](https://img.shields.io/badge/📜%20License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/🐍%20Python-3.8+-green?style=for-the-badge)](https://python.org)
[![Flask](https://img.shields.io/badge/⚡%20Flask-2.0+-orange?style=for-the-badge)](https://flask.palletsprojects.com)

<img src="https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif" width="600" alt="Space Animation">

**🌌 An intelligent system that predicts exoplanet habitability using machine learning**

[Features](#-features) • [Demo](#-live-demo) • [Installation](#-quick-start) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What's This?

<div align="center">

| 🌍 **Earth** | 🪐 **Exoplanets** | 🤖 **AI Prediction** |
|:------------:|:-----------------:|:--------------------:|
| Our home | 5,600+ discovered | Instant analysis |

</div>

**ExoHabit AI** uses advanced machine learning to analyze planetary data and predict which distant worlds might support life. Just input the stellar and planetary parameters, and our ML model will tell you if that exoplanet is habitable!

<details>
<summary>🎬 <b>Watch it in action</b> (Click to expand)</summary>

### Features Demo

- ✅ **3D Space Visualization** - Interactive starfield with Three.js
- ✅ **Real-time Predictions** - Get results in milliseconds
- ✅ **Educational Content** - Learn about famous exoplanets
- ✅ **Data Visualization** - Beautiful charts and graphs

</details>

---

## ✨ Features

<div align="center">

| Feature | Description | Status |
|:-------:|-------------|:------:|
| 🤖 | **ML Prediction** | ✅ |
| 🎨 | **3D Visualizations** | ✅ |
| 📱 | **Mobile Responsive** | ✅ |
| ⚡ | **Fast API** | ✅ |
| 📊 | **Interactive Charts** | ✅ |

</div>

### 🎮 Interactive Elements

- 🌟 **3D Hero Section** - Animated starfield with floating particles
- 🔮 **Prediction Dashboard** - Real-time habitability scoring
- 📚 **Exoplanet Encyclopedia** - Learn about Proxima b, TRAPPIST-1, and more
- 📈 **Data Visualizations** - Feature importance and distribution charts

---

## 🚀 Live Demo

<div align="center">

### **[✨ Try ExoHabit AI Now ✨](https://exohabit-ai-3ni1.onrender.com)**

<img src="https://img.shields.io/badge/Status-Online-success?style=for-the-badge&logo=render&logoColor=white" alt="Status">

</div>

---

## 🛠️ Tech Stack

<details>
<summary>💻 <b>Backend</b> - Click to expand</summary>

```
🐍 Python 3.8+
⚡ Flask - Web framework
🤖 Scikit-learn - ML models
📦 Joblib - Model serialization
🐼 Pandas/NumPy - Data processing
```

</details>

<details>
<summary>🎨 <b>Frontend</b> - Click to expand</summary>

```
🌐 HTML5/CSS3
📜 JavaScript ES6+
🎭 Three.js - 3D graphics
📊 Chart.js - Data visualization
🎬 GSAP - Animations
```

</details>

---


---

## 📚 API Documentation

### 🔗 Endpoints

```http
GET  /          → Website homepage
GET  /health    → Check API status
GET  /features  → List required features
POST /predict   → Make prediction
```

### 🎯 Example Request

<details>
<summary>Click to see API example</summary>

```bash
# Make a prediction
curl -X POST https://exohabit-ai.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pl_orbper": 365.25,
    "pl_rade": 1.0,
    "pl_bmasse": 1.0,
    "pl_eqt": 288,
    "st_teff": 5778,
    "st_rad": 1.0,
    "st_mass": 1.0,
    "sy_dist": 10.0,
    "sy_snum": 1,
    "sy_pnum": 1
  }'
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "is_habitable": 1,
    "habitability_probability": 0.85,
    "confidence": "High",
    "classification": "Habitable"
  }
}
```

</details>

### 📊 Input Features

| Feature | Description | Example |
|---------|-------------|---------|
| `pl_orbper` | Orbital Period (days) | 365.25 |
| `pl_rade` | Planet Radius (Earth radii) | 1.0 |
| `pl_bmasse` | Planet Mass (Earth masses) | 1.0 |
| `pl_eqt` | Equilibrium Temperature (K) | 288 |
| `st_teff` | Stellar Temperature (K) | 5778 |

---

## 📈 Project Roadmap

<div align="center">

```
Phase 0: Setup          [██████████] 100% ✅
Phase 1: Data Analysis  [██████████] 100% ✅
Phase 2: Preprocessing  [██████████] 100% ✅
Phase 3: ML Models      [██████████] 100% ✅
Phase 4: Web App        [██████████] 100% ✅
Phase 5: Deployment     [████████░░] 80% 🚀
```

</div>

---

## 🤝 Contributing

We welcome contributions! Here's how:

```bash
# 1. Fork the repo
# 2. Create your branch
git checkout -b feature/AmazingFeature

# 3. Commit changes
git commit -m 'Add: Amazing feature'

# 4. Push to branch
git push origin feature/AmazingFeature

# 5. Open Pull Request
```

<div align="center">

[![Contributors](https://img.shields.io/badge/👥-Contributors-blue?style=for-the-badge)](https://github.com/springboardmentor1234r/ExoHabit-AI/graphs/contributors)

</div>

---

## 🙏 Acknowledgments

<div align="center">

| Organization | Contribution |
|:------------:|:------------|
| 🚀 NASA | Exoplanet Archive data |
| 🔭 Kepler/TESS | Exoplanet discoveries |
| 🌐 Open Source | Amazing tools & libraries |

</div>

---

## 📞 Contact

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-ExoHabit--AI-black?style=for-the-badge&logo=github)](https://github.com/springboardmentor1234r/ExoHabit-AI)

**Made with ❤️ and 🚀 for space enthusiasts**

> *"The universe is not only queerer than we suppose, but queerer than we can suppose."* - J.B.S. Haldane

<img src="https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif" width="200" alt="Rocket">

</div>

---

<div align="center">

⭐ **Star this repo if you find it helpful!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/springboardmentor1234r/ExoHabit-AI?style=social)](https://github.com/springboardmentor1234r/ExoHabit-AI/stargazers)

</div>
