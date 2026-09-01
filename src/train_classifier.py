from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


DATA_FILE = Path("data/processed/emails.csv")
MODEL_FILE = Path("models/email_classifier.pkl")


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

df = df.dropna(
    subset=["text", "label"]
)


X = df["text"]
y = df["label"]


print(f"Total emails: {len(df)}")

print("\nClass distribution:")
print(y.value_counts())


# --------------------------------------------------
# Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining emails:", len(X_train))
print("Testing emails:", len(X_test))


# --------------------------------------------------
# Build model
# --------------------------------------------------

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",

            # Look at individual words and
            # two-word combinations
            ngram_range=(1, 2),

            # Ignore extremely rare features
            min_df=2,

            # Prevent enormous feature matrices
            max_features=60000
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])


# --------------------------------------------------
# Train
# --------------------------------------------------

print("\nTraining classifier...")

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

print("\nTesting classifier...")

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\nAccuracy:")
print(f"{accuracy:.2%}")


print("\nClassification report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Legitimate",
            "Malicious"
        ]
    )
)


print("\nConfusion matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# --------------------------------------------------
# Save classifier
# --------------------------------------------------

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)


print(
    f"\nClassifier saved to {MODEL_FILE}"
)