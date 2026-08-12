from fastapi import FastAPI
from pydantic import BaseModel
import torch
from model import LSTMAnomalyDetector, compute_anomaly_score

app = FastAPI(title="Infrastructure Anomaly Inference API")

model = LSTMAnomalyDetector()
# Load pre-trained model weights if available: model.load_state_dict(torch.load("model.pth"))

class MetricWindow(BaseModel):
    node_id: str
    sequence: list[list[float]]  # Expected shape: [seq_len, num_features] e.g., [10, 2]

@app.post("/predict")
def predict_anomaly(data: MetricWindow):
    tensor_input = torch.tensor([data.sequence], dtype=torch.float32)
    score, is_anomaly = compute_anomaly_score(model, tensor_input)
    
    return {
        "node_id": data.node_id,
        "anomaly_score": score,
        "predicted_failure_risk": is_anomaly,
        "recommended_action": "Trigger Horizontal Pod Autoscaler / Cordon Node" if is_anomaly else "Nominal"
    }
