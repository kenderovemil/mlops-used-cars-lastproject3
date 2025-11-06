import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import json
from datetime import datetime

def write_diagnostics(args, log_path, train_rows, test_rows):
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            f.write("=== PREP DATA DIAGNOSTICS ===\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n\n")

            f.write(">>> ARGUMENTS:\n")
            f.write(json.dumps(vars(args), indent=2))
            f.write("\n\n")

            f.write(">>> ENVIRONMENT VARIABLES (partial):\n")
            env = {k: v for k, v in os.environ.items() if "AZUREML" in k or "ML" in k}
            f.write(json.dumps(env, indent=2))
            f.write("\n\n")

            f.write(">>> OUTPUT SUMMARY:\n")
            f.write(f"Train rows: {train_rows}\n")
            f.write(f"Test rows: {test_rows}\n")
            f.write(f"Train path: {args.train_data}\n")
            f.write(f"Test path: {args.test_data}\n")
            f.write("\n=== END ===\n")
    except Exception as e:
        print(f"⚠️ Failed to write diagnostics: {e}", flush=True)

def main(args):
    print("🚀 prep.py started", flush=True)
    df = pd.read_csv(args.raw_data)
    print(f"✅ Raw data shape: {df.shape}", flush=True)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(args.train_data, exist_ok=True)
    os.makedirs(args.test_data, exist_ok=True)

    train_df.to_csv(os.path.join(args.train_data, "train.csv"), index=False)
    test_df.to_csv(os.path.join(args.test_data, "test.csv"), index=False)

    print(f"✅ Train rows: {len(train_df)}, Test rows: {len(test_df)}")

    # Запис на диагностичен лог
    # log_path = "/mnt/batch/tasks/shared/LS_root/mounts/clusters/lastprojectcompute/code/Users/kenderov.emil/notes/notes/prep_diagnostics.txt"
    log_path = os.path.join(args.train_data, "prep_diagnostics.txt")


    write_diagnostics(args, log_path, len(train_df), len(test_df))
    print("🏁 prep.py finished", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_data", type=str)
    parser.add_argument("--train_data", type=str)
    parser.add_argument("--test_data", type=str)
    args = parser.parse_args()
    main(args)

# import argparse
# import pandas as pd
# from sklearn.model_selection import train_test_split
# import os

# def main(args):
#     df = pd.read_csv(args.raw_data)
#     train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

#     os.makedirs(args.train_data, exist_ok=True)
#     os.makedirs(args.test_data, exist_ok=True)

#     train_df.to_csv(os.path.join(args.train_data, "train.csv"), index=False)
#     test_df.to_csv(os.path.join(args.test_data, "test.csv"), index=False)

#     print(f"✅ Train rows: {len(train_df)}, Test rows: {len(test_df)}")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--raw_data", type=str)
#     parser.add_argument("--train_data", type=str)
#     parser.add_argument("--test_data", type=str)
#     args = parser.parse_args()
#     main(args)

