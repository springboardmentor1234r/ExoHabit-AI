from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planets'
    
    id = db.Column(db.Integer, primary_key=True)
    pl_name = db.Column(db.String(100), unique=True, nullable=False)
    pl_rade = db.Column(db.Float)
    pl_orbper = db.Column(db.Float)
    pl_eqt = db.Column(db.Float)
    pl_dens = db.Column(db.Float)
    st_teff = db.Column(db.Float)
    st_rad = db.Column(db.Float)
    st_mass = db.Column(db.Float)
    sy_dist = db.Column(db.Float)
    sy_pnum = db.Column(db.Integer)
    is_habitable = db.Column(db.Boolean)
    habitability_score = db.Column(db.Float)

    def to_dict(self):
        return {
            'pl_name': self.pl_name,
            'pl_rade': self.pl_rade,
            'pl_orbper': self.pl_orbper,
            'pl_eqt': self.pl_eqt,
            'sy_dist': self.sy_dist,
            'is_habitable': self.is_habitable,
            'habitability_score': self.habitability_score
        }

def init_db(app):
    # Use internal database URL for Render, or sqlite for local dev
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///exoplanets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
