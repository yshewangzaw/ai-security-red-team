from pathlib import Path
import json

import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader


BASE_DIR = Path(__file__).resolve().parents[2]

IMAGE_DIR = BASE_DIR / "samples" / "extraction_500" / "images"
LABEL_FILE = BASE_DIR / "samples" / "extraction_500" / "query_labels.json"
OUTPUT_FILE = BASE_DIR / "samples" / "extraction_500" / "substitute_model.pth"

DEVICE = torch.device("cpu")
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001


class ExtractionDataset(Dataset):
    def __init__(self, image_dir, label_file):
        self.image_dir = image_dir

        with open(label_file, "r", encoding="utf-8") as file:
            self.records = json.load(file)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        record = self.records[index]

        image_path = self.image_dir / f"query_{record['query_id']:03d}.png"

        image = Image.open(image_path).convert("L")
        image = image.resize((28, 28))

        image_tensor = torch.tensor(
            list(image.getdata()),
            dtype=torch.float32
        ).reshape(1, 28, 28) / 255.0

        label = torch.tensor(
            record["api_prediction"],
            dtype=torch.long
        )

        return image_tensor, label


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
    dataset = ExtractionDataset(
        IMAGE_DIR,
        LABEL_FILE
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    model = SubstituteModel().to(DEVICE)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE
    )

    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0.0

        for images, labels in loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        average_loss = total_loss / len(loader)

        print(
            f"Epoch {epoch + 1}/{EPOCHS} "
            f"- Loss: {average_loss:.4f}"
        )

    torch.save(
        model.state_dict(),
        OUTPUT_FILE
    )

    print()
    print("500-query substitute model training complete.")
    print(f"Training queries: {len(dataset)}")
    print(f"Model saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
