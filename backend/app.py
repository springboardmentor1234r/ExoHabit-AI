from flask import Flask, request, render_template, jsonify, send_file
import joblib
import numpy as np
import os
import json
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch

app = Flask(__name__)

# Get the directory of the current file and construct the correct path
current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(os.path.dirname(current_dir), 'model')

model = joblib.load(os.path.join(model_dir, "habitability_model.pkl"))
scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))

# Enhanced feature names
FEATURE_NAMES = ['Planet Radius', 'Planet Mass', 'Orbital Period', 'Equilibrium Temp', 'Star Temp', 'Star Luminosity']
FEATURE_SHORT = ['pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_eqt', 'st_teff', 'st_lum']

def calculate_habitability_score(pl_eqt, confidence):
    """Calculate a 0-100 habitability score based on temperature and model confidence"""
    # Habitable zone: 273.15K (0°C) to 373.15K (100°C)
    min_temp, max_temp = 273.15, 373.15
    if pl_eqt < min_temp or pl_eqt > max_temp:
        temp_score = max(0, 100 - abs(pl_eqt - 323.15) / 323.15 * 100)
    else:
        # Optimal temp around 288.15K (15°C - Earth average)
        optimal = 288.15
        temp_score = 100 - abs(pl_eqt - optimal) / (max_temp - min_temp) * 100
    
    # Model confidence is provided as a probability (0.0 - 1.0). Convert to 0-100 scale.
    confidence_pct = float(confidence) * 100.0

    # Dynamic weighting: if model confidence is very low, give more weight to temperature
    if confidence_pct < 30:
        temp_weight = 0.75
    elif confidence_pct < 60:
        temp_weight = 0.6
    else:
        temp_weight = 0.4

    conf_weight = 1.0 - temp_weight

    habitability_score = (temp_score * temp_weight) + (confidence_pct * conf_weight)
    return round(max(0, min(100, habitability_score)), 2)

def get_planet_rank(habitability_score):
    """Categorize planet based on habitability score"""
    if habitability_score >= 80:
        return "Highly Habitable", "badge-success"
    elif habitability_score >= 60:
        return "Likely Habitable", "badge-info"
    elif habitability_score >= 40:
        return "Possibly Habitable", "badge-warning"
    else:
        return "Low Habitability", "badge-danger"

def generate_pdf_report():
    """Generate a PDF report with dashboard data"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        alignment=1
    )
    elements.append(Paragraph("Exoplanet Habitability Analysis Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Date
    date_style = ParagraphStyle('CustomDate', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", date_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Overview Section
    elements.append(Paragraph("Executive Summary", styles['Heading2']))
    overview_text = """
    This report provides a comprehensive analysis of exoplanet habitability predictions using machine learning. 
    The model evaluates six key characteristics of exoplanets and their host stars to determine the likelihood 
    of supporting Earth-like life.
    """
    elements.append(Paragraph(overview_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Feature Importance Section
    elements.append(Paragraph("Feature Importance Analysis", styles['Heading2']))
    try:
        importances = model.feature_importances_.tolist()
        total = sum(importances)
        feature_data = [['Feature', 'Importance %', 'Impact Level']]
        for i, (name, importance) in enumerate(zip(FEATURE_NAMES, importances)):
            pct = (importance / total * 100)
            impact = "High" if pct > 20 else "Medium" if pct > 10 else "Low"
            feature_data.append([name, f"{pct:.1f}%", impact])
        
        feature_table = Table(feature_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        elements.append(feature_table)
    except:
        elements.append(Paragraph("Unable to generate feature importance table", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Habitability Categories Section
    elements.append(Paragraph("Habitability Classification System", styles['Heading2']))
    categories_data = [
        ['Score Range', 'Category', 'Description'],
        ['80-100', 'Highly Habitable', 'Excellent conditions for life with favorable temperature and planetary characteristics'],
        ['60-79', 'Likely Habitable', 'Good conditions with reasonable trade-offs and strong potential for life support'],
        ['40-59', 'Possibly Habitable', 'Marginal conditions that might support microbial or exotic organisms'],
        ['0-39', 'Low Habitability', 'Unfavorable conditions making life unlikely without extreme adaptations']
    ]
    
    categories_table = Table(categories_data, colWidths=[1.2*inch, 1.5*inch, 3*inch])
    categories_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    elements.append(categories_table)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Model Information
    elements.append(Paragraph("Model Specifications", styles['Heading2']))
    model_info = f"""
    <b>Model Type:</b> Random Forest Classifier<br/>
    <b>Training Data:</b> NASA Exoplanet Archive (40,000+ records)<br/>
    <b>Features Evaluated:</b> 6 key characteristics<br/>
    <b>Model Accuracy:</b> ~94%<br/>
    <b>Prediction Method:</b> Machine learning with ensemble methods<br/>
    <b>Habitability Threshold:</b> Temperature range 0°C - 100°C (273.15K - 373.15K)
    """
    elements.append(Paragraph(model_info, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_text = """
    <i>This report was automatically generated by the Exoplanet Habitability Predictor. 
    The predictions are based on machine learning models and should be considered alongside 
    other scientific criteria for exoplanet habitability assessment.</i>
    """
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_csv_report():
    """Generate CSV reports with model data"""
    output = BytesIO()
    
    # Feature Importance Report
    try:
        importances = model.feature_importances_.tolist()
        total = sum(importances)
        
        feature_data = {
            'Feature': FEATURE_NAMES,
            'Importance Score': importances,
            'Percentage (%)': [round((i/total*100), 2) for i in importances],
            'Impact Level': ['High' if (i/total*100) > 20 else 'Medium' if (i/total*100) > 10 else 'Low' for i in importances]
        }
        
        df = pd.DataFrame(feature_data)
        csv_string = "EXOPLANET HABITABILITY ANALYSIS - FEATURE IMPORTANCE REPORT\n"
        csv_string += f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}\n"
        csv_string += "="*80 + "\n\n"
        csv_string += df.to_csv(index=False)
        csv_string += "\n\n" + "="*80 + "\n"
        csv_string += "HABITABILITY CLASSIFICATION THRESHOLDS\n"
        csv_string += "="*80 + "\n"
        csv_string += "Score Range,Category,Description\n"
        csv_string += "80-100,Highly Habitable,Excellent conditions for life\n"
        csv_string += "60-79,Likely Habitable,Good conditions with favorable characteristics\n"
        csv_string += "40-59,Possibly Habitable,Marginal conditions\n"
        csv_string += "0-39,Low Habitability,Unfavorable conditions\n"
        
        output.write(csv_string.encode())
        output.seek(0)
        return output
    except Exception as e:
        output.write(f"Error generating CSV: {str(e)}".encode())
        output.seek(0)
        return output

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = [
            float(request.form["pl_rade"]),
            float(request.form["pl_bmasse"]),
            float(request.form["pl_orbper"]),
            float(request.form["pl_eqt"]),
            float(request.form["st_teff"]),
            float(request.form["st_lum"])
        ]

        scaled = scaler.transform([features])
        prediction = model.predict(scaled)[0]
        confidence = model.predict_proba(scaled)[0][1]
        
        # Calculate habitability score
        habitability_score = calculate_habitability_score(features[3], confidence)
        planet_rank, badge_class = get_planet_rank(habitability_score)

        result = "Potentially Habitable 🌍" if prediction == 1 else "Not Habitable ❌"

        return render_template("index.html",
                               prediction_text=result,
                               confidence=round(confidence*100, 2),
                               habitability_score=habitability_score,
                               planet_rank=planet_rank,
                               badge_class=badge_class)
    except KeyError:
        return render_template("index.html",
                               prediction_text="❌ Error: Missing required input field")
    except ValueError:
        return render_template("index.html",
                               prediction_text="❌ Error: Please enter valid numbers")
    except Exception as e:
        return render_template("index.html",
                               prediction_text=f"❌ Error: {str(e)}")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """JSON API endpoint for predictions. Accepts JSON with the six features and returns
    habitability score, confidence, and rank as JSON.
    """
    try:
        data = request.get_json() or {}
        # Allow both flat JSON and form-like keys
        pl_rade = float(data.get('pl_rade'))
        pl_bmasse = float(data.get('pl_bmasse'))
        pl_orbper = float(data.get('pl_orbper'))
        pl_eqt = float(data.get('pl_eqt'))
        st_teff = float(data.get('st_teff'))
        st_lum = float(data.get('st_lum'))

        features = [pl_rade, pl_bmasse, pl_orbper, pl_eqt, st_teff, st_lum]
        scaled = scaler.transform([features])
        # Prediction and confidence
        prob = model.predict_proba(scaled)[0][1]
        habitability_score = calculate_habitability_score(pl_eqt, prob)
        planet_rank, badge_class = get_planet_rank(habitability_score)

        return jsonify({
            'habitability_score': habitability_score,
            'confidence': round(prob * 100, 2),
            'planet_rank': planet_rank,
            'badge_class': badge_class
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/api/top-ranked")
def api_top_ranked():
    """Return top-N planets from the dataset ranked by habitability score.

    Query params:
      - n: number of top results to return (default 5)
    """
    try:
        n = int(request.args.get('n', 5))
        # locate dataset
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        data_path = os.path.join(project_root, 'data', 'exoplanet_clean_40k.csv')
        if not os.path.exists(data_path):
            return jsonify({'error': f'data file not found at {data_path}'}), 500

        # read only needed columns to be efficient
        usecols = ['pl_name','pl_rade','pl_bmasse','pl_orbper','pl_eqt','st_teff','st_lum']
        df = pd.read_csv(data_path, usecols=usecols)

        # drop rows missing critical features
        df = df.dropna(subset=['pl_rade','pl_bmasse','pl_orbper','pl_eqt','st_teff','st_lum'])

        # prepare features for model
        features = df[['pl_rade','pl_bmasse','pl_orbper','pl_eqt','st_teff','st_lum']].astype(float).values
        scaled = scaler.transform(features)
        probs = model.predict_proba(scaled)[:,1]

        # compute habitability scores using existing helper
        # calculate_habitability_score returns a single float (not a tuple)
        scores = [calculate_habitability_score(float(eq), float(p)) for eq, p in zip(df['pl_eqt'].astype(float).values, probs)]

        df_result = df.copy()
        df_result['confidence'] = (probs * 100).round(2)
        df_result['habitability_score'] = scores

        top = df_result.sort_values('habitability_score', ascending=False).head(n)

        results = []
        for _, row in top.iterrows():
            results.append({
                'pl_name': row['pl_name'],
                'pl_rade': float(row['pl_rade']),
                'pl_bmasse': float(row['pl_bmasse']),
                'pl_orbper': float(row['pl_orbper']),
                'pl_eqt': float(row['pl_eqt']),
                'st_teff': float(row['st_teff']),
                'st_lum': float(row['st_lum']),
                'confidence': float(row['confidence']),
                'habitability_score': float(row['habitability_score'])
            })

        return jsonify({'top': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/feature-importance")
def get_feature_importance():
    """Return feature importance from the trained model"""
    try:
        importances = model.feature_importances_.tolist()
        return jsonify({
            "features": FEATURE_NAMES,
            "importances": importances,
            "total": sum(importances)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    """Dashboard view with visualizations"""
    return render_template("dashboard.html")


@app.route("/health")
def health():
    """Simple healthcheck: verifies model and scaler loaded"""
    try:
        ok = True
        # quick checks
        _ = float(model.feature_importances_.sum())
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/export/pdf")
def export_pdf():
    """Export dashboard report as PDF"""
    try:
        pdf_buffer = generate_pdf_report()
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'exoplanet_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

@app.route("/export/csv")
def export_csv():
    """Export analysis data as CSV"""
    try:
        csv_buffer = generate_csv_report()
        return send_file(
            csv_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'exoplanet_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({"error": f"CSV generation failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
