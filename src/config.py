from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGDIR = ROOT / "results" / "figures"

RAW_CSV = DATA_RAW / "ai4i2020.csv"
FEATURES_CSV = DATA_PROCESSED / "ai4i_features.csv"

def load_raw():
    import pandas as pd
    return pd.read_csv(RAW_CSV, encoding="utf-8-sig")
