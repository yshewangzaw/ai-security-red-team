from pathlib import Path
import io
import json

import requests
from PIL import Image
from torchvision import datasets


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "samples" / "extraction"
IMAGE_DIR = OUTPUT_DIR / "images"
OUTPUT_FILE = OUTPUT_DIR / "query_labels.json"

API_URL = "http://127.0.0.1:8000/predict"
NUM_QUERIES = 50


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    dataset = datasets.MNIST(
        root=DATA_DIR,
        train=False,
        download=False
    )

    records = []

    for index in range(NUM_QUERIES):
        image, _ = dataset[index]

        image_path = IMAGE_DIR / f"query_{index:03d}.png"
        image.save(image_path, format="PNG")

        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        response = requests.post(
            API_URL,
            files={
                "file": (
                    f"query_{index:03d}.png",
                    image_buffer,
                    "image/png"
                )
            },
            timeout=10
        )

        response.raise_for_status()

        result = response.json()
        predicted_label = result["prediction"]

        records.append({
            "query_id": index,
            "image": f"images/query_{index:03d}.png",
            "api_prediction": predicted_label
        })

        print(
            f"Query {index + 1}/{NUM_QUERIES}: "
            f"API prediction = {predicted_label}"
        )

    OUTPUT_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    print()
    print(f"Collected {len(records)} black-box predictions.")
    print(f"Images saved to: {IMAGE_DIR}")
    print(f"Labels saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()