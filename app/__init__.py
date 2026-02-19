from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )

    from app.routes.predict import bp as predict_bp
    from app.routes.planets import bp as planets_bp

    app.register_blueprint(predict_bp, url_prefix="/api/v1")
    app.register_blueprint(planets_bp, url_prefix="/api/v1")

    return app
