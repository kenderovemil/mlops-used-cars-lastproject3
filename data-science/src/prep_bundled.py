import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def main(args):
    print("🚀 prep_bundled.py started", flush=True)
    
    # If raw_data path fails, fall back to bundled CSV
    try:
        df = pd.read_csv(args.raw_data)
        print(f"✅ Loaded data from: {args.raw_data}", flush=True)
    except Exception as e:
        print(f"⚠️  Failed to load from {args.raw_data}: {e}", flush=True)
        print("📦 Loading bundled CSV from code directory...", flush=True)
        
        # Try to find the CSV in the code directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bundled_csv = os.path.join(script_dir, "used_cars.csv")
        
        if os.path.exists(bundled_csv):
            df = pd.read_csv(bundled_csv)
            print(f"✅ Loaded bundled data from: {bundled_csv}", flush=True)
        else:
            raise FileNotFoundError(f"Neither {args.raw_data} nor {bundled_csv} found")
    
    print(f"📊 Raw data shape: {df.shape}", flush=True)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(args.train_data, exist_ok=True)
    os.makedirs(args.test_data, exist_ok=True)

    train_df.to_csv(os.path.join(args.train_data, "train.csv"), index=False)
    test_df.to_csv(os.path.join(args.test_data, "test.csv"), index=False)

    print(f"✅ Train rows: {len(train_df)}, Test rows: {len(test_df)}")
    print("🏁 prep_bundled.py finished", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", type=str, default="used_cars.csv")
    parser.add_argument("--train_data", type=str)
    parser.add_argument("--test_data", type=str)
    args = parser.parse_args()
    main(args)
