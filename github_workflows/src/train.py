import argparse
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()

print(f"📥 Loading cleaned data from: {args.data}")
df = pd.read_csv(Path(args.data) / "clean_data.csv")

X = df.drop("target", axis=1)
y = df["target"]

model = LogisticRegression()
model.fit(X, y)

print(f"📤 Saving model to: {args.output}")
Path(args.output).mkdir(parents=True, exist_ok=True)
joblib.dump(model, Path(args.output) / "model.pkl")
