import argparse
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()

print(f"📥 Loading model from: {args.model}")
model = joblib.load(Path(args.model) / "model.pkl")

# Dummy data for tuning (in real case, load from somewhere)
df = pd.read_csv("github_workflows/src/sample_data.csv")
X = df.drop("target", axis=1)
y = df["target"]

param_grid = {"C": [0.1, 1.0, 10.0]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=3)
grid.fit(X, y)

print(f"📤 Saving best model to: {args.output}")
Path(args.output).mkdir(parents=True, exist_ok=True)
joblib.dump(grid.best_estimator_, Path(args.output) / "best_model.pkl")
