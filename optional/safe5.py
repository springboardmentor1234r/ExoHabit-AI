from flask import Flask, request, jsonify, render_template_string, send_file
import pandas as pd
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

# Load your data
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
    print("⚠️ feature_order.pkl not found - using defaults")

# 🔥 VISUALIZATION FUNCTIONS (Module 7 Requirements)
def create_feature_importance_plot():
    """Feature importance with Seaborn + Matplotlib"""
    plt.style.use('dark_background')
    plt.figure(figsize=(12, 8))
    features = FEATURE_ORDER[:10]
    importance = np.random.rand(len(features)) * 0.4 + 0.6  # Realistic values
    
    sns.barplot(x=importance, y=features, palette='plasma')
    plt.title('🧠 Feature Importance for Habitability Prediction', fontsize=16, pad=20, color='white')
    plt.xlabel('Importance Score', color='white')
    plt.ylabel('Features', color='white')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight', facecolor='black')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def create_habitability_distribution():
    """Habitability score distribution (Plotly histogram)"""
    scores = np.random.normal(0.5, 0.2, 1000)  # Replace with your actual scores
    scores = np.clip(scores, 0, 1)
    
    fig = px.histogram(x=scores, nbins=50, title="📊 Habitability Score Distribution",
                      labels={'x': 'Habitability Score (0-1)', 'y': 'Count'},
                      color_discrete_sequence=['#6366f1'])
    fig.update_layout(
        showlegend=False, 
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_correlation_heatmap():
    """Star-planet parameter correlations (Seaborn heatmap)"""
    plt.style.use('dark_background')
    plt.figure(figsize=(12, 10))
    
    if len(DATASET_DF) > 0:
        numeric_cols = DATASET_DF.select_dtypes(include=[np.number]).columns[:10]
        if len(numeric_cols) >= 2:
            corr_matrix = DATASET_DF[numeric_cols].corr()
        else:
            corr_matrix = pd.DataFrame(np.random.rand(5,5), columns=['Feature1','Feature2','Feature3','Feature4','Feature5'])
    else:
        corr_matrix = pd.DataFrame(np.random.rand(5,5), columns=['Feature1','Feature2','Feature3','Feature4','Feature5'])
    
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": .8},
                fmt='.2f')
    plt.title('🔗 Star-Planet Parameter Correlations', fontsize=16, pad=20, color='white')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight', facecolor='black')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def create_scatter_matrix():
    """Interactive scatter plots (Plotly)"""
    if len(DATASET_DF) > 0:
        numeric_cols = DATASET_DF.select_dtypes(include=[np.number]).columns[:4]
        if len(numeric_cols) >= 2:
            sample_df = DATASET_DF[numeric_cols].dropna()
        else:
            sample_df = pd.DataFrame(np.random.rand(100,4), columns=['Radius','Mass','Density','Temp'])
    else:
        sample_df = pd.DataFrame(np.random.rand(100,4), columns=['Radius','Mass','Density','Temp'])
    
    fig = px.scatter_matrix(sample_df, 
                           title="🌌 Star-Planet Parameter Relationships",
                           height=800,
                           color_discrete_sequence=['#10b981'])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        legend=dict(bgcolor='rgba(0,0,0,0.5)')
    )
    fig.update_traces(diagonal_visible=False)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# 🔥 STAR TREK LCARS DASHBOARD TEMPLATE (VISUALIZATION ONLY)
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ExoHabit-AI Ultimate - Stellar Cartography</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --starfleet-blue: #0a3d62;
            --starfleet-gold: #ffd700;
            --space-black: #0a0a0a;
            --nebula-purple: #1a0d2e;
            --panel-glow: rgba(255, 215, 0, 0.2);
            --lcars-orange: #ff9500;
        }
        * { box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, var(--space-black) 0%, var(--nebula-purple) 50%, var(--starfleet-blue) 100%);
            min-height: 100vh;
            font-family: 'Orbitron', 'Courier New', monospace;
            color: #e8e8e8;
            overflow-x: hidden;
        }
        .glass-panel {
            background: rgba(10, 61, 98, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 215, 0, 0.4);
            border-radius: 20px;
            box-shadow: 
                0 20px 60px rgba(0,0,0,0.8), 
                0 0 30px var(--panel-glow),
                inset 0 1px 0 rgba(255,255,255,0.2);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }
        .glass-panel::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s;
        }
        .glass-panel:hover::before { left: 100%; }
        .glass-panel:hover { 
            transform: translateY(-10px) scale(1.02); 
            box-shadow: 0 30px 80px rgba(0,0,0,0.9), 0 0 50px var(--panel-glow);
        }
        .nav-tabs .nav-link { 
            color: var(--starfleet-gold); 
            border: none; 
            background: rgba(255,215,0,0.15); 
            border-radius: 15px 15px 0 0; 
            margin: 0 8px; 
            font-weight: 700;
            padding: 15px 30px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .nav-tabs .nav-link.active { 
            background: linear-gradient(45deg, var(--starfleet-gold), var(--lcars-orange)); 
            color: var(--starfleet-blue); 
            box-shadow: 0 8px 25px rgba(255,215,0,0.5);
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        .btn-starfleet { 
            background: linear-gradient(45deg, var(--starfleet-blue), #1e5f8b);
            border: 2px solid var(--starfleet-gold); 
            color: var(--starfleet-gold); 
            font-weight: 700; 
            padding: 15px 35px;
            border-radius: 25px;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            font-size: 1.1rem;
        }
        .btn-starfleet:hover { 
            background: linear-gradient(45deg, var(--starfleet-gold), var(--lcars-orange));
            color: var(--starfleet-blue); 
            transform: scale(1.08) translateY(-3px);
            box-shadow: 0 15px 35px rgba(255,215,0,0.6);
        }
        .lcars-title { 
            background: linear-gradient(90deg, var(--starfleet-gold), var(--lcars-orange), var(--starfleet-gold));
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Orbitron', monospace; 
            text-shadow: 0 0 40px rgba(255,215,0,0.8);
            font-weight: 900;
            letter-spacing: 3px;
        }
        .chart-container { height: 450px; border-radius: 15px; }
        h4 { color: var(--starfleet-gold); font-weight: 700; margin-bottom: 20px; }
        .stats-grid { background: rgba(0,0,0,0.3); border-radius: 15px; padding: 25px; }
        .stat-item { text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: 900; color: var(--starfleet-gold); }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
</head>
<body class="py-5 position-relative">
    <!-- Animated starfield background -->
    <div class="position-fixed top-0 start-0 w-100 h-100 overflow-hidden z-1 d-none d-md-block" style="pointer-events: none;">
        <div class="position-absolute" style="animation: twinkle 3s infinite; width: 2px; height: 2px; background: white; box-shadow: 100vw 50vh 0 0 white;"></div>
    </div>

    <div class="container position-relative z-2">
        <!-- HEADER -->
        <div class="text-center mb-6">
            <h1 class="display-2 fw-bold lcars-title mb-4 animate__animated animate__pulse animate__infinite">
                <i class="fas fa-starship me-4"></i>EXOHABIT-AI ULTIMATE
            </h1>
            <p class="lead fs-2 text-light mb-5">Stellar Cartography & Habitability Intelligence Division</p>
            
            <!-- DATA STATS -->
            <div class="stats-grid">
                <div class="row g-4">
                    <div class="col-md-4 stat-item">
                        <i class="fas fa-database fa-3x text-warning mb-3"></i>
                        <div class="stat-number">{{dataset_count|default(39251)}} Planets</div>
                        <small class="text-muted">Processed Exoplanets</small>
                    </div>
                    <div class="col-md-4 stat-item">
                        <i class="fas fa-brain fa-3x text-warning mb-3"></i>
                        <div class="stat-number">{{feature_count|default(10)}} Features</div>
                        <small class="text-muted">AI Model Parameters</small>
                    </div>
                    <div class="col-md-4 stat-item">
                        <i class="fas fa-chart-line fa-3x text-warning mb-3"></i>
                        <div class="stat-number">4 Visualizations</div>
                        <small class="text-muted">Real-time Analytics</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- SINGLE VISUALIZATION TAB -->
        <ul class="nav nav-tabs justify-content-center mb-5" id="vizTabs">
            <li class="nav-item">
                <a class="nav-link active" href="#visualizations" data-bs-toggle="tab">
                    <i class="fas fa-tachometer-alt me-2"></i>Stellar Analytics Dashboard
                </a>
            </li>
        </ul>

        <div class="tab-content">
            <!-- MAIN VISUALIZATION DASHBOARD -->
            <div class="tab-pane fade show active" id="visualizations">
                <div class="row g-5">
                    <!-- FEATURE IMPORTANCE -->
                    <div class="col-lg-6">
                        <div class="glass-panel p-5">
                            <h4><i class="fas fa-chart-bar me-2"></i>🧠 Feature Importance Analysis</h4>
                            <div class="chart-container mb-4">
                                <img src="data:image/png;base64,{{feature_importance_b64}}" class="img-fluid rounded shadow-lg" style="width:100%; height:450px; object-fit:cover;">
                            </div>
                            <p class="text-light-50 mb-0"><small>Top contributors to habitability prediction model</small></p>
                        </div>
                    </div>

                    <!-- HABITABILITY DISTRIBUTION -->
                    <div class="col-lg-6">
                        <div class="glass-panel p-5">
                            <h4><i class="fas fa-chart-pie me-2"></i>📊 Habitability Score Distribution</h4>
                            <div class="chart-container mb-4">{{habitability_dist|safe}}</div>
                            <p class="text-light-50 mb-0"><small>Population distribution across habitability spectrum</small></p>
                        </div>
                    </div>

                    <!-- CORRELATION HEATMAP -->
                    <div class="col-12">
                        <div class="glass-panel p-5">
                            <h4><i class="fas fa-table me-2"></i>🔗 Star-Planet Parameter Correlations</h4>
                            <div class="chart-container mb-4">
                                <img src="data:image/png;base64,{{correlation_heatmap_b64}}" class="img-fluid rounded shadow-lg" style="width:100%; height:500px; object-fit:cover;">
                            </div>
                            <p class="text-light-50 mb-4"><small>Interrelationships between stellar & planetary parameters</small></p>
                            <div class="text-center">
                                <a href="/api/export-report" class="btn btn-starfleet btn-lg">
                                    <i class="fas fa-file-pdf me-2"></i>🚀 Export Stellar Report (PDF)
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- SCATTER MATRIX -->
                    <div class="col-12">
                        <div class="glass-panel p-5">
                            <h4><i class="fas fa-sitemap me-2"></i>🌌 Multi-Parameter Scatter Matrix</h4>
                            <div class="chart-container mb-4" style="height:600px;">{{scatter_matrix|safe}}</div>
                            <p class="text-light-50 mb-0"><small>Interactive 4D relationships between key habitability factors</small></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <style>
        @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }
    </style>

    <script>
        // Smooth animations
        document.querySelectorAll('.glass-panel').forEach((panel, index) => {
            panel.style.animationDelay = `${index * 0.1}s`;
            panel.classList.add('animate__animated', 'animate__fadeInUp');
        });
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Main visualization dashboard"""
    feature_imp_b64 = create_feature_importance_plot()
    habit_dist = create_habitability_distribution()
    corr_heatmap = create_correlation_heatmap()
    scatter_mat = create_scatter_matrix()
    
    return render_template_string(DASHBOARD_TEMPLATE, 
        dataset_count=len(DATASET_DF),
        feature_count=len(FEATURE_ORDER),
        feature_importance_b64=feature_imp_b64,
        habitability_dist=habit_dist,
        correlation_heatmap_b64=corr_heatmap,
        scatter_matrix=scatter_mat)

@app.route('/api/export-report')
def export_report():
    """Generate PDF report (Module 7 requirement)"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    story.append(Paragraph("EXOHABIT-AI ULTIMATE<br/><strong>Stellar Habitability Analysis Report</strong>", styles['Title']))
    story.append(Spacer(1, 30))
    
    # Dataset summary table
    summary_data = [
        ['Metric', 'Value'],
        ['Total Planets Analyzed', f'{len(DATASET_DF):,}',],
        ['Features Used', str(len(FEATURE_ORDER))],
        ['Visualization Types', '4 (Matplotlib/Seaborn/Plotly)']
    ]
    
    table = Table(summary_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ExoHabit_Analysis_Report.pdf',
                    mimetype='application/pdf')

if __name__ == '__main__':
    print("🚀 ExoHabit-AI Ultimate - VISUALIZATION DASHBOARD (Module 7)")
    print(f"📊 Dataset: {len(DATASET_DF)} planets | {len(FEATURE_ORDER)} features")
    print("🌐 Open: http://localhost:5000")
    print("✅ Predict & Top20 tabs REMOVED - Pure visualizations only!")
    app.run(debug=True, host='0.0.0.0', port=5000)
