import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path


# Paths
DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# Load data & model
def load_data():
    df = pd.read_csv(DATA_DIR / "bigmart_processed.csv")
    return df

def load_model():
    return joblib.load(MODEL_DIR / "pricing_model.pkl")


# Feature Importance
def plot_feature_importance(model, X):
    if not hasattr(model, "feature_importances_"):
        print("Model does not support feature importance.")
        return

    importances = model.feature_importances_
    features = X.columns

    fi_df = pd.DataFrame({
        "feature": features,
        "importance": importances
    }).sort_values(by="importance", ascending=False).head(15)

    plt.figure(figsize=(8,5))
    plt.barh(fi_df["feature"], fi_df["importance"])
    plt.gca().invert_yaxis()
    plt.title("Top 15 Feature Importances")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance.png")
    plt.show()

    fi_df.to_csv(OUTPUT_DIR / "feature_importance.csv", index=False)
    print("Feature importance saved.")


# Error Analysis
def error_analysis(model, X, y):
    preds = model.predict(X)
    errors = y - preds

    error_df = pd.DataFrame({
        "actual": y,
        "predicted": preds,
        "error": errors
    })

    print("\nError Statistics")
    print(error_df["error"].describe())

    error_df.to_csv(OUTPUT_DIR / "prediction_errors.csv", index=False)

# Main evaluation pipeline

def main():
    df = load_data()
    model = load_model()

    y = df["MRP"]
    X = df.drop(columns=["MRP"])
    X = X.select_dtypes(include=[np.number])

    plot_feature_importance(model, X)
    error_analysis(model, X, y)

    print("\nEvaluation completed. Check outputs/ folder.")


if __name__ == "__main__":
    main()