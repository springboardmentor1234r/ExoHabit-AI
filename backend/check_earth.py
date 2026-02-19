#!/usr/bin/env python3
"""Small helper: compute model outputs and habitability score for a planet.

Usage:
  python scripts/check_earth.py           # defaults to Earth-like inputs
  python scripts/check_earth.py --name Mars --pl_eqt 210

The script prints the raw model probability, temperature score, and final habitability score.
If the planet name is 'Earth' the dashboard displays Earth as 100 for UX; this script can show both raw and displayed values.
"""
import os
import joblib
import argparse


def calculate_habitability_score(pl_eqt, confidence):
    min_temp, max_temp = 273.15, 373.15
    if pl_eqt < min_temp or pl_eqt > max_temp:
        temp_score = max(0, 100 - abs(pl_eqt - 323.15) / 323.15 * 100)
    else:
        optimal = 288.15
        temp_score = 100 - abs(pl_eqt - optimal) / (max_temp - min_temp) * 100

    confidence_pct = float(confidence) * 100.0

    if confidence_pct < 30:
        temp_weight = 0.75
    elif confidence_pct < 60:
        temp_weight = 0.6
    else:
        temp_weight = 0.4

    conf_weight = 1.0 - temp_weight
    habitability_score = (temp_score * temp_weight) + (confidence_pct * conf_weight)
    return round(max(0, min(100, habitability_score)), 2), round(temp_score, 2), round(confidence_pct, 2)


def find_model_dir():
    cwd = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(cwd, '..'))
    model_dir = os.path.join(root, 'model')
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Model directory not found at {model_dir}")
    return model_dir


def main():
    parser = argparse.ArgumentParser(description='Check habitability prediction for a sample planet')
    parser.add_argument('--name', default='Earth', help='Planet name to label output')
    parser.add_argument('--pl_rade', type=float, default=1.0)
    parser.add_argument('--pl_bmasse', type=float, default=1.0)
    parser.add_argument('--pl_orbper', type=float, default=365)
    parser.add_argument('--pl_eqt', type=float, default=288.0)
    parser.add_argument('--st_teff', type=float, default=5778)
    parser.add_argument('--st_lum', type=float, default=1.0)
    args = parser.parse_args()

    model_dir = find_model_dir()
    model = joblib.load(os.path.join(model_dir, 'habitability_model.pkl'))
    scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))

    features = [args.pl_rade, args.pl_bmasse, args.pl_orbper, args.pl_eqt, args.st_teff, args.st_lum]
    scaled = scaler.transform([features])

    prob = model.predict_proba(scaled)[0][1]
    pred = model.predict(scaled)[0]

    raw_score, temp_score, confidence_pct = calculate_habitability_score(args.pl_eqt, prob)

    # Dashboard overrides Earth display to 100 for UX; show both raw and displayed
    displayed_score = 100 if args.name.lower() == 'earth' else raw_score

    print('Planet:', args.name)
    print('Inputs: pl_rade=', args.pl_rade, 'pl_bmasse=', args.pl_bmasse, 'pl_orbper=', args.pl_orbper, 'pl_eqt=', args.pl_eqt)
    print('        st_teff=', args.st_teff, 'st_lum=', args.st_lum)
    print('\nModel:')
    print('  predicted_label=', int(pred))
    print('  model_probability=', round(prob, 4))
    print('\nScore breakdown:')
    print('  temperature_score=', temp_score)
    print('  confidence_pct=', confidence_pct)
    print('  raw_habitability_score=', raw_score)
    print('  displayed_habitability_score=', displayed_score)


if __name__ == '__main__':
    main()
