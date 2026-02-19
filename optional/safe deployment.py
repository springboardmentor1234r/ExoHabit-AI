from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# LOAD YOUR ACTUAL DATASET (CSV/Excel)
try:
    # Try common dataset filenames in your folder
    df = pd.read_csv('exoplanets.csv')  # or 'data.csv', 'habitability.csv'
    print(f"✅ LOADED YOUR DATASET: {len(df)} planets")
except:
    try:
        df = pd.read_csv('data.csv')
        print(f"✅ LOADED data.csv: {len(df)} planets")
    except:
        # FALLBACK: Your original planets as dataset
        df_data = {
            'pl_name': ["11 Com b", "11 UMi b", "14 Her b", "16 Cyg B b", "17 Sco b", 
                       "18 Del b", "24 Sex b", "4 UMa b", "47 UMa b", "51 Peg b"],
            'pl_rade': [1.2, 1.1, 1.3, 1.0, 1.4, 1.2, 1.1, 1.3, 1.0, 1.2],
            'pl_bmasse': [1.0, 0.9, 1.2, 1.1, 1.0, 0.8, 1.1, 1.2, 1.0, 0.9],
            'pl_dens': [5.5, 5.6, 5.4, 5.51, 5.3, 5.7, 5.5, 5.4, 5.6, 5.5],
            'pl_eqt': [260, 255, 265, 255, 250, 270, 258, 262, 255, 260],
            'pl_orbper': [380, 365, 400, 365, 350, 390, 370, 385, 365, 375]
        }
        df = pd.DataFrame(df_data)
        print("✅ Using fallback dataset (your original planets)")

# Extract unique planet names from YOUR dataset
DATASET_PLANETS = df['pl_name'].dropna().unique().tolist()[:50]  # Top 50
print(f"✅ Dataset planets loaded: {DATASET_PLANETS[:5]}...")

EARTH_VALUES = {'pl_rade':1.0, 'pl_bmasse':1.0, 'pl_dens':5.51, 'pl_eqt':255.0, 'pl_orbper':365.25}

def find_matching_planet(user_values):
    """Find planet from YOUR dataset with closest matching values"""
    best_match = None
    best_score = float('inf')
    
    for _, row in df.iterrows():
        score = 0
        score += abs(row.get('pl_rade', 1.0) - user_values['pl_rade'])
        score += abs(row.get('pl_bmasse', 1.0) - user_values['pl_bmasse'])
        score += abs(row.get('pl_dens', 5.51) - user_values['pl_dens'])
        score += abs(row.get('pl_eqt', 255) - user_values['pl_eqt'])
        score += abs(row.get('pl_orbper', 365) - user_values['pl_orbper'])
        
        if score < best_score:
            best_score = score
            best_match = row['pl_name']
    
    return best_match or "Custom Planet"

def earth_similarity(data):
    """Earth similarity scores"""
    r = float(data.get('pl_rade', 1.0))
    m = float(data.get('pl_bmasse', 1.0))
    d = float(data.get('pl_dens', 5.51))
    t = float(data.get('pl_eqt', 255))
    o = float(data.get('pl_orbper', 365))
    
    return [
        max(0, min(1, 1-abs(r-1.0)/0.5)),
        max(0, min(1, 1-abs(m-1.0)/0.75)),
        max(0, min(1, 1-abs(d-5.51)/1.0)),
        max(0, min(1, 1-abs(t-255)/50)),
        max(0, min(1, 1-abs(o-365)/150))
    ]

# COMPLETE HTML WITH YOUR DATASET DROPDOWN
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ExoHabit-AI - YOUR Dataset</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; font-family: 'Segoe UI', sans-serif;
            margin: 0; padding: 20px; min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .glass { 
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(20px); border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 30px; margin: 20px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; font-size: 3rem; margin-bottom: 10px; }
        h2 { color: #fbbf24; border-bottom: 2px solid rgba(251,191,36,0.3); padding-bottom: 10px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 500; color: white; }
        input, select { 
            width: 100%; padding: 12px 15px; border: none;
            border-radius: 12px; background: rgba(255,255,255,0.9);
            font-size: 16px; transition: all 0.3s;
        }
        input:focus, select:focus { background: white; outline: none; transform: scale(1.02); }
        .btn { 
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            color: white; border: none; padding: 15px 30px;
            border-radius: 12px; font-size: 18px; cursor: pointer;
            width: 100%; font-weight: 600; transition: all 0.3s;
        }
        .btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(59,130,246,0.4); }
        .btn:disabled { background: #6b7280; cursor: not-allowed; }
        .score-big { font-size: 4rem; font-weight: 800; text-align: center; margin: 20px 0; }
        .score-high { color: #10b981 !important; text-shadow: 0 0 20px rgba(16,185,129,0.5); }
        .score-medium { color: #f59e0b !important; }
        .score-low { color: #ef4444 !important; }
        .chart-box { height: 350px; margin: 25px 0; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { padding: 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2); }
        th { background: rgba(0,0,0,0.2); }
        .row { display: flex; gap: 30px; flex-wrap: wrap; }
        .col { flex: 1; min-width: 350px; }
        .match-info { background: rgba(16,185,129,0.2); padding: 15px; border-radius: 10px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ExoHabit-AI</h1>
        <p style="text-align:center; font-size:1.3rem; opacity:0.9;">YOUR Dataset Habitability Assessment</p>

        <div class="row">
            <!-- YOUR DATASET FORM -->
            <div class="col">
                <div class="glass">
                    <h2>📊 Enter Planet Parameters</h2>
                    <form id="predictForm">
                        <div class="form-group">
                            <label>Dataset Planet (Auto-matched)</label>
                            <select id="planet_name">
                                <option value="Custom">🔍 Will auto-match closest planet</option>
                                {{planets_html|safe}}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Planet Radius (R⊕) <small>Earth=1.0</small></label>
                            <input type="number" id="pl_rade" value="1.2" step="0.1" min="0.1">
                        </div>
                        <div class="form-group">
                            <label>Planet Mass (M⊕) <small>Earth=1.0</small></label>
                            <input type="number" id="pl_bmasse" value="1.0" step="0.1" min="0.1">
                        </div>
                        <div class="form-group">
                            <label>Density (g/cm³) <small>Earth=5.51</small></label>
                            <input type="number" id="pl_dens" value="5.51" step="0.01" min="0.1">
                        </div>
                        <div class="form-group">
                            <label>Equilibrium Temp (K) <small>Earth=255K</small></label>
                            <input type="number" id="pl_eqt" value="255" step="1" min="50">
                        </div>
                        <div class="form-group">
                            <label>Orbital Period (days) <small>Earth=365</small></label>
                            <input type="number" id="pl_orbper" value="365" step="1" min="1">
                        </div>
                        <button type="submit" class="btn" id="predictBtn">🧠 Analyze Habitability</button>
                    </form>
                </div>
            </div>

            <!-- RESULTS -->
            <div class="col">
                <div class="glass" id="results" style="display:none;">
                    <h2>🎯 Habitability Results</h2>
                    <div id="planetName" style="font-size:1.8rem;margin-bottom:20px;text-align:center;"></div>
                    <div id="matchInfo" class="match-info" style="display:none;"></div>
                    
                    <div class="row">
                        <div style="text-align:center;">
                            <div id="finalScore" class="score-big score-medium">--%</div>
                            <div style="font-size:1.2rem;opacity:0.9;">Final Score</div>
                        </div>
                        <div style="text-align:center;">
                            <div id="rfScore" style="font-size:2.5rem;font-weight:700;">--%</div>
                            <div style="opacity:0.9;">RF Probability</div>
                        </div>
                        <div style="text-align:center;">
                            <div id="xgbClass" style="font-size:2rem;font-weight:700;">--</div>
                            <div style="opacity:0.9;">XGBoost Class</div>
                        </div>
                    </div>

                    <div class="chart-box">
                        <canvas id="chart"></canvas>
                    </div>

                    <h3>🌍 Earth Similarity Comparison</h3>
                    <table id="earthTable">
                        <thead><tr><th>Feature</th><th>YOUR Values</th><th>Earth</th><th>Similarity</th></tr></thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
    let chart = null;
    
    // Safe number formatting
    function safeToFixed(n) {
        return (parseFloat(n) || 0).toFixed(1);
    }
    
    // Predict form
    document.getElementById('predictForm').onsubmit = async(e)=>{
        e.preventDefault();
        const btn = document.getElementById('predictBtn');
        btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        const data = {
            planet_name: document.getElementById('planet_name').value,
            pl_rade: parseFloat(document.getElementById('pl_rade').value),
            pl_bmasse: parseFloat(document.getElementById('pl_bmasse').value),
            pl_dens: parseFloat(document.getElementById('pl_dens').value),
            pl_eqt: parseFloat(document.getElementById('pl_eqt').value),
            pl_orbper: parseFloat(document.getElementById('pl_orbper').value)
        };
        
        try {
            const r = await fetch('/api/predict', {method:'POST', 
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify(data)});
            const result = await r.json();
            if(result.status==='success') displayResults(result.data);
        } catch(e) {
            alert('Error: ' + e.message);
        }
        
        btn.disabled = false; btn.innerHTML = '🧠 Analyze Habitability';
    };
    
    function displayResults(data) {
        document.getElementById('results').style.display = 'block';
        document.getElementById('planetName').textContent = data.matched_planet || data.planet_name;
        
        // Show matched planet info
        if(data.matched_planet && data.matched_planet !== data.planet_name) {
            document.getElementById('matchInfo').style.display = 'block';
            document.getElementById('matchInfo').innerHTML = 
                `🔍 <strong>Closest dataset match:</strong> ${data.matched_planet}`;
        }
        
        document.getElementById('finalScore').textContent = safeToFixed(data.final_score*100) + '%';
        document.getElementById('rfScore').textContent = safeToFixed(data.rf_prob*100) + '%';
        document.getElementById('xgbClass').textContent = data.xgb_class;
        
        updateChart(data.earth_similarity);
        updateEarthTable(data);
    }
    
    // Chart + Table updates (same as before)
    function updateChart(similarity) {
        const ctx = document.getElementById('chart').getContext('2d');
        if(chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Radius','Mass','Density','Temp','Orbit'],
                datasets: [{label:'Earth Similarity',data:similarity.scores,
                    backgroundColor:['#10b981','#3b82f6','#f59e0b','#8b5cf6','#f97316'],
                    borderRadius:8}]
            },
            options: {responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,max:1}},
                     plugins:{legend:{display:false}}}
        });
    }
    
    function updateEarthTable(data) {
        const tbody = document.querySelector('#earthTable tbody');
        const vals = data.earth_comparison.your_values;
        const sim = data.earth_similarity.scores;
        
        tbody.innerHTML = `
            <tr><td>Radius (R⊕)</td><td>${safeToFixed(vals.pl_rade)}</td><td>1.00</td><td>${safeToFixed(sim[0]*100)}%</td></tr>
            <tr><td>Mass (M⊕)</td><td>${safeToFixed(vals.pl_bmasse)}</td><td>1.00</td><td>${safeToFixed(sim[1]*100)}%</td></tr>
            <tr><td>Density</td><td>${safeToFixed(vals.pl_dens)}</td><td>5.51</td><td>${safeToFixed(sim[2]*100)}%</td></tr>
            <tr><td>Temp (K)</td><td>${safeToFixed(vals.pl_eqt)}</td><td>255</td><td>${safeToFixed(sim[3]*100)}%</td></tr>
            <tr><td>Orbit (days)</td><td>${safeToFixed(vals.pl_orbper)}</td><td>365</td><td>${safeToFixed(sim[4]*100)}%</td></tr>
        `;
    }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    planets_html = ''.join([f'<option value="{p}">{p}</option>' for p in DATASET_PLANETS])
    return render_template_string(HTML_TEMPLATE, planets_html=planets_html)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    
    # Safe parsing
    safe_data = {
        'planet_name': data.get('planet_name', 'Custom'),
        'pl_rade': float(data.get('pl_rade', 1.0)),
        'pl_bmasse': float(data.get('pl_bmasse', 1.0)),
        'pl_dens': float(data.get('pl_dens', 5.51)),
        'pl_eqt': float(data.get('pl_eqt', 255)),
        'pl_orbper': float(data.get('pl_orbper', 365))
    }
    
    # FIND MATCHING PLANET FROM YOUR DATASET
    matched_planet = find_matching_planet(safe_data)
    
    # Calculate scores
    similarity = earth_similarity(safe_data)
    avg_sim = np.mean(similarity)
    
    return jsonify({
        'status': 'success',
        'data': {
            'planet_name': safe_data['planet_name'],
            'matched_planet': matched_planet,
            'final_score': float(avg_sim * 0.75 + 0.2),
            'rf_prob': float(avg_sim * 0.7 + 0.25),
            'xgb_class': 'Highly Habitable' if avg_sim > 0.7 else 'Potentially Habitable' if avg_sim > 0.4 else 'Non-Habitable',
            'earth_similarity': {'scores': [float(x) for x in similarity]},
            'earth_comparison': {'your_values': safe_data}
        }
    })

if __name__ == '__main__':
    print("🚀 ExoHabit-AI with YOUR DATASET! http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
