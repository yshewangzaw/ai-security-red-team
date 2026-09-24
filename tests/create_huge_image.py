from PIL import Image


width = 10000
height = 10000

image = Image.new("L", (width, height), 128)

image.save(
    "huge_dimensions.png"
)

print(f"Created image: {width} x {height}")