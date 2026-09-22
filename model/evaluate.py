import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from model import MNISTModel


# Use CPU
device = torch.device("cpu")


# Convert images to tensors
transform = transforms.ToTensor()


# Load the MNIST test dataset
test_dataset = datasets.MNIST(
    root="../data",
    train=False,
    download=True,
    transform=transform
)


# Load test images in batches
test_loader = DataLoader(
    test_dataset,
    batch_size=64,
    shuffle=False
)


# Create the same model architecture
model = MNISTModel().to(device)


# Load the trained weights
model.load_state_dict(
    torch.load("model.pth", map_location=device)
)


# Put the model into evaluation mode
model.eval()


# Count correct predictions
correct = 0
total = 0


# Disable gradient calculations during normal evaluation
with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)
        labels = labels.to(device)

        # Make predictions
        predictions = model(images)

        # Find the class with the highest score
        predicted_labels = predictions.argmax(dim=1)

        # Count correct predictions
        correct += (predicted_labels == labels).sum().item()

        # Count total images
        total += labels.size(0)


# Calculate accuracy
accuracy = correct / total


print(f"Correct predictions: {correct}")
print(f"Total test images: {total}")
print(f"Baseline accuracy: {accuracy * 100:.2f}%")


