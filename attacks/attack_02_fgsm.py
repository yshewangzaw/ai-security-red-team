import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)
import torch
from torchvision import datasets, transforms
from PIL import Image



from model.model import MNISTModel
# Load MNIST test dataset
dataset = datasets.MNIST(
    root="data",
    train=False,
    download=False,
    transform=transforms.ToTensor()
)
# Load trained model
model = MNISTModel()

model.load_state_dict(
    torch.load(
        "model/model.pth",
        map_location="cpu"
    )
)

model.eval()
# Prepare image for the model
image, true_label = dataset[1]
image_input = image.unsqueeze(0)
image_input.requires_grad = True

# Make normal prediction
output = model(image_input)

prediction = output.argmax(dim=1).item()

print("True label:", true_label)
print("Model prediction:", prediction)
loss_function = torch.nn.CrossEntropyLoss()

loss = loss_function(
    output,
    torch.tensor([true_label])
)

print("Loss:", loss.item())
model.zero_grad()

loss.backward()

gradient = image_input.grad

print("Gradient shape:", gradient.shape)
print("Gradient minimum:", gradient.min().item())
print("Gradient maximum:", gradient.max().item())
signed_gradient = gradient.sign()

print("Signed gradient minimum:", signed_gradient.min().item())
print("Signed gradient maximum:", signed_gradient.max().item())
epsilon = 0.1

perturbation = epsilon * signed_gradient

print("Perturbation minimum:", perturbation.min().item())
print("Perturbation maximum:", perturbation.max().item())
adversarial_image = image_input + perturbation

adversarial_image = torch.clamp(
    adversarial_image,
    0,
    1
)
adversarial_output = model(adversarial_image)

adversarial_prediction = (
    adversarial_output.argmax(dim=1).item()
)
adversarial_loss = loss_function(
    adversarial_output,
    torch.tensor([true_label])
)

print(
    "Adversarial loss:",
    adversarial_loss.item()
)

print(
    "Adversarial prediction:",
    adversarial_prediction
)
print(
    "Adversarial image minimum:",
    adversarial_image.min().item()
)

print(
    "Adversarial image maximum:",
    adversarial_image.max().item()
)
# Save adversarial image

adversarial_pixels = (
    adversarial_image.squeeze().detach().numpy() * 255
).astype("uint8")

Image.fromarray(adversarial_pixels).save(
    "samples/adversarial/understand_fgsm_adversarial.png"
)

print("Adversarial image saved.")
#

# Save the original image
pixels = (
    image.squeeze().numpy() * 255
).astype("uint8")

Image.fromarray(pixels).save(
    "samples/original/understand_fgsm_original.png"
)

print("Original image saved.")