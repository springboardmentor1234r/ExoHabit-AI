import pandas as pd
from backend.app import app
from backend.database import db, Planet
import os

def seed():
    # Load dataset
    csv_path = os.path.join(os.path.dirname(__file__), '../notebooks/exoplanets_processed.csv')
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} records from CSV.")
    except FileNotFoundError:
        print(f"CSV not found at {csv_path}")
        return

    with app.app_context():
        # Clear existing data? Or checking if empty
        if Planet.query.first():
            print("Database already seeded.")
            return

        planets = []
        for _, row in df.iterrows():
            # Map CSV columns to Model fields
            # Note: Verify CSV column names match these
            p = Planet(
                pl_name=row.get('pl_name', f"Unknown-{_}"),
                pl_rade=row.get('pl_rade'),
                pl_orbper=row.get('pl_orbper'),
                pl_eqt=row.get('pl_eqt'),
                pl_dens=row.get('pl_dens'),
                st_teff=row.get('st_teff'),
                st_rad=row.get('st_rad'),
                st_mass=row.get('st_mass'),
                sy_dist=row.get('sy_dist'),
                sy_pnum=row.get('sy_pnum'),
                is_habitable=bool(row.get('is_habitable', False)),
                habitability_score=row.get('habitability_score', 0.0)
            )
            planets.append(p)
            
            if len(planets) >= 1000: # Commit in chunks
                db.session.add_all(planets)
                db.session.commit()
                planets = []
                print(f"Seeded 1000 records...")

        if planets:
            db.session.add_all(planets)
            db.session.commit()
            
        print("Database seeding completed.")

if __name__ == '__main__':
    seed()
