# Email Spam / Phishing Classifier

A machine learning project for classifying email messages as either **legitimate** or **malicious** using natural language processing.

The current version trains a binary email classifier using approximately 40,000 emails collected from several public email datasets. Email subject lines and message bodies are converted into numerical features using **TF-IDF**, then classified using **Logistic Regression**.

This classifier is intended to serve as the machine learning component of a larger email spam and phishing detection application.

## Current Status

**Version 1 — Binary Email Classifier**

The current model classifies emails into two categories:

* `0` — Legitimate
* `1` — Malicious / Spam / Phishing

The current version focuses only on the textual content of an email. Future versions will incorporate additional phishing indicators such as URLs, sender information, email headers, and attachment characteristics.

## Model Performance

The processed dataset contains **40,437 emails**.

| Class      |     Emails |
| ---------- | ---------: |
| Legitimate |     19,882 |
| Malicious  |     20,555 |
| **Total**  | **40,437** |

The dataset was split into:

* **32,349 training emails**
* **8,088 testing emails**
* 80/20 train-test split

### Test Results

**Accuracy: 98.52%**

| Class      | Precision | Recall | F1 Score |
| ---------- | --------: | -----: | -------: |
| Legitimate |      0.99 |   0.98 |     0.98 |
| Malicious  |      0.98 |   0.99 |     0.99 |

### Confusion Matrix

```text
                 Predicted
              Legitimate  Malicious

Legitimate       3904        73
Malicious          47      4064
```

Of the 8,088 test emails:

* 3,904 legitimate emails were classified correctly
* 4,064 malicious emails were classified correctly
* 73 legitimate emails were incorrectly flagged as malicious
* 47 malicious emails were incorrectly classified as legitimate

These results represent performance on a random test split of the public datasets used for training and should not be interpreted as guaranteed performance on real-world email.

## Datasets

The classifier currently uses email samples from four public datasets:

* **Enron**
* **SpamAssassin**
* **Nazario**
* **Nigerian Fraud**

After preprocessing and removing unusable or duplicate messages, the sources contain:

| Dataset        | Emails |
| -------------- | -----: |
| Enron          | 29,745 |
| SpamAssassin   |  5,809 |
| Nigerian Fraud |  3,319 |
| Nazario        |  1,564 |

### Labels by Dataset

| Dataset        | Legitimate | Malicious |
| -------------- | ---------: | --------: |
| Enron          |     15,791 |    13,954 |
| SpamAssassin   |      4,091 |     1,718 |
| Nazario        |          0 |     1,564 |
| Nigerian Fraud |          0 |     3,319 |

The different datasets use varying formats and labels. `prepare_data.py` standardizes them into a common format before training.

## How It Works

The current machine learning pipeline is:

```text
Raw Email Datasets
        |
        v
Data Inspection
        |
        v
Data Cleaning / Label Normalization
        |
        v
Subject + Email Body
        |
        v
TF-IDF Vectorization
        |
        v
Logistic Regression
        |
        v
Legitimate or Malicious
```

### TF-IDF

`TfidfVectorizer` converts email text into numerical features that can be processed by the machine learning model.

The current vectorizer:

* Converts text to lowercase
* Removes accent differences
* Examines individual words and two-word combinations
* Ignores extremely rare features
* Uses a maximum of 60,000 text features

### Logistic Regression

A Logistic Regression classifier is trained on the TF-IDF features.

The classifier uses balanced class weighting and outputs whether an email is predicted to be legitimate or malicious.

## Project Structure

```text
email_spam-phishing_classifier/
│
├── data/
│   ├── raw/
│   │   ├── Enron.csv
│   │   ├── Nazario.csv
│   │   ├── Nigerian_Fraud.csv
│   │   └── SpamAssasin.csv
│   │
│   └── processed/
│       └── emails.csv
│
├── models/
│   └── email_classifier.pkl
│
├── src/
│   ├── inspect_data.py
│   ├── prepare_data.py
│   └── train_classifier.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Scripts

### `inspect_data.py`

Inspects each raw CSV dataset and displays information including:

* Number of rows
* Column names
* Example records
* Label distribution

This was used to determine how the different public datasets were structured before combining them.

### `prepare_data.py`

Prepares the raw datasets for machine learning.

The script:

* Loads all CSV files from `data/raw`
* Detects subject, body, and label columns
* Combines the subject and email body
* Normalizes different label formats
* Converts labels to `0` or `1`
* Removes empty emails
* Removes duplicate emails
* Tracks the source dataset
* Combines all datasets
* Saves the resulting dataset as `data/processed/emails.csv`

The final processed dataset contains:

```text
text
label
source
```

### `train_classifier.py`

Trains and evaluates the machine learning classifier.

The script:

1. Loads the processed email dataset
2. Performs an 80/20 train-test split
3. Converts email text using TF-IDF
4. Trains a Logistic Regression classifier
5. Evaluates the classifier using:

   * Accuracy
   * Precision
   * Recall
   * F1 score
   * Confusion matrix
6. Saves the trained model

The trained model is stored at:

```text
models/email_classifier.pkl
```

## Installation

Clone the repository:

```bash
git clone https://github.com/MW562/email_spam-phishing_classifier.git
cd email_spam-phishing_classifier
```

Create a Python virtual environment:

### Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

### 1. Inspect the raw datasets

```bash
python src/inspect_data.py
```

### 2. Prepare the combined dataset

```bash
python src/prepare_data.py
```

This generates:

```text
data/processed/emails.csv
```

### 3. Train the classifier

```bash
python src/train_classifier.py
```

After training, the model is saved as:

```text
models/email_classifier.pkl
```

## Limitations

This is the first version of the classifier and currently analyzes only the **subject and body text** of an email.

A phishing detection system cannot reliably identify every attack using text alone. Legitimate security notifications and phishing emails can contain very similar wording.

The current model also uses a random train-test split from the same source datasets. As a result, the reported accuracy may be higher than performance on completely independent, real-world email.

The current classifier should therefore be considered an experimental machine learning model rather than a production security system.


## Technologies

* Python
* pandas
* NumPy
* scikit-learn
* TF-IDF
* Logistic Regression
* joblib

## Purpose

This project was created to explore the application of **machine learning, natural language processing, and cybersecurity concepts** to email threat detection.

Version 1 establishes the machine learning foundation. Future development will build a complete email analysis system around the trained classifier.
