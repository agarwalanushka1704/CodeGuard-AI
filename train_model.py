# ==========================================
# CODEGUARD AI - MODEL TRAINING & EVALUATION
# ==========================================

import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import (
    train_test_split,
    KFold,
    cross_val_score
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# PATHS
# ==========================================

DATASET_PATH = "dataset/code_dataset.csv"
MODEL_DIR = "model"

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(DATASET_PATH)

print("\n===================================")
print("   CODEGUARD AI MODEL EVALUATION")
print("===================================")

print("\nDataset shape:", df.shape)


# ==========================================
# FEATURES
# ==========================================

features = [
    "lines",
    "functions",
    "branches",
    "loops",
    "exception_handlers",
    "boolean_operations",
    "complexity",
    "nesting_depth",
    "long_lines",
    "duplicate_lines",
    "comments",
    "comment_ratio",
    "risky_calls"
]


X = df[features]

y_quality = df["quality_score"]

y_bug_risk = df["bug_risk"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_quality_train, y_quality_test, y_risk_train, y_risk_test = train_test_split(
    X,
    y_quality,
    y_bug_risk,
    test_size=0.2,
    random_state=42
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 5-FOLD CROSS VALIDATION
# ==========================================

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


print("\nCross-validation: 5-Fold")


# ==========================================
# MODEL FACTORY
# ==========================================

def create_models():

    return {

        "Random Forest": RandomForestRegressor(
            n_estimators=150,
            random_state=42
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=100,
            random_state=42
        ),

        "Linear Regression": LinearRegression()

    }


# ==========================================
# CROSS-VALIDATION FUNCTION
# ==========================================

def cross_validate_model(model, X_data, y_data):

    mae_scores = -cross_val_score(
        model,
        X_data,
        y_data,
        cv=cv,
        scoring="neg_mean_absolute_error"
    )

    mse_scores = -cross_val_score(
        model,
        X_data,
        y_data,
        cv=cv,
        scoring="neg_mean_squared_error"
    )

    r2_scores = cross_val_score(
        model,
        X_data,
        y_data,
        cv=cv,
        scoring="r2"
    )

    rmse_scores = np.sqrt(mse_scores)

    return {
        "MAE": round(float(mae_scores.mean()), 4),
        "RMSE": round(float(rmse_scores.mean()), 4),
        "R2": round(float(r2_scores.mean()), 4)
    }


# ==========================================
# HOLD-OUT TEST EVALUATION
# ==========================================

def evaluate_test_model(model, X_train, X_test, y_train, y_test):

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    return model, {
        "MAE": round(float(mae), 4),
        "RMSE": round(float(rmse), 4),
        "R2": round(float(r2), 4)
    }


# ==========================================
# QUALITY MODEL COMPARISON
# ==========================================

print("\n===================================")
print("       QUALITY MODEL COMPARISON")
print("===================================")

quality_results = {}

for name in create_models():

    # -------------------------------
    # Cross Validation
    # -------------------------------

    cv_model = create_models()[name]

    cv_metrics = cross_validate_model(
        cv_model,
        X_train,
        y_quality_train
    )

    # -------------------------------
    # Hold-out Test
    # -------------------------------

    test_model = create_models()[name]

    trained_model, test_metrics = evaluate_test_model(
        test_model,
        X_train,
        X_test,
        y_quality_train,
        y_quality_test
    )

    quality_results[name] = {

        "CV_MAE": cv_metrics["MAE"],
        "CV_RMSE": cv_metrics["RMSE"],
        "CV_R2": cv_metrics["R2"],

        "MAE": test_metrics["MAE"],
        "RMSE": test_metrics["RMSE"],
        "R2": test_metrics["R2"]

    }

    print(f"\n{name}")

    print("CV MAE :", cv_metrics["MAE"])
    print("CV RMSE:", cv_metrics["RMSE"])
    print("CV R²  :", cv_metrics["R2"])

    print("Test MAE :", test_metrics["MAE"])
    print("Test RMSE:", test_metrics["RMSE"])
    print("Test R²  :", test_metrics["R2"])


# ==========================================
# SELECT BEST QUALITY MODEL
# ==========================================

best_quality_name = min(
    quality_results,
    key=lambda name: quality_results[name]["CV_RMSE"]
)


best_quality_model = create_models()[best_quality_name]

best_quality_model.fit(
    X_train,
    y_quality_train
)


# ==========================================
# BUG RISK MODEL COMPARISON
# ==========================================

print("\n===================================")
print("        BUG RISK MODEL COMPARISON")
print("===================================")

risk_results = {}

for name in create_models():

    # -------------------------------
    # Cross Validation
    # -------------------------------

    cv_model = create_models()[name]

    cv_metrics = cross_validate_model(
        cv_model,
        X_train,
        y_risk_train
    )

    # -------------------------------
    # Hold-out Test
    # -------------------------------

    test_model = create_models()[name]

    trained_model, test_metrics = evaluate_test_model(
        test_model,
        X_train,
        X_test,
        y_risk_train,
        y_risk_test
    )

    risk_results[name] = {

        "CV_MAE": cv_metrics["MAE"],
        "CV_RMSE": cv_metrics["RMSE"],
        "CV_R2": cv_metrics["R2"],

        "MAE": test_metrics["MAE"],
        "RMSE": test_metrics["RMSE"],
        "R2": test_metrics["R2"]

    }

    print(f"\n{name}")

    print("CV MAE :", cv_metrics["MAE"])
    print("CV RMSE:", cv_metrics["RMSE"])
    print("CV R²  :", cv_metrics["R2"])

    print("Test MAE :", test_metrics["MAE"])
    print("Test RMSE:", test_metrics["RMSE"])
    print("Test R²  :", test_metrics["R2"])


# ==========================================
# SELECT BEST BUG RISK MODEL
# ==========================================

best_risk_name = min(
    risk_results,
    key=lambda name: risk_results[name]["CV_RMSE"]
)


best_risk_model = create_models()[best_risk_name]

best_risk_model.fit(
    X_train,
    y_risk_train
)


# ==========================================
# SAVE BEST MODELS
# ==========================================

joblib.dump(
    best_quality_model,
    os.path.join(
        MODEL_DIR,
        "quality_model.pkl"
    )
)

joblib.dump(
    best_risk_model,
    os.path.join(
        MODEL_DIR,
        "bug_risk_model.pkl"
    )
)

joblib.dump(
    features,
    os.path.join(
        MODEL_DIR,
        "features.pkl"
    )
)


# ==========================================
# SAVE EVALUATION RESULTS
# ==========================================

evaluation = {

    "dataset_samples": int(len(df)),

    "training_samples": int(len(X_train)),

    "testing_samples": int(len(X_test)),

    "cross_validation": {
        "method": "5-Fold K-Fold Cross Validation",
        "folds": 5
    },

    "quality_model": {

        "algorithm": best_quality_name,

        "MAE": quality_results[best_quality_name]["MAE"],

        "RMSE": quality_results[best_quality_name]["RMSE"],

        "R2": quality_results[best_quality_name]["R2"],

        "CV_MAE": quality_results[best_quality_name]["CV_MAE"],

        "CV_RMSE": quality_results[best_quality_name]["CV_RMSE"],

        "CV_R2": quality_results[best_quality_name]["CV_R2"]

    },

    "bug_risk_model": {

        "algorithm": best_risk_name,

        "MAE": risk_results[best_risk_name]["MAE"],

        "RMSE": risk_results[best_risk_name]["RMSE"],

        "R2": risk_results[best_risk_name]["R2"],

        "CV_MAE": risk_results[best_risk_name]["CV_MAE"],

        "CV_RMSE": risk_results[best_risk_name]["CV_RMSE"],

        "CV_R2": risk_results[best_risk_name]["CV_R2"]

    },

    "model_comparison": {

        "quality": quality_results,

        "bug_risk": risk_results

    }

}


with open(
    os.path.join(
        MODEL_DIR,
        "evaluation.json"
    ),
    "w"
) as file:

    json.dump(
        evaluation,
        file,
        indent=4
    )


# ==========================================
# FINAL RESULTS
# ==========================================

print("\n===================================")
print("          BEST MODELS")
print("===================================")

print("\nBest Quality Model:")
print(best_quality_name)

print("\nBest Bug Risk Model:")
print(best_risk_name)


print("\n-----------------------------------")
print("FILES SAVED")
print("-----------------------------------")

print("✓ quality_model.pkl")
print("✓ bug_risk_model.pkl")
print("✓ features.pkl")
print("✓ evaluation.json")

print("\n===================================")
print(" Model training completed successfully.")
print("===================================\n")