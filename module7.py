from flask import Flask, render_template_string, send_file
import pandas as pd
import pickle
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)

# Load your data (for stats only)
try:
    DATASET_DF = pd.read_csv('processed_exoplanets.csv')
    print(f"✅ LOADED processed_exoplanets.csv: {len(DATASET_DF)} planets")
except:
    DATASET_DF = pd.DataFrame()
    print("⚠️ processed_exoplanets.csv not found")

try:
    with open('feature_order.pkl', 'rb') as f:
        FEATURE_ORDER = pickle.load(f)
    print(f"✅ LOADED feature_order.pkl: {len(FEATURE_ORDER)} features")
except:
    FEATURE_ORDER = ['pl_rade', 'pl_bmasse', 'pl_dens', 'pl_eqt', 'pl_orbper']
    print("⚠️ feature_order.pkl not found")

# 🔥 ULTIMATE GLASSMORPHISM + STAR TREK LCARS TEMPLATE
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ExoHabit-AI Ultimate - Glass Analytics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: rgba(255, 255, 255, 0.15);
            --glass-glow: rgba(255, 215, 0, 0.3);
            --starfleet-blue: #0a3d62;
            --starfleet-gold: #ffd700;
            --nebula-purple: linear-gradient(135deg, #1a0d2e 0%, #2a1a3d 50%, #0a3d62 100%);
        }
        
        * { box-sizing: border-box; }
        body {
            background: var(--nebula-purple);
            min-height: 100vh;
            font-family: 'Orbitron', 'Courier New', monospace;
            color: #e8e8e8;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Animated starfield */
        .stars {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 1;
        }
        .star {
            position: absolute; width: 2px; height: 2px; background: white;
            border-radius: 50%; animation: twinkle 2s infinite;
        }
        
        /* ULTRA GLASSMORPHISM PANELS */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(25px) saturate(180%);
            border: 1px solid var(--glass-border);
            border-radius: 25px;
            box-shadow: 
                0 8px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 var(--glass-shadow),
                0 0 0 1px rgba(255,255,255,0.05);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative; overflow: hidden;
        }
        
        .glass-panel::before {
            content: ''; position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.6s; opacity: 0;
        }
        
        .glass-panel:hover::before { left: 100%; opacity: 1; }
        .glass-panel:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: 
                0 20px 60px rgba(0,0,0,0.6),
                inset 0 1px 0 var(--glass-shadow),
                0 0 30px var(--glass-glow);
            border-color: var(--starfleet-gold);
        }
        
        .glass-title {
            background: linear-gradient(90deg, var(--starfleet-gold), #ffed4a, var(--starfleet-gold));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-family: 'Orbitron', monospace; font-weight: 900;
            text-shadow: 0 0 30px rgba(255,215,0,0.6); letter-spacing: 2px;
        }
        
        .chart-container {
            height: 400px; border-radius: 20px;
            background: rgba(0,0,0,0.2); padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .stats-glass {
            background: var(--glass-bg); backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border); border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }
        
        .btn-glass {
            background: var(--glass-bg); backdrop-filter: blur(20px);
            border: 2px solid var(--glass-border); color: #e8e8e8;
            font-weight: 700; padding: 15px 40px; border-radius: 50px;
            transition: all 0.3s ease; text-transform: uppercase;
        }
        
        .btn-glass:hover {
            background: rgba(255,215,0,0.15); border-color: var(--starfleet-gold);
            color: var(--starfleet-gold); transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(255,215,0,0.3);
        }
        
        @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.3); }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Animated Stars Background -->
    <div class="stars" id="stars"></div>
    
    <div class="container py-5 position-relative" style="z-index: 2;">
        <!-- HEADER -->
        <div class="text-center mb-5">
            <h1 class="display-3 fw-bold glass-title mb-4">
                <i class="fas fa-starship me-4"></i>EXOHABIT-AI ULTIMATE
            </h1>
            <p class="lead fs-2 text-light mb-4">Glassmorphism Stellar Analytics Dashboard</p>
            
            <div class="stats-glass p-5 mx-auto" style="max-width: 800px;">
                <div class="row text-center g-4">
                    <div class="col-md-4">
                        <i class="fas fa-database fa-3x text-warning mb-3"></i>
                        <div class="fs-1 fw-bold text-warning">{{dataset_count}}</div>
                        <small class="text-white-50">Planets Analyzed</small>
                    </div>
                    <div class="col-md-4">
                        <i class="fas fa-brain fa-3x text-warning mb-3"></i>
                        <div class="fs-1 fw-bold text-warning">{{feature_count}}</div>
                        <small class="text-white-50">Features</small>
                    </div>
                    <div class="col-md-4">
                        <i class="fas fa-chart-line fa-3x text-warning mb-3"></i>
                        <div class="fs-1 fw-bold text-warning">4 Charts</div>
                        <small class="text-white-50">Visualizations</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- 4 OLD CHARTS ONLY - GLASS PANELS -->
        <div class="row g-4">
            <!-- CHART 1: Habitability Distribution (Doughnut) -->
            <div class="col-lg-6">
                <div class="glass-panel p-4">
                    <h4 class="glass-title mb-4">📊 Habitability Distribution</h4>
                    <div class="chart-container">
                        <canvas id="habitabilityPie"></canvas>
                    </div>
                </div>
            </div>

            <!-- CHART 2: Feature Importance (Radar) -->
            <div class="col-lg-6">
                <div class="glass-panel p-4">
                    <h4 class="glass-title mb-4">🧠 Feature Importance</h4>
                    <div class="chart-container">
                        <canvas id="featureRadar"></canvas>
                    </div>
                </div>
            </div>

            <!-- CHART 3: Top Scores (Bar) -->
            <div class="col-lg-6">
                <div class="glass-panel p-4">
                    <h4 class="glass-title mb-4">🏆 Top Candidates</h4>
                    <div class="chart-container">
                        <canvas id="topScoresBar"></canvas>
                    </div>
                </div>
            </div>

            <!-- CHART 4: Radius vs Habitability (Scatter) -->
            <div class="col-lg-6">
                <div class="glass-panel p-4">
                    <h4 class="glass-title mb-4">📍 Radius Analysis</h4>
                    <div class="chart-container">
                        <canvas id="radiusScatter"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- EXPORT BUTTON -->
        <div class="text-center mt-5">
            <a href="/api/export-report" class="btn btn-glass btn-lg fs-5">
                <i class="fas fa-file-pdf me-3"></i>🚀 Export Glass Analytics Report
            </a>
        </div>
    </div>

    <!-- YOUR OLD CHART.JS CODE (EXACTLY SAME) -->
    <script>
    let charts = {};
    document.addEventListener('DOMContentLoaded', function() {
        // Create animated stars
        createStars();
        initCharts();
    });

    function createStars() {
        const starsContainer = document.getElementById('stars');
        for(let i = 0; i < 100; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 2 + 's';
            star.style.animationDuration = (Math.random() * 3 + 2) + 's';
            starsContainer.appendChild(star);
        }
    }

    function initCharts() {
        // 1. Habitability Distribution (Doughnut)
        charts.habitabilityPie = new Chart(document.getElementById('habitabilityPie').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Highly Habitable','Potentially Habitable','Marginally Habitable','Non-Habitable'],
                datasets: [{
                    data: [25, 45, 20, 10],
                    backgroundColor: ['#10b981', '#f59e0b', '#f97316', '#ef4444'],
                    borderWidth: 0,
                    borderRadius: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#e8e8e8', padding: 20 } } }
            }
        });

        // 2. Feature Importance (Radar)
        charts.featureRadar = new Chart(document.getElementById('featureRadar').getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['Radius','Mass','Density','Temp','Orbit','Distance','Stellar Lum','Stellar Temp'],
                datasets: [{
                    label: 'Feature Importance',
                    data: [0.28, 0.25, 0.22, 0.15, 0.10, 0.08, 0.07, 0.05],
                    backgroundColor: 'rgba(102,126,234,0.2)',
                    borderColor: '#667eea',
                    borderWidth: 3,
                    pointBackgroundColor: '#ffd700',
                    pointBorderColor: '#fff',
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 0.4,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        pointLabels: { color: '#e8e8e8' },
                        angleLines: { color: 'rgba(255,255,255,0.2)' },
                        ticks: { color: '#e8e8e8', backdropColor: 'transparent' }
                    }
                }
            }
        });

        // 3. Top Scores (Bar)
        charts.topScoresBar = new Chart(document.getElementById('topScoresBar').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['11 Com b','11 UMi b','14 Her b','16 Cyg B b','17 Sco b','18 Del b','24 Sex b','4 UMa b','47 UMa b','51 Peg b'],
                datasets: [{
                    label: 'Habitability Score (%)',
                    data: [92, 91, 90, 89, 88, 87, 86, 85, 84, 83],
                    backgroundColor: '#10b981',
                    borderRadius: 12,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#e8e8e8' } },
                    x: { grid: { display: false }, ticks: { color: '#e8e8e8', maxRotation: 45 } }
                }
            }
        });

        // 4. Radius vs Habitability (Scatter)
        charts.radiusScatter = new Chart(document.getElementById('radiusScatter').getContext('2d'), {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Exoplanets',
                    data: [
                        {x: 1.2, y: 92}, {x: 1.1, y: 91}, {x: 1.3, y: 90}, {x: 1.0, y: 89},
                        {x: 1.4, y: 88}, {x: 0.9, y: 87}, {x: 1.5, y: 86}, {x: 1.6, y: 85}
                    ],
                    backgroundColor: '#3b82f6',
                    borderColor: '#60a5fa',
                    pointRadius: 8,
                    pointHoverRadius: 12
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { 
                        title: { display: true, text: 'Radius (R⊕)', color: '#e8e8e8' },
                        grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#e8e8e8' }
                    },
                    y: { 
                        title: { display: true, text: 'Habitability Score (%)', color: '#e8e8e8' },
                        grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#e8e8e8' }
                    }
                }
            }
        });
    }
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, 
        dataset_count=len(DATASET_DF),
        feature_count=len(FEATURE_ORDER))

@app.route('/api/export-report')
def export_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    story.append(Paragraph("EXOHABIT-AI ULTIMATE<br/><strong>Glassmorphism Analytics Dashboard</strong>", styles['Title']))
    story.append(Spacer(1, 30))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Planets', f'{len(DATASET_DF):,}'],
        ['Features Used', str(len(FEATURE_ORDER))],
        ['Visualizations', '4 Chart.js Charts']
    ]
    
    table = Table(summary_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ExoHabit_Glass_Report.pdf')

if __name__ == '__main__':
    print("🚀 ExoHabit-AI Ultimate - GLASSMORPHISM + OLD CHARTS ONLY")
    print(f"📊 Dataset: {len(DATASET_DF)} planets | {len(FEATURE_ORDER)} features")
    print("✅ REMOVED: All Matplotlib/Seaborn/Plotly")
    print("✅ KEPT: 4 OLD Chart.js charts")
    print("✅ NEW: Ultra-transparent glassmorphism design")
    print("🌐 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
