from flask import Blueprint, request, jsonify
from app.services.model_service import HabitabilityModel
from app.schemas.predict_schema import validate

bp = Blueprint("predict", __name__, url_prefix="/api/v1")

model = HabitabilityModel()

@bp.route("/predict", methods=["POST"])
def predict():
    data = request.json
    validate(data)

    probs = model.predict(data)

    labels = ["Non-Habitable", "Potentially Habitable", "Highly Habitable"]

    return jsonify({
        "prediction": labels[probs.index(max(probs))],
        "probabilities": probs
    })
