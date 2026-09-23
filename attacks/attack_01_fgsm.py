import torch

from PIL import Image
from torchvision import datasets, transforms
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

import torch
from model.model import MNISTModel


# -----------------------------
# Settings
# -----------------------------

device = torch.device("cpu")
epsilon = 0.1

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.pth"
OUTPUT_DIR = BASE_DIR / "samples" / "adversarial"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Load model
# -----------------------------

model = MNISTModel().to(device)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.eval()


# -----------------------------
# Load one MNIST image
# -----------------------------

transform = transforms.ToTensor()

dataset = datasets.MNIST(
    root=BASE_DIR / "data",
    train=False,
    download=False,
    transform=transform
)

image, true_label = dataset[0]

image = image.unsqueeze(0).to(device)
true_label = torch.tensor([true_label]).to(device)

image.requires_grad = True


# -----------------------------
# Normal prediction
# -----------------------------

output = model(image)

original_prediction = output.argmax(dim=1).item()

print("True label:", true_label.item())
print("Original prediction:", original_prediction)


# -----------------------------
# Calculate loss and gradient
# -----------------------------

loss_function = torch.nn.CrossEntropyLoss()

loss = loss_function(output, true_label)

model.zero_grad()

loss.backward()

gradient = image.grad


# -----------------------------
# Create FGSM adversarial image
# -----------------------------

perturbation = epsilon * gradient.sign()

adversarial_image = image + perturbation

adversarial_image = torch.clamp(
    adversarial_image,
    0,
    1
)


# -----------------------------
# Test adversarial image
# -----------------------------

with torch.no_grad():

    adversarial_output = model(adversarial_image)

    adversarial_prediction = (
        adversarial_output.argmax(dim=1).item()
    )


print("Adversarial prediction:", adversarial_prediction)

if adversarial_prediction != true_label.item():
    print("FGSM attack SUCCESS")
else:
    print("FGSM attack FAILED")


# -----------------------------
# Save images
# -----------------------------

original_pixels = (
    image.squeeze().detach().cpu().numpy() * 255
).astype("uint8")

adversarial_pixels = (
    adversarial_image.squeeze().detach().cpu().numpy() * 255
).astype("uint8")


Image.fromarray(original_pixels).save(
    OUTPUT_DIR / "fgsm_original.png"
)

Image.fromarray(adversarial_pixels).save(
    OUTPUT_DIR / "fgsm_adversarial.png"
)

print("Saved original image.")
print("Saved adversarial image.")