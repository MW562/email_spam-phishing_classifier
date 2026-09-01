from pathlib import Path

import pandas as pd


RAW_FOLDER = Path("data/raw")
OUTPUT_FILE = Path("data/processed/emails.csv")

def normalize_label(value):

    value = str(value).strip().lower()

    safe_labels = {
        "0",
        "safe",
        "safe email",
        "ham",
        "legitimate",
        "legit"
    }

    malicious_labels = {
        "1",
        "spam",
        "phishing",
        "phishing email",
        "malicious"
    }

    if value in safe_labels:
        return 0

    if value in malicious_labels:
        return 1

    return None

def find_column(df, possible_names):
    """Find a column regardless of capitalization."""
    column_lookup = {
        str(col).lower().strip(): col
        for col in df.columns
    }

    for name in possible_names:
        if name.lower() in column_lookup:
            return column_lookup[name.lower()]

    return None


def load_dataset(file_path):
    print(f"Loading {file_path.name}...")

    df = pd.read_csv(file_path, low_memory=False)

    subject_col = find_column(
        df,
        ["subject", "email subject"]
    )

    body_col = find_column(
        df,
        ["body", "text", "email text", "message"]
    )

    label_col = find_column(
        df,
        ["label", "email type", "type"]
    )

    if body_col is None:
        print(f"Skipping {file_path.name}: couldn't find body column.")
        return None

    if label_col is None:
        print(f"Skipping {file_path.name}: couldn't find label column.")
        return None

    # Get subject if available
    if subject_col is not None:
        subject = df[subject_col].fillna("").astype(str)
    else:
        subject = ""

    body = df[body_col].fillna("").astype(str)

    # Combine subject and body
    df_clean = pd.DataFrame()

    df_clean["text"] = (
        subject + "\n\n" + body
    ).str.strip()

    df_clean["label"] = df[label_col].apply(normalize_label)

    df_clean["source"] = file_path.stem

    return df_clean


all_datasets = []


for file_path in RAW_FOLDER.glob("*.csv"):

    cleaned = load_dataset(file_path)

    if cleaned is not None:
        all_datasets.append(cleaned)


combined = pd.concat(
    all_datasets,
    ignore_index=True
)


print("\nOriginal rows:", len(combined))


# Remove rows where the label could not be recognized
combined = combined.dropna(
    subset=["label"]
)

# Convert labels from floats like 0.0 / 1.0 to integers 0 / 1
combined["label"] = combined["label"].astype(int)


# Remove emails with no text
combined = combined[
    combined["text"].str.len() > 0
]


# Remove duplicate email bodies
combined = combined.drop_duplicates(
    subset=["text"]
)


print("Rows after cleanup:", len(combined))


print("\nCurrent labels:")
print(combined["label"].value_counts(dropna=False))


print("\nSources:")
print(combined["source"].value_counts())

print("\nLabels by source:")
print(
    combined.groupby(
        ["source", "label"]
    ).size()
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

combined.to_csv(
    OUTPUT_FILE,
    index=False
)


print(f"\nSaved to {OUTPUT_FILE}")