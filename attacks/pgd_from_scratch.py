import torch
from torchvision import datasets, transforms
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from model.model import MNISTModel


device = torch.device("cpu")

model = MNISTModel().to(device)

model.load_state_dict(
    torch.load("model/model.pth", map_location=device)
)

model.eval()


transform = transforms.ToTensor()

dataset = datasets.MNIST(
    root="data",
    train=False,
    download=False,
    transform=transform
)

image, true_label = dataset[0]

image = image.unsqueeze(0).to(device)

true_label = torch.tensor(
    [true_label]
).to(device)

print("True label:", true_label.item())

output = model(image)

original_prediction = output.argmax(
    dim=1
).item()

print("Original prediction:", original_prediction)
loss_function = torch.nn.CrossEntropyLoss()
epsilon = 0.1
alpha = 0.01
steps = 10
adversarial_image = image.clone().detach()
for step in range(steps):
    adversarial_image.requires_grad = True

    output = model(adversarial_image)

    loss = loss_function(
        output,
        true_label
    )

    model.zero_grad()

    loss.backward()

    gradient = adversarial_image.grad

    with torch.no_grad():
        adversarial_image = (
            adversarial_image
            + alpha * gradient.sign()
        )

        perturbation = adversarial_image - image

        perturbation = torch.clamp(
            perturbation,
            -epsilon,
            epsilon
        )

        adversarial_image = image + perturbation

        adversarial_image = torch.clamp(
            adversarial_image,
            0,
            1
        )
with torch.no_grad():
    adversarial_output = model(adversarial_image)

adversarial_prediction = adversarial_output.argmax(
    dim=1
).item()

print("Adversarial prediction:", adversarial_prediction)
output_path = Path(
    "samples/adversarial/pgd_from_scratch_7_to_3.png"
)

adversarial_pixels = (
    adversarial_image.squeeze()
    .detach()
    .numpy()
    * 255
).astype("uint8")

Image.fromarray(adversarial_pixels).save(output_path)

print("Adversarial image saved to:", output_path)