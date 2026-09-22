import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from model import MNISTModel


# Use CPU for this project
device = torch.device("cpu")


# Convert MNIST images into PyTorch tensors
transform = transforms.ToTensor()


# Download and load the MNIST training dataset
train_dataset = datasets.MNIST(
    root="../data",
    train=True,
    download=True,
    transform=transform
)


# Give the model small groups of images at a time
train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True
)


# Create our AI model
model = MNISTModel().to(device)


# Loss function
loss_function = torch.nn.CrossEntropyLoss()


# Optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# Train the model
epochs = 3

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        # Clear old gradients
        optimizer.zero_grad()

        # Ask the model to make predictions
        predictions = model(images)

        # Calculate how wrong the predictions were
        loss = loss_function(predictions, labels)

        # Calculate gradients
        loss.backward()

        # Update model weights
        optimizer.step()

        total_loss += loss.item()

    average_loss = total_loss / len(train_loader)

    print(
        f"Epoch {epoch + 1}/{epochs}, "
        f"Loss: {average_loss:.4f}"
    )


# Save the trained model
torch.save(
    model.state_dict(),
    "model.pth"
)

print("Training complete.")
print("Model saved to model.pth")