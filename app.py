from flask import Flask, render_template, request, jsonify

from predictor import analyze_code
import json
import os

# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

def load_evaluation():
    evaluation_path = os.path.join(
        "model",
        "evaluation.json"
    )

    if not os.path.exists(evaluation_path):
        return {}

    with open(evaluation_path, "r") as file:
        return json.load(file)
# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# CODE ANALYSIS API
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        # -----------------------------------------
        # Get code from frontend
        # -----------------------------------------

        code = data.get("code", "")

        # -----------------------------------------
        # Empty code check
        # -----------------------------------------

        if not code.strip():

            return jsonify({
                "success": False,
                "error": "Please enter Python code."
            }), 400

        # -----------------------------------------
        # Analyze code using ML pipeline
        # -----------------------------------------

        result = analyze_code(code)
        result["evaluation"] = load_evaluation()
        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )