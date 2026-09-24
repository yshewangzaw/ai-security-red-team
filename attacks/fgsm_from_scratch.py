from pathlib import Path
from PIL import Image
import torch
from torchvision import datasets, transforms
import sys
from pathlib import Path

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

image.requires_grad = True
true_label = torch.tensor([true_label]).to(device)
output = model(image)

original_prediction = output.argmax(dim=1).item()

print("True label:", true_label.item())
print("Original prediction:", original_prediction)
loss_function = torch.nn.CrossEntropyLoss()

loss = loss_function(
    output,
    true_label
)
loss.backward()
signed_gradient = image.grad.sign()
epsilon = 0.1

perturbation = epsilon * signed_gradient


print("Perturbation minimum:", perturbation.min().item())
print("Perturbation maximum:", perturbation.max().item())

print("Signed gradient minimum:", signed_gradient.min().item())
print("Signed gradient maximum:", signed_gradient.max().item())
print("Loss:", loss.item())
print("Gradient shape:", image.grad.shape)
print("Gradient minimum:", image.grad.min().item())
print("Gradient maximum:", image.grad.max().item())
adversarial_image = image + perturbation

adversarial_image = torch.clamp(
    adversarial_image,
    0,
    1
)

print(
    "Final adversarial image minimum:",
    adversarial_image.min().item()
)

print(
    "Final adversarial image maximum:",
    adversarial_image.max().item()
)
adversarial_output = model(adversarial_image)

adversarial_prediction = adversarial_output.argmax(
    dim=1
).item()

print(
    "Adversarial prediction:",
    adversarial_prediction
)
output_path = Path(
    "samples/adversarial/fgsm_from_scratch_7_to_3.png"
)

adversarial_pixels = (
    adversarial_image.squeeze()
    .detach()
    .numpy()
    * 255
).astype("uint8")

Image.fromarray(adversarial_pixels).save(output_path)

print("Adversarial image saved to:", output_path)