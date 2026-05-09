import random
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

DATA_FILE = DOCS_DIR / "behavior_events.csv"
RESULTS_FILE = DOCS_DIR / "behavior_scored.csv"


def generate_normal_events(n=60):
    events = []
    normal_files = [
        "employee_notes.txt",
        "access_logs.txt",
        "workstation_todo.txt",
        "q4_budget.csv",
        "event_logs.txt",
        "vpn_config.cfg",
    ]

    for _ in range(n):
        filename = random.choice(normal_files)
        events.append({
            "hour": random.randint(8, 18),
            "weekday": random.choice([0, 1, 2, 3, 4]),
            "event_type": random.choice(["open", "modify"]),
            "file_type": filename.split(".")[-1],
            "high_value": 1 if filename in ["q4_budget.csv", "vpn_config.cfg"] else 0,
            "files_touched": random.randint(1, 3),
            "label": "normal",
        })

    return events


def generate_suspicious_events(n=20):
    events = []
    suspicious_files = [
        "passwords.txt",
        "db_connection.txt",
        "confidential_chirps.csv",
        "deleted_chirps.csv",
    ]

    for _ in range(n):
        filename = random.choice(suspicious_files)
        events.append({
            "hour": random.choice([0, 1, 2, 3, 22, 23]),
            "weekday": random.randint(0, 6),
            "event_type": random.choice(["open", "modify", "delete", "create"]),
            "file_type": filename.split(".")[-1],
            "high_value": 1,
            "files_touched": random.randint(4, 8),
            "label": "suspicious",
        })

    return events


def build_dataset():
    events = generate_normal_events() + generate_suspicious_events()
    df = pd.DataFrame(events)
    df.to_csv(DATA_FILE, index=False)
    return df


def encode_features(df, encoder=None, fit_encoder=False):
    categorical_columns = ["event_type", "file_type"]
    numeric_columns = ["hour", "weekday", "high_value", "files_touched"]

    if fit_encoder:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        encoded = encoder.fit_transform(df[categorical_columns])
    else:
        encoded = encoder.transform(df[categorical_columns])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical_columns),
        index=df.index
    )

    numeric_df = df[numeric_columns].copy()

    final_df = pd.concat([numeric_df, encoded_df], axis=1)
    return final_df, encoder


def train_and_score(df):
    # Fit encoder on the full dataset so all possible event/file categories exist.
    X_all, encoder = encode_features(df, fit_encoder=True)

    normal_indexes = df[df["label"] == "normal"].index
    X_train = X_all.loc[normal_indexes]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.25,
        random_state=42
    )

    model.fit(X_train)

    predictions = model.predict(X_all)
    scores = model.decision_function(X_all)

    results = df.copy()
    results["prediction"] = predictions
    results["prediction_label"] = results["prediction"].map({
        1: "normal",
        -1: "anomalous"
    })
    results["anomaly_score"] = scores

    results.to_csv(RESULTS_FILE, index=False)
    return results


def print_results(results):
    print("\nAI Behavior Detection Results")
    print("=" * 80)

    print(results[
        [
            "hour",
            "weekday",
            "event_type",
            "file_type",
            "high_value",
            "files_touched",
            "label",
            "prediction_label",
            "anomaly_score",
        ]
    ].head(25).to_string(index=False))

    print("\nPrediction Counts")
    print(results["prediction_label"].value_counts())

    print(f"\nDataset saved to: {DATA_FILE}")
    print(f"Scored results saved to: {RESULTS_FILE}")


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    df = build_dataset()
    results = train_and_score(df)
    print_results(results)


if __name__ == "__main__":
    main()