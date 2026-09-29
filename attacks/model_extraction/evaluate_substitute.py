from pathlib import Path
import io
import json

import requests
import torch
import torch.nn as nn
from PIL import Image
from torchvision import datasets


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
MODEL_PATH = BASE_DIR / "samples" / "extraction" / "substitute_model.pth"
TRAINING_LABELS = BASE_DIR / "samples" / "extraction" / "query_labels.json"

API_URL = "http://127.0.0.1:8000/predict"

DEVICE = torch.device("cpu")


class SubstituteModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.network(x)


def main():
    model = SubstituteModel().to(DEVICE)

    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location=DEVICE,
            weights_only=True
        )
    )

    model.eval()

    with open(TRAINING_LABELS, "r", encoding="utf-8") as file:
        training_records = json.load(file)

    training_ids = {
        record["query_id"]
        for record in training_records
    }

    dataset = datasets.MNIST(
        root=DATA_DIR,
        train=False,
        download=False
    )

    total = 0
    matches = 0

    print("Testing substitute model on new queries...")
    print()

    for index in range(50, 100):
        if index in training_ids:
            continue

        image, _ = dataset[index]

        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        response = requests.post(
            API_URL,
            files={
                "file": (
                    f"evaluation_{index:03d}.png",
                    image_buffer,
                    "image/png"
                )
            },
            timeout=10
        )

        response.raise_for_status()

        api_prediction = response.json()["prediction"]

        image_tensor = torch.tensor(
            list(image.getdata()),
            dtype=torch.float32
        ).reshape(1, 1, 28, 28) / 255.0

        with torch.no_grad():
            output = model(image_tensor)
            substitute_prediction = output.argmax(dim=1).item()

        match = api_prediction == substitute_prediction

        if match:
            matches += 1

        total += 1

        print(
            f"Query {index}: "
            f"API={api_prediction}, "
            f"Substitute={substitute_prediction}, "
            f"Match={match}"
        )

    fidelity = (matches / total) * 100

    print()
    print("Extraction fidelity evaluation")
    print(f"Evaluation queries: {total}")
    print(f"Matching predictions: {matches}")
    print(f"Fidelity: {fidelity:.2f}%")


if __name__ == "__main__":
    main()
