from pathlib import Path


file_path = Path("invalid_test.txt")

file_path.write_text(
    "This is not an image."
)

print(f"Created: {file_path}")