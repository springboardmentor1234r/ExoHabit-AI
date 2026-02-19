from flask import Blueprint, jsonify
import sqlite3

bp = Blueprint("planets", __name__, url_prefix="/api/v1")

@bp.route("/top-planets")
def top_planets():
    conn = sqlite3.connect("database/exoplanets.db")
    rows = conn.execute("""
        SELECT pl_name, final_habitability_score
        FROM exoplanets
        ORDER BY final_habitability_score DESC
        LIMIT 10
    """).fetchall()
    conn.close()

    return jsonify([
        {"pl_name": r[0], "score": r[1]} for r in rows
    ])
