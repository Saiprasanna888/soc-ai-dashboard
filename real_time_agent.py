import os
import time
import shutil
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import smtplib
from email.mime.text import MIMEText

# ---------------------------
# Config
WATCH_FOLDER = "alerts_folder"
MODEL_FILE = "triage_model.joblib"
FROM_EMAIL = "sololeveling6868@gmail.com"
FROM_PASSWORD = "wnit gcdo wdax bonm"
TO_EMAIL = "deepchat6996@gmail.com"

# ---------------------------
# Email function
def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.send_message(msg)
        print(f"[INFO] Email sent successfully to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

# ---------------------------
# Load and preprocess dataset
def load_and_preprocess(file):
    print("[INFO] Loading and preprocessing dataset...")
    df = pd.read_csv(file)

    # Maps
    priority_map = {
        '1 - Critical': 1,
        '2 - High': 2,
        '3 - Moderate': 3,
        '4 - Low': 4
    }
    urgency_map = {
        '1 - High': 1,
        '2 - Medium': 2,
        '3 - Low': 3
    }

    df['priority_num'] = df['priority'].map(priority_map)
    df['urgency_num'] = df['urgency'].map(urgency_map)

    # Label: Critical/High OR High urgency
    df['label'] = df.apply(
        lambda row: 1 if (row['priority_num'] in [1, 2]) or (row['urgency_num'] == 1) else 0,
        axis=1
    )

    df = df.dropna(subset=['priority_num', 'urgency_num', 'label'])
    print(f"[INFO] Dataset loaded with {len(df)} rows after preprocessing")
    return df

# ---------------------------
# Train model (if needed)
def train_and_save_model(df):
    print("[INFO] Training the ML model...")
    features = ['priority_num', 'urgency_num']
    X = df[features]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("[INFO] Classification report for model evaluation:\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_FILE)
    print(f"[INFO] Model saved to {MODEL_FILE}")
    return model

# ---------------------------
# Load model
def load_model():
    try:
        model = joblib.load(MODEL_FILE)
        print(f"[INFO] Loaded model from {MODEL_FILE}")
        return model
    except FileNotFoundError:
        print("[WARN] Model file not found – please run training first.")
        return None

# ---------------------------
# Predict alerts and notify
def predict_and_notify(df, model):
    print("[INFO] Running predictions on dataset...")
    feature_cols = ['priority_num', 'urgency_num']
    data_to_predict = df.dropna(subset=feature_cols).copy()

    if data_to_predict.empty:
        print("[WARN] No data to predict after preprocessing.")
        return

    predictions = model.predict(data_to_predict[feature_cols])
    data_to_predict['ml_triage_label'] = predictions

    urgent_alerts = data_to_predict[data_to_predict['ml_triage_label'] == 1]

    if urgent_alerts.empty:
        print("[INFO] No high priority alerts predicted by the model.")
        return

    urgent_alerts = urgent_alerts.head(5)

    print("\n" + "="*40)
    print("*** ML PREDICTED HIGH PRIORITY ALERTS ***")
    print("="*40 + "\n")

    for _, alert in urgent_alerts.iterrows():
        msg = (
            f"Incident: {alert['number']}\n"
            f"Priority: {alert['priority']}\n"
            f"Urgency: {alert['urgency']}\n"
            f"State: {alert['incident_state']}\n"
            f"Opened At: {alert['opened_at']}\n"
            f"Assigned To: {alert.get('assigned_to', 'N/A')}\n"
        )
        print(f"ALERT:\n{msg}\n{'-'*40}\n")

        subject = f"URGENT: High Priority Incident {alert['number']}"
        send_email(subject, msg, TO_EMAIL)

# ---------------------------
# Main real-time loop
def main():
    print("[INFO] Starting SOC AI Agent real-time monitor...")
    print(f"[INFO] Watching folder: {WATCH_FOLDER}")

    model = load_model()
    if not model:
        print("[ERROR] No model available. Exiting.")
        return

    seen_files = set()

    while True:
        for file in os.listdir(WATCH_FOLDER):
            if file.endswith(".csv") and file not in seen_files:
                file_path = os.path.join(WATCH_FOLDER, file)
                temp_path = file_path + ".tmp"

                try:
                    print(f"\n[INFO] New alert file detected: {file_path}")
                    # Make a safe copy to avoid file lock issues
                    shutil.copy(file_path, temp_path)
                    df = load_and_preprocess(temp_path)
                    predict_and_notify(df, model)
                    seen_files.add(file)
                    os.remove(temp_path)  # clean up
                except Exception as e:
                    print(f"[ERROR] Could not process file {file_path}: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
