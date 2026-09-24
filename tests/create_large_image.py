from PIL import Image
import numpy as np
import os

pixels = np.random.randint(
    0, 256, (3000, 3000), dtype=np.uint8
)

image = Image.fromarray(pixels, "L")

image.save(
    "large_test.png",
    format="PNG",
    compress_level=0
)

size = os.path.getsize("large_test.png")

print(f"Created: {size} bytes")# from PIL import Image

# image = Image.new("L", (3000, 3000), 255)

# image.save(
#     "large_test.png",
#     format="PNG"
# )

# print("Large image created.")