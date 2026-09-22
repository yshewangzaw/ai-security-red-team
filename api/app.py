from pathlib import Path

import torch
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from torchvision import transforms

from model.model import MNISTModel


# Use CPU
device = torch.device("cpu")


# Find the trained model file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.pth"


# Create the AI model
model = MNISTModel().to(device)

# Load the trained weights
model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

# Put the model into prediction mode
model.eval()


# Image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor()
])


# Create the API
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

    # Read the uploaded image
    image_data = await file.read()

    # Convert the uploaded file into an image
    image = Image.open(
        __import__("io").BytesIO(image_data)
    )

    # Prepare the image for the model
    image_tensor = transform(image)

    # Add a batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Make the prediction
    with torch.no_grad():
        output = model(image_tensor)

    # Find the digit with the highest score
    predicted_digit = output.argmax(dim=1).item()

    return {
        "filename": file.filename,
        "prediction": predicted_digit
    }