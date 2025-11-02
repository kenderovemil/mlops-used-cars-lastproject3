#!/usr/bin/env python3
import argparse
import os
import joblib
import pandas as pd
from typing import Optional

def main(model_input_path: str, train_csv_path: Optional[str], model_name: str):
    # --- Локална директория за артефакти ---
    out_path = os.path.join(os.path.dirname(__file__), "local_output")
    os.makedirs(out_path, exist_ok=True)

    # --- Load model (само за проверка) ---
    if not os.path.exists(model_input_path):
        raise FileNotFoundError(f"Model file not found at {model_input_path}")
    model = joblib.load(model_input_path)

    # --- Optional: load training data (само за диагностика) ---
    if train_csv_path and os.path.exists(train_csv_path):
        train_df = pd.read_csv(train_csv_path)
        print("Train data shape:", train_df.shape)

    # --- Write result artifact ---
    out_file = os.path.join(out_path, "reg_model_output.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("✅ Model validated successfully.\n\n")
        f.write(f"📍 Path to the model: {model_input_path}\n")
        f.write(f"📌 Intended Model Name: {model_name}\n")
        f.write("🕊️ This is an act of alignment and backup.\n")

    print("✅ Model validated and artifact written to:", out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_input_path", type=str, required=True, help="Path to model.pkl")
    parser.add_argument("--train_csv_path", type=str, required=False, default=None, help="Optional path to train.csv")
    parser.add_argument("--model_name", type=str, required=True, help="Name under which to register the model")
    args = parser.parse_args()
    main(args.model_input_path, args.train_csv_path, args.model_name)



# #!/usr/bin/env python3
# import argparse
# import os
# import joblib
# import pandas as pd
# from typing import Optional

# def main(model_input_path: str, train_csv_path: Optional[str], model_name: str):
#     os.makedirs("best_registered_model", exist_ok=True)

#     # --- Load model (само за проверка) ---
#     if not os.path.exists(model_input_path):
#         raise FileNotFoundError(f"Model file not found at {model_input_path}")
#     model = joblib.load(model_input_path)

#     # --- Optional: load training data (само за диагностика) ---
#     if train_csv_path and os.path.exists(train_csv_path):
#         train_df = pd.read_csv(train_csv_path)
#         print("Train data shape:", train_df.shape)

#     # --- Write result artifact ---
#     out_path = "best_registered_model"
#     with open(os.path.join(out_path, "reg_model_output.txt"), "w", encoding="utf-8") as f:
#         f.write("✅ Model validated successfully.\n\n")
#         f.write(f"📍 Path to the model: {model_input_path}\n")
#         f.write(f"📌 Intended Model Name: {model_name}\n")
#         f.write("🕊️ This is an act of alignment and backup.\n")

#     print("✅ Model validated and artifact written to:", out_path)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model_input_path", type=str, required=True, help="Path to model.pkl")
#     parser.add_argument("--train_csv_path", type=str, required=False, default=None, help="Optional path to train.csv")
#     parser.add_argument("--model_name", type=str, required=True, help="Name under which to register the model")
#     args = parser.parse_args()
#     main(args.model_input_path, args.train_csv_path, args.model_name)

