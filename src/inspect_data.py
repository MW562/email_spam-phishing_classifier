import pandas as pd
from pathlib import Path


DATA_FOLDER = Path("data/raw")


for file in DATA_FOLDER.glob("*.csv"):

    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")
    print("=" * 60)

    df = pd.read_csv(file, low_memory=False)

    print("\nRows:")
    print(len(df))

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3))

    if "label" in df.columns:
        print("\nLabel counts:")
        print(df["label"].value_counts(dropna=False))