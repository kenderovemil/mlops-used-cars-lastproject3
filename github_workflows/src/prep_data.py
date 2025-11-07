import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str, required=True)
parser.add_argument("--output_data", type=str, required=True)
args = parser.parse_args()

print(f"📥 Loading raw data from: {args.input_data}")
df = pd.read_csv(args.input_data)

# Minimal preprocessing
df = df.dropna()
df = df.reset_index(drop=True)

print(f"📤 Saving cleaned data to: {args.output_data}")
Path(args.output_data).mkdir(parents=True, exist_ok=True)
df.to_csv(Path(args.output_data) / "clean_data.csv", index=False)
