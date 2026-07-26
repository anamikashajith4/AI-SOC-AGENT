import joblib
import pandas as pd
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Load the live-compatible model (trained only on fields our simulator actually produces)
model = joblib.load(os.path.join(MODEL_DIR, 'isolation_forest_live.pkl'))
encoders = joblib.load(os.path.join(MODEL_DIR, 'encoders.pkl'))
live_feature_columns = joblib.load(os.path.join(MODEL_DIR, 'live_feature_columns.pkl'))


def safe_encode(column_name, value):
    """Encode a text value using the saved encoder. Falls back to 0 if it's an unseen category."""
    le = encoders[column_name]
    if value in le.classes_:
        return int(le.transform([value])[0])
    return 0


def build_feature_vector(log):
    """Turn a simulated log entry into the 7-feature row the live model expects."""
    row = {
        'protocol_type': safe_encode('protocol_type', log['protocol_type']),
        'service': safe_encode('service', log['service']),
        'flag': safe_encode('flag', log['flag']),
        'src_bytes': log['src_bytes'],
        'dst_bytes': log['dst_bytes'],
        'num_failed_logins': log['num_failed_logins'],
        'serror_rate': log['serror_rate'],
    }
    return pd.DataFrame([row])[live_feature_columns]


def detect(log):
    """Run the live-compatible Isolation Forest on a single log entry."""
    features = build_feature_vector(log)
    prediction = model.predict(features)[0]
    score = model.decision_function(features)[0]

    return {
        "ai_flagged": bool(prediction == -1),
        "anomaly_score": round(float(score), 4)
    }