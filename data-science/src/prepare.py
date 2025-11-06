#!/usr/bin/env python3
import argparse, json, os, sys, traceback
from datetime import datetime
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare dataset for training")
    parser.add_argument("--raw_data", required=True, help="Path to raw data file")
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=42)
    args = parser.parse_args()
    print(f"[DEBUG] Parsed args: {vars(args)}", flush=True)
    return args

def ensure_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"[WARN] Could not create directory {path}: {e}", flush=True)

def write_json(path: str, data: dict):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[DEBUG] Diagnostics written to: {path}", flush=True)
    except Exception as e:
        print(f"[WARN] Failed to write diagnostics: {e}", flush=True)

def main():
    args = parse_args()
    raw_path = args.raw_data

    if not os.path.exists(raw_path):
        print(f"[ERROR] Raw data path does not exist: {raw_path}", flush=True)
        sys.exit(1)

    if os.path.isdir(raw_path):
        csvs = [f for f in os.listdir(raw_path) if f.lower().endswith(".csv")]
        if len(csvs) == 1:
            raw_path = os.path.join(raw_path, csvs[0])
            print(f"[DEBUG] Found CSV in directory: {raw_path}", flush=True)
        else:
            print(f"[ERROR] Directory contains no or multiple CSVs: {csvs}", flush=True)
            sys.exit(1)

    try:
        df = pd.read_csv(raw_path)
        print(f"[DEBUG] Read CSV with shape {df.shape}", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}", flush=True)
        sys.exit(1)

    if df.shape[0] == 0:
        print("[ERROR] CSV contains zero rows", flush=True)
        sys.exit(1)

    try:
        df_shuffled = df.sample(frac=1.0, random_state=args.random_state).reset_index(drop=True)
        split_idx = int(df.shape[0] * (1.0 - args.test_size))
        df_train = df_shuffled.iloc[:split_idx].reset_index(drop=True)
        df_test = df_shuffled.iloc[split_idx:].reset_index(drop=True)
        print(f"[DEBUG] Train shape: {df_train.shape}, Test shape: {df_test.shape}", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to split data: {e}", flush=True)
        sys.exit(1)

    # Write outputs
    ensure_dir("outputs/train")
    ensure_dir("outputs/test")
    try:
        df_train.to_csv("outputs/train/train.csv", index=False)
        df_test.to_csv("outputs/test/test.csv", index=False)
        print("[DEBUG] CSVs written successfully", flush=True)
    except Exception as e:
        print(f"[WARN] Failed to write CSVs: {e}", flush=True)

    # Write diagnostics
    diagnostics = {
        "status": "completed",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "raw_data": raw_path,
        "raw_rows": df.shape[0],
        "train_rows": df_train.shape[0],
        "test_rows": df_test.shape[0],
        "test_size": args.test_size,
        "random_state": args.random_state,
        "train_csv": "outputs/train/train.csv",
        "test_csv": "outputs/test/test.csv"
    }
    write_json("outputs/prep_diagnostics.json", diagnostics)

    print("✅ Data preparation complete.", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}", flush=True)
        traceback.print_exc()
        write_json("outputs/prep_diagnostics.json", {"status": "failed", "exception": str(e)})
        sys.exit(1)


# #!/usr/bin/env python3
# """
# Data preparation script for the used-cars pipeline.

# Behavior:
# - Parses command line arguments (--raw_data, --train_output, --test_output).
# - Resolves whether raw_data is a local path, a mounted path, or an AzureML placeholder.
# - Reads CSV (pandas), splits into train/test (default 80/20), writes CSV outputs.
# - Emits debug prints to stdout for early-failure visibility and writes a prep_diagnostics.json
#   file into the train output folder with metadata about the run.
# - Exits with non-zero code on error.

# Usage example:
# python prepare.py --raw_data /path/to/used_cars.csv --train_output ./outputs/train --test_output ./outputs/test
# """

# import argparse
# import json
# import os
# import sys
# import traceback
# from datetime import datetime

# import pandas as pd

# def parse_args():
#     import time
#     print(f"[DEBUG] Argument parsing started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     parser = argparse.ArgumentParser(description="Prepare dataset for training")

#     # ⚠️ train_output и test_output са премахнати — записваме локално в ./outputs/
#     parser.add_argument(
#         "--raw_data", required=True, help="Path to raw data file (local path or AzureML asset placeholder)"
#     )
#     parser.add_argument(
#         "--test_size",
#         type=float,
#         default=0.2,
#         help="Fraction of data to reserve for test set (default: 0.2)",
#     )
#     parser.add_argument(
#         "--random_state", type=int, default=42, help="Random state for reproducible splits (default: 42)"
#     )

#     args = parser.parse_args()

#     print(f"[DEBUG] Parsed arguments:")
#     print(f"         raw_data      = {args.raw_data}")
#     print(f"         test_size     = {args.test_size}")
#     print(f"         random_state  = {args.random_state}")
#     print(f"[DEBUG] Argument parsing completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     return args




# def parse_args():
#     parser = argparse.ArgumentParser(description="Prepare dataset for training")
#     parser.add_argument(
#         "--raw_data", required=True, help="Path to raw data file (local path or AzureML asset placeholder)"
#     )
#     parser.add_argument(
#         "--train_output", required=True, help="Directory where train split will be written (uri_folder output)"
#     )
#     parser.add_argument(
#         "--test_output", required=True, help="Directory where test split will be written (uri_folder output)"
#     )
#     parser.add_argument(
#         "--test_size",
#         type=float,
#         default=0.2,
#         help="Fraction of data to reserve for test set (default: 0.2)",
#     )
#     parser.add_argument(
#         "--random_state", type=int, default=42, help="Random state for reproducible splits (default: 42)"
#     )
#     return parser.parse_args()


def is_azureml_placeholder(path_str: str) -> bool:
    if not isinstance(path_str, str):
        return False
    return path_str.startswith("azureml:") or path_str.startswith("azureml://")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_diagnostics(out_dir: str, diag: dict):
    try:
        ensure_dir(out_dir)
        diag_path = os.path.join(out_dir, "prep_diagnostics.json")
        with open(diag_path, "w", encoding="utf-8") as f:
            json.dump(diag, f, indent=2, default=str)
        print(f"Diagnostics written to: {diag_path}", flush=True)
    except Exception as e:
        print(f"Failed to write diagnostics to {out_dir}: {e}", flush=True)


def fail(message: str, exc: Exception = None):
    """Print failure message, diagnostics and exit non-zero."""
    print(f"ERROR: {message}", file=sys.stderr, flush=True)
    if exc is not None:
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
    sys.stderr.flush()
    # try to write a minimal diagnostics file in current directory
    try:
        write_diagnostics(".", {"status": "failed", "message": message, "exception": str(exc)})
    except Exception:
        pass
    sys.exit(1)


def main():
    args = parse_args()

    # Basic debug output for early failure diagnosis
    print(f"DEBUG: args.raw_data = {args.raw_data}", flush=True)
    print(f"DEBUG: args.train_output = {args.train_output}", flush=True)
    print(f"DEBUG: args.test_output = {args.test_output}", flush=True)
    print(f"DEBUG: test_size = {args.test_size}, random_state = {args.random_state}", flush=True)

    # Ensure output directories exist (AzureML will map uri_folder outputs; create local directories for the job)
    try:
        ensure_dir(args.train_output)
        ensure_dir(args.test_output)
    except Exception as e:
        fail("Could not create output directories", e)

    # Defensive check: if AzureML placeholder was passed instead of a resolved local path, fail early with clear message
    if is_azureml_placeholder(args.raw_data):
        # AzureML normally resolves asset placeholders to a local path when input is passed with mode=download or ro_mount.
        # If we get here, the job likely received the literal asset URI (unmounted). Fail fast with hints.
        fail(
            "Input raw_data was not resolved to a local path. Received AzureML asset placeholder "
            f"'{args.raw_data}'. Ensure the job input was passed as an Input asset with mode='download' or 'ro_mount'."
        )

    # Check that raw_data exists and is a file
    raw_path = args.raw_data
    if not os.path.exists(raw_path):
        fail(f"Raw data path does not exist: {raw_path}")

    if os.path.isdir(raw_path):
        # If a directory was passed accidentally, try to find a CSV inside (helpful guard)
        candidates = [f for f in os.listdir(raw_path) if f.lower().endswith(".csv")]
        if not candidates:
            fail(f"Raw data path is a directory and contains no CSV files: {raw_path}")
        elif len(candidates) == 1:
            raw_path = os.path.join(raw_path, candidates[0])
            print(f"DEBUG: Found single CSV in directory, using: {raw_path}", flush=True)
        else:
            # multiple CSV files—fail and ask user to provide exact file path
            fail(f"Raw data path is a directory with multiple CSV files; please provide the exact CSV file. Files: {candidates}")

    if not os.path.isfile(raw_path):
        fail(f"Raw data is not a file: {raw_path}")

    # At this point raw_path should be a local CSV file path
    try:
        df = pd.read_csv(raw_path)
        print(f"DEBUG: Read CSV with shape {df.shape}", flush=True)
    except Exception as e:
        fail(f"Failed to read CSV at {raw_path}", e)

    # Basic sanity checks
    if df.shape[0] == 0:
        fail("Input CSV contains zero rows")

    # Create train/test splits
    try:
        test_size = float(args.test_size)
        if not (0.0 < test_size < 1.0):
            fail("test_size must be between 0 and 1 (exclusive)")
        split_idx = int(df.shape[0] * (1.0 - test_size))
        # simple deterministic split using shuffle with random_state for reproducibility
        df_shuffled = df.sample(frac=1.0, random_state=args.random_state).reset_index(drop=True)
        df_train = df_shuffled.iloc[:split_idx].reset_index(drop=True)
        df_test = df_shuffled.iloc[split_idx:].reset_index(drop=True)
        print(f"DEBUG: Train shape {df_train.shape}, Test shape {df_test.shape}", flush=True)
    except Exception as e:
        fail("Failed to split dataset", e)

    # Write outputs (CSV files)
    try:
        train_file = os.path.join(args.train_output, "train.csv")
        test_file = os.path.join(args.test_output, "test.csv")
        df_train.to_csv(train_file, index=False)
        df_test.to_csv(test_file, index=False)
        print(f"DEBUG: Wrote train CSV to {train_file}", flush=True)
        print(f"DEBUG: Wrote test CSV to {test_file}", flush=True)
    except Exception as e:
        fail("Failed to write train/test CSV outputs", e)

    # Collect diagnostics
    diagnostics = {
        "status": "completed",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "raw_data_provided": args.raw_data,
        "raw_data_resolved_path": raw_path,
        "raw_rows": int(df.shape[0]),
        "train_rows": int(df_train.shape[0]),
        "test_rows": int(df_test.shape[0]),
        "test_size": args.test_size,
        "random_state": args.random_state,
        "train_csv": train_file,
        "test_csv": test_file,
    }

    # Try to write diagnostics into train output (primary output location)
    try:
        write_diagnostics(args.train_output, diagnostics)
    except Exception as e:
        print(f"WARNING: Failed to write diagnostics into train_output: {e}", file=sys.stderr, flush=True)

    # Final success message with experiment/run visibility
    print("✅ Data preparation complete.", flush=True)
    print(f"Train rows: {diagnostics['train_rows']}, Test rows: {diagnostics['test_rows']}", flush=True)

    # Exit normally
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        # Catch-any to ensure we print tracebacks to the job log for diagnosis
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
        # Attempt to write a minimal diagnostics JSON to cwd
        try:
            write_diagnostics(".", {"status": "failed", "exception": str(exc), "trace": traceback.format_exc()})
        except Exception:
            pass
        sys.exit(1)
