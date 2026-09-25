from pathlib import Path
import hashlib
import io

import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from model.model import MNISTModel


device = torch.device("cpu")

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.pth"
MODEL_HASH_PATH = BASE_DIR / "model" / "model.sha256"

MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_IMAGE_DIMENSION = 2048


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_model_integrity():
    expected_hash = MODEL_HASH_PATH.read_text(
        encoding="ascii"
    ).strip().lower()

    actual_hash = calculate_sha256(MODEL_PATH)

    if actual_hash != expected_hash:
        raise RuntimeError(
            "Model integrity check failed."
        )


verify_model_integrity()

model = MNISTModel().to(device)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device,
        weights_only=True
    )
)

model.eval()


transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor()
])


app = FastAPI(
    title="AI Security Red Team Demo",
    description="Local MNIST image classification API",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI API is running"
    }


@app.get("/model-info")
def model_info():
    return {
        "model": "MNISTModel",
        "dataset": "MNIST",
        "device": "CPU"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_data = await file.read()

    if len(image_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large."
        )

    if len(image_data) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        image = Image.open(
            io.BytesIO(image_data)
        )

        image.load()

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )

    if (
        image.width > MAX_IMAGE_DIMENSION
        or image.height > MAX_IMAGE_DIMENSION
    ):
        raise HTTPException(
            status_code=413,
            detail="Image dimensions are too large."
        )

    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(image_tensor)

    predicted_digit = output.argmax(dim=1).item()

    return {
        "filename": file.filename,
        "prediction": predicted_digit
    }
# from pathlib import Path

# import torch
# from fastapi import FastAPI, File, UploadFile
# from PIL import Image
# from torchvision import transforms

# from model.model import MNISTModel


# # Use CPU
# device = torch.device("cpu")


# # Find the trained model file
# BASE_DIR = Path(__file__).resolve().parent.parent
# MODEL_PATH = BASE_DIR / "model" / "model.pth"


# # Create the AI model
# model = MNISTModel().to(device)

# # Load the trained weights
# model.load_state_dict(
#     torch.load(MODEL_PATH, map_location=device)
# )

# # Put the model into prediction mode
# model.eval()


# # Image preprocessing
# transform = transforms.Compose([
#     transforms.Grayscale(),
#     transforms.Resize((28, 28)),
#     transforms.ToTensor()
# ])


# # Create the API
# app = FastAPI(
#     title="AI Security Red Team Demo",
#     description="Local MNIST image classification API",
#     version="1.0.0"
# )


# @app.get("/health")
# def health_check():
#     return {
#         "status": "ok",
#         "message": "AI API is running"
#     }


# @app.get("/model-info")
# def model_info():
#     return {
#         "model": "MNISTModel",
#         "dataset": "MNIST",
#         "device": "CPU"
#     }


# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):

#     # Read the uploaded image
#     image_data = await file.read()

#     # Convert the uploaded file into an image
#     image = Image.open(
#         __import__("io").BytesIO(image_data)
#     )

#     # Prepare the image for the model
#     image_tensor = transform(image)

#     # Add a batch dimension
#     image_tensor = image_tensor.unsqueeze(0)

#     # Make the prediction
#     with torch.no_grad():
#         output = model(image_tensor)

#     # Find the digit with the highest score
#     predicted_digit = output.argmax(dim=1).item()

#     return {
#         "filename": file.filename,
#         "prediction": predicted_digit
#     }