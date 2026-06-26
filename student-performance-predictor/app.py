from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from model import StudentPerformanceModel
from preprocessing import FEATURE_COLUMNS, clean_dataset, load_dataset, split_features_target


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_data.csv"

app = Flask(__name__)
model = StudentPerformanceModel()
dataset_summary = {}


def bootstrap_model() -> None:
    global dataset_summary

    raw_df = load_dataset(str(DATA_PATH))
    clean_df = clean_dataset(raw_df)
    x, y = split_features_target(clean_df)
    model.fit(x, y)
    dataset_summary = {
        "row_count": int(clean_df.shape[0]),
        "features": FEATURE_COLUMNS,
        "metrics": {
            "r2_score": model.r2_score_,
            "rmse": model.rmse_,
        },
        "statistics": model.stats_summary(clean_df),
    }


@app.route("/")
def index():
    return render_template("index.html", feature_columns=FEATURE_COLUMNS)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/summary", methods=["GET"])
def summary():
    return jsonify(dataset_summary)


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}

    missing = [col for col in FEATURE_COLUMNS if col not in payload]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        attendance = float(payload["attendance"])
        study_hours = float(payload["study_hours"])
        previous_grades = float(payload["previous_grades"])
    except (TypeError, ValueError):
        return jsonify({"error": "Input values must be numeric."}), 400

    prediction = model.predict_score(attendance, study_hours, previous_grades)
    band = model.performance_band(prediction)

    return jsonify(
        {
            "predicted_score": round(prediction, 2),
            "performance_band": band,
            "input": {
                "attendance": attendance,
                "study_hours": study_hours,
                "previous_grades": previous_grades,
            },
        }
    )


bootstrap_model()


if __name__ == "__main__":
    app.run(debug=True)

