
# ==========================================
# CODEGUARD AI - ML PREDICTOR
# ==========================================

from pyexpat import features

import joblib
import pandas as pd

from feature_extractor import extract_features
from ai_reviewer import analyze_with_gemini

# Load trained machine learning models
quality_model = joblib.load("model/quality_model.pkl")
bug_risk_model = joblib.load("model/bug_risk_model.pkl")
feature_names = joblib.load("model/features.pkl")


# ==========================================
# QUALITY LEVEL
# ==========================================

def get_quality_level(score):

    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "Poor"


# ==========================================
# BUG RISK LEVEL
# ==========================================

def get_risk_level(score):

    if score <= 20:
        return "Low Risk"
    elif score <= 50:
        return "Moderate Risk"
    elif score <= 75:
        return "High Risk"
    else:
        return "Critical Risk"


# ==========================================
# SIMPLE CODE FINDINGS
# ==========================================

def generate_findings(features):

    findings = []

    if features["complexity"] > 10:
        findings.append({
            "type": "warning",
            "title": "Code Is Too Complex",
            "message": "Your code has many conditions and decisions. This can make it difficult to understand."
        })

    elif features["complexity"] > 5:
        findings.append({
            "type": "info",
            "title": "Some Logic Can Be Simplified",
            "message": "Your code has several conditions. Try to keep the logic simple and clear."
        })

    if features["nesting_depth"] > 3:
        findings.append({
            "type": "warning",
            "title": "Too Many Nested Blocks",
            "message": "Some if statements or loops are placed inside others. This can make the code harder to follow."
        })

    if features["long_lines"] > 0:
        findings.append({
            "type": "info",
            "title": "Long Lines Found",
            "message": f"{features['long_lines']} line(s) are longer than the recommended length. Try splitting them into shorter lines."
        })

    if features["duplicate_lines"] > 0:
        findings.append({
            "type": "warning",
            "title": "Repeated Code Found",
            "message": f"{features['duplicate_lines']} repeated line(s) were found. Reusing functions can help avoid repetition."
        })

    if features["risky_calls"] > 0:
        findings.append({
            "type": "danger",
            "title": "Operations Need Checking",
            "message": f"{features['risky_calls']} potentially risky operation(s) were found. Check whether they are safe to use."
        })

    if features["lines"] >= 10 and features["comments"] == 0:
        findings.append({
            "type": "info",
            "title": "No Comments Found",
            "message": "Your code has no comments. Add short explanations where they can help someone understand the code."
        })

    if features["functions"] == 0 and features["lines"] > 20:
        findings.append({
            "type": "info",
            "title": "No Functions Found",
            "message": "Your program is quite long. Dividing it into smaller functions can make it easier to manage."
        })

    if not findings:
        findings.append({
            "type": "success",
            "title": "Code Looks Well Structured",
            "message": "No major structural problems were found in your code."
        })

    return findings


# ==========================================
# SIMPLE RECOMMENDATIONS
# ==========================================

def generate_recommendations(features):

    recommendations = []

    if features["complexity"] > 5:
        recommendations.append(
            "Keep conditions simple and divide long logic into smaller parts."
        )

    if features["nesting_depth"] > 3:
        recommendations.append(
            "Avoid placing too many if statements or loops inside each other."
        )

    if features["duplicate_lines"] > 0:
        recommendations.append(
            "Avoid writing the same code again and again. Create a function for repeated tasks."
        )

    if features["long_lines"] > 0:
        recommendations.append(
            "Break long lines into smaller and easier-to-read statements."
        )

    if features["comments"] == 0 and features["lines"] >= 10:
        recommendations.append(
            "Add useful comments to explain important parts of your code."
        )

    if features["functions"] == 0 and features["lines"] > 20:
        recommendations.append(
            "Divide your program into smaller functions to make it easier to understand."
        )

    if features["risky_calls"] > 0:
        recommendations.append(
            "Check potentially risky operations and make sure their inputs are valid."
        )

    if not recommendations:
        recommendations.append(
            "Your code has a good structure. Keep writing clean and readable code."
        )

    return recommendations


# ==========================================
# MAIN ANALYSIS FUNCTION
# ==========================================

def analyze_code(code):

    # Read and analyze the Python code
    features = extract_features(code)

    # Check for syntax errors
    if features.get("syntax_error"):

        return {
            "success": False,
            "error": features.get(
                "syntax_message",
                "There is a mistake in your Python code."
            )
        }

    # Prepare features for prediction
    input_data = {
        feature: features.get(feature, 0)
        for feature in feature_names
    }

    input_df = pd.DataFrame([input_data])

    # Predict code quality and bug risk
    quality_prediction = quality_model.predict(input_df)[0]
    bug_risk_prediction = bug_risk_model.predict(input_df)[0]

    # Keep scores between 0 and 100
    quality_score = max(0, min(100, float(quality_prediction)))
    bug_risk = max(0, min(100, float(bug_risk_prediction)))

    # Find score levels
    quality_level = get_quality_level(quality_score)
    risk_level = get_risk_level(bug_risk)

    # Generate fallback findings and recommendations
    findings = generate_findings(features)
    recommendations = generate_recommendations(features)

    # Get dynamic AI review from Gemini
    ai_review = analyze_with_gemini(code)

    # Use Gemini results if available
    if ai_review:
        findings = ai_review["findings"]
        recommendations = ai_review["recommendations"]

    # Return final results
    return {
        "success": True,
        "quality_score": round(quality_score, 2),
        "quality_level": quality_level,
        "bug_risk": round(bug_risk, 2),
        "risk_level": risk_level,
        "features": features,
        "findings": findings,
        "recommendations": recommendations
    }


# ==========================================
# TEST THE PREDICTOR
# ==========================================

if __name__ == "__main__":

    sample_code = """
def calculate_total(numbers):
    total = 0

    for number in numbers:
        if number > 0:
            total += number

    return total

result = calculate_total([10, 20, 30])
print(result)
"""

    result = analyze_code(sample_code)

    print("\nCODEGUARD AI ANALYSIS")

    if result["success"]:

        print("\nQuality Score:", result["quality_score"])
        print("Quality Level:", result["quality_level"])

        print("\nBug Risk:", result["bug_risk"])
        print("Risk Level:", result["risk_level"])

        print("\nFindings:")
        for finding in result["findings"]:
            print("-", finding["title"])
            print(" ", finding["message"])

        print("\nRecommendations:")
        for recommendation in result["recommendations"]:
            print("-", recommendation)

    else:
        print("\nError:", result["error"])
