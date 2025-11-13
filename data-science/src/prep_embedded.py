import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from io import StringIO

# Embedded CSV data - no external file access needed
EMBEDDED_CSV = """Segment,Kilometers_Driven,Mileage,Engine,Power,Seats,price
non-luxury segment,72000,26.6,998,58.16,5,5.51
non-luxury segment,41000,19.67,1582,126.2,5,16.06
non-luxury segment,46000,18.2,1199,88.7,5,8.61
non-luxury segment,87000,20.77,1248,88.76,7,11.27
non-luxury segment,75000,21.1,814,55.2,5,10.25
non-luxury segment,86999,23.08,1461,63.1,5,9.47
non-luxury segment,36000,11.36,2755,171.5,8,21
non-luxury segment,64430,20.54,1598,103.6,5,13.23
non-luxury segment,65932,22.3,1248,74,5,7.63
non-luxury segment,25692,21.56,1462,103.25,5,10.65
non-luxury segment,40670,19.91,1498,86,5,8.61
non-luxury segment,112000,16.5,1498,100,5,5.25
non-luxury segment,20282,21.01,1199,81.8,5,7.25
non-luxury segment,15000,19.1,1497,89,5,7
luxury segment,51000,15.76,2199,138.8,5,22.55
luxury segment,55000,15.2,1968,138.8,5,18.75
non-luxury segment,25000,23.84,1582,110.4,5,7.75
non-luxury segment,24371,18.9,1248,88.5,7,9.85
non-luxury segment,45000,19.3,1197,88.5,5,5.65
non-luxury segment,72000,18.6,1197,82,5,5.25
non-luxury segment,62000,23.84,1248,88.76,5,6.25
non-luxury segment,11000,23.84,1199,81.8,5,7.25
non-luxury segment,3435,17.01,1497,89,5,7.25
luxury segment,51000,15.76,2199,138.8,5,20.52
non-luxury segment,68000,16.4,1498,100,5,5.51
non-luxury segment,8000,19.7,1248,74,5,8.61
non-luxury segment,18828,18.6,1197,82,5,5.52
non-luxury segment,60000,16.5,1498,100,5,5.01
non-luxury segment,30000,17.21,1396,88.76,5,7.22
non-luxury segment,140000,19.91,1498,86,5,6.85
non-luxury segment,35000,19.4,1248,89,5,7
non-luxury segment,47000,17.01,1462,103.25,5,9.65
non-luxury segment,13000,17.01,1462,103.25,5,9.6
non-luxury segment,15000,23.84,1199,81.8,5,7.5
non-luxury segment,100000,16.5,1498,100,5,4.25
non-luxury segment,22249,17.11,1598,103.5,5,8.62
non-luxury segment,31864,18.9,1248,88.5,7,9.05
non-luxury segment,22500,17.21,1396,88.76,5,6
non-luxury segment,66129,16.5,1498,100,5,4.66
non-luxury segment,109000,16.5,1498,100,5,4.66
luxury segment,85000,10.5,2498,178,5,18.06
non-luxury segment,46433,21.01,1199,81.8,5,7.5
luxury segment,31000,21.01,1199,81.8,5,8.1
luxury segment,32000,11.4,3604,207,8,28.51
non-luxury segment,54000,16.5,1498,100,5,5.01
non-luxury segment,90000,17.73,1248,88.76,5,5.81
non-luxury segment,50000,16.5,1498,100,5,5.51
luxury segment,89000,13.2,1968,171,5,19.01
non-luxury segment,43000,17.01,1462,103.25,5,8.87
luxury segment,31000,10,3604,207,8,28.51
non-luxury segment,40000,16.5,1498,100,5,5.51
non-luxury segment,52132,17.01,1462,103.25,5,10.13
non-luxury segment,56879,17.01,1462,103.25,5,10.99
luxury segment,30119,16.8,1197,104.7,5,15.76
non-luxury segment,79000,23,1172,71,5,6.47
non-luxury segment,56000,17.01,1462,103.25,5,8.87
non-luxury segment,40000,19.4,1248,89,5,7.25
non-luxury segment,48767,25,1172,80,5,7.51
non-luxury segment,38000,19.7,1248,74,5,7.51
non-luxury segment,60000,25,1248,82,5,7.51
luxury segment,45000,10.8,3604,255,8,36.01
non-luxury segment,25000,18.9,1248,88.5,7,9.51
non-luxury segment,45000,19.7,1248,74,5,8.01
non-luxury segment,14465,19.4,1248,89,5,6.81
non-luxury segment,80000,19,1172,71,5,6.85
luxury segment,29000,11.6,3604,255,8,37.01
non-luxury segment,72039,17.01,1462,103.25,5,9.51
non-luxury segment,35000,25,1248,82,5,8.41
non-luxury segment,60000,19,1248,88.7,5,7.51
luxury segment,110000,13.2,1968,171,5,17.76
non-luxury segment,20000,19.7,1248,74,5,8.26
non-luxury segment,47427,18.9,1248,88.5,7,9.5
non-luxury segment,25000,19.4,1248,89,5,7.51
non-luxury segment,21780,18.9,1248,88.5,7,8.91
non-luxury segment,60000,24.1,1248,82.85,5,7.25
non-luxury segment,120000,16,1493,90.2,5,4.26
non-luxury segment,46000,26.6,998,67.04,5,5.76
non-luxury segment,20000,19.7,1248,74,5,8.51
non-luxury segment,25000,25,1248,82,5,8.76
non-luxury segment,26000,24.1,1248,82.85,5,7.25
non-luxury segment,16700,19.4,1248,89,5,7.76
non-luxury segment,25000,19.3,1197,88.5,5,7.76
non-luxury segment,112000,16,1493,90.2,5,4.76
luxury segment,28571,11.4,3604,207,8,33.02
non-luxury segment,61203,17.01,1462,103.25,5,10.01
non-luxury segment,25000,18.9,1248,88.5,7,10.01
non-luxury segment,35000,18.9,1248,88.5,7,9.76
non-luxury segment,41000,24,1197,83.14,5,6.25
non-luxury segment,80000,23.08,1461,63.1,5,7.76
non-luxury segment,48000,25,1248,82,5,7.76
luxury segment,80000,13.9,2179,138,5,20.26
non-luxury segment,23000,22.4,1248,82.85,5,6.76
non-luxury segment,75000,24,1197,83.14,5,7.51
luxury segment,80000,13.2,1968,171,5,18.01
non-luxury segment,27000,19.7,1248,74,5,8.26
non-luxury segment,10000,19.4,1248,89,5,7.26
non-luxury segment,14000,18.9,1248,88.5,7,9.01
non-luxury segment,50000,19.3,1197,88.5,5,6.76
non-luxury segment,31000,22.54,1197,81.8,5,6.76
non-luxury segment,75557,17.01,1462,103.25,5,10.01
non-luxury segment,41000,18.9,1248,88.5,7,9.51
non-luxury segment,110000,16,1493,90.2,5,3.85
non-luxury segment,17000,25,1248,82,5,8.51
luxury segment,51000,8.2,4951,335,5,55.01
non-luxury segment,20411,18.9,1248,88.5,7,9.01
non-luxury segment,30000,22.54,1197,81.8,5,7.01
non-luxury segment,25000,18.9,1248,88.5,7,9.51
non-luxury segment,22000,18.9,1248,88.5,7,9.76
non-luxury segment,35000,25,1248,82,5,8.01
non-luxury segment,66000,16,1493,90.2,5,4.76
non-luxury segment,40000,22.38,1199,88.5,7,9.01
luxury segment,30000,10.8,3604,255,8,38.51
luxury segment,60000,11.8,3604,254,8,34.52
non-luxury segment,72039,24,1197,83.14,5,6.76
non-luxury segment,25000,19.7,1248,74,5,7.26
non-luxury segment,41000,21.13,1368,88.5,5,8.13
luxury segment,41000,10.8,3604,255,8,37.51
non-luxury segment,60000,26.6,998,67.04,5,5.26
non-luxury segment,20000,21.14,1498,99,5,10.51
non-luxury segment,7000,18.9,1248,88.5,7,9.26
non-luxury segment,49000,22.54,1197,81.8,5,5.26
non-luxury segment,40000,25,1248,82,5,7.76
luxury segment,25000,10.8,3604,255,8,39.51
non-luxury segment,23000,18.9,1248,88.5,7,10.01
non-luxury segment,22500,24.3,1197,83.1,5,8.01
non-luxury segment,13000,17.5,1582,125.3,5,11.63
non-luxury segment,35000,18.9,1248,88.5,7,9.51
non-luxury segment,8500,25,1248,82,5,8.51
non-luxury segment,119000,16.5,1498,100,5,4.51
non-luxury segment,48000,24.3,1197,83.1,5,7.01
luxury segment,70000,11.8,3604,254,8,29.76
non-luxury segment,11000,22.54,1197,81.8,5,7.51
non-luxury segment,22000,22.54,1197,81.8,5,6.51
non-luxury segment,22700,21.13,1368,88.5,5,8.76
non-luxury segment,45000,18.9,1248,88.5,7,9.76
non-luxury segment,16934,21.14,1498,99,5,8.76
non-luxury segment,15000,21.14,1498,99,5,9.01
non-luxury segment,25000,18.9,1248,88.5,7,9.01
non-luxury segment,4341,24.3,1197,83.1,5,7.76
non-luxury segment,38000,18.9,1248,88.5,7,9.01
luxury segment,36000,11.8,3604,254,8,33.52
luxury segment,72000,11.8,3604,254,8,29.52
non-luxury segment,60000,17.5,1582,125.3,5,12.51
non-luxury segment,36566,21.13,1368,88.5,5,9.51
non-luxury segment,50000,22.54,1197,81.8,5,6.26
non-luxury segment,30000,22.54,1197,81.8,5,6.26
luxury segment,71000,12.6,2996,245,5,36.26
non-luxury segment,61000,17.5,1582,125.3,5,11.26
luxury segment,35000,8.9,5204,306,7,38.01
non-luxury segment,35000,21.14,1498,99,5,9.26
luxury segment,40000,12.6,2996,245,5,37.01
non-luxury segment,35000,22.54,1197,81.8,5,7.26
non-luxury segment,96000,18.9,1248,88.5,7,8.26
non-luxury segment,34800,22.27,1248,82.85,5,5.76
non-luxury segment,45000,22.54,1197,81.8,5,6.26
non-luxury segment,47132,22.38,1199,88.5,7,8.76
non-luxury segment,22500,22.54,1197,81.8,5,7.26
luxury segment,40000,12.6,2996,245,5,37.76
non-luxury segment,45000,19.3,1197,88.5,5,6.76
non-luxury segment,87934,17.5,1582,125.3,5,10.26
non-luxury segment,110000,22.38,1199,88.5,7,8.01
luxury segment,75000,12.6,2996,245,5,33.76
non-luxury segment,30000,18.9,1248,88.5,7,10.26
luxury segment,125000,11,2987,215.2,5,17.76
non-luxury segment,30000,21.14,1498,99,5,9.76
non-luxury segment,45000,18.9,1248,88.5,7,10.01
non-luxury segment,23781,21.01,1199,81.8,5,8.01
luxury segment,31000,16.8,1197,104.7,5,16.51
non-luxury segment,47132,18.9,1248,88.5,7,9.26
luxury segment,30000,12.6,2996,245,5,37.01
non-luxury segment,48000,18.9,1248,88.5,7,8.76
non-luxury segment,55000,17.5,1582,125.3,5,11.01
luxury segment,25000,8.9,5204,306,7,41.01
luxury segment,72000,12.6,2996,245,5,34.26
non-luxury segment,36000,18.9,1248,88.5,7,9.51
luxury segment,40000,13.5,2179,170,5,24.01
luxury segment,40000,13.5,2179,168,5,22.76
luxury segment,50000,13.5,2179,168,5,23.01
non-luxury segment,70000,24.3,1197,83.1,5,7.76
non-luxury segment,17000,18.9,1248,88.5,7,11.01
non-luxury segment,45000,17.5,1582,125.3,5,11.51
luxury segment,51000,11,2987,215.2,5,21.76
non-luxury segment,60000,22.38,1199,88.5,7,8.51
non-luxury segment,7000,18.9,1248,88.5,7,10.76
luxury segment,25000,12.6,2996,245,5,39.26"""

def main(args):
    print("🚀 prep_embedded.py started - using embedded CSV data", flush=True)
    
    # Load data from embedded string
    df = pd.read_csv(StringIO(EMBEDDED_CSV))
    print(f"📊 Loaded embedded data: {df.shape}", flush=True)
    
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(args.train_data, exist_ok=True)
    os.makedirs(args.test_data, exist_ok=True)

    train_df.to_csv(os.path.join(args.train_data, "train.csv"), index=False)
    test_df.to_csv(os.path.join(args.test_data, "test.csv"), index=False)

    print(f"✅ Train rows: {len(train_df)}, Test rows: {len(test_df)}")
    print("🏁 prep_embedded.py finished", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_data", type=str)
    parser.add_argument("--test_data", type=str)
    args = parser.parse_args()
    main(args)
