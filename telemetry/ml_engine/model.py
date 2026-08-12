import torch
import torch.nn as nn

class LSTMAnomalyDetector(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=64, num_layers=2):
        super(LSTMAnomalyDetector, self).__init__()
        # Encoder
        self.encoder = nn.LSTM(
            input_size=input_dim, 
            hidden_size=hidden_dim, 
            num_layers=num_layers, 
            batch_first=True
        )
        # Decoder
        self.decoder = nn.LSTM(
            input_size=hidden_dim, 
            hidden_size=input_dim, 
            num_layers=num_layers, 
            batch_first=True
        )

    def forward(self, x):
        encoded, (hn, cn) = self.encoder(x)
        decoded, _ = self.decoder(encoded)
        return decoded

def compute_anomaly_score(model, input_tensor, threshold=0.15):
    model.eval()
    with torch.no_grad():
        reconstruction = model(input_tensor)
        loss = torch.mean((input_tensor - reconstruction) ** 2, dim=[1, 2])
        is_anomaly = loss > threshold
    return loss.item(), is_anomaly.item()
