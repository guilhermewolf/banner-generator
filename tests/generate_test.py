from utils import download_image, generate_banner
from PIL import Image

# Test 1: Space background (current)
print("\n=== Test 1: Space Background ===")
image_url = "https://wallpapercave.com/wp/wp3788129.jpg"
text = "Sigma's new BF camera features a minimalist design, built-in SSD, and L-Mount compatibility. It offers a redesigned interface, 24.6-megapixel resolution, 6K video capture, and hybrid autofocus. Priced at $1,999, shipping in April 2025."
footer = "@TheSignalDaily"

print("Downloading background image...")
bg = download_image(image_url)

print("Generating banner...")
banner_io = generate_banner(bg, text, footer)

print("Saving to output.png...")
with open("output.png", "wb") as f:
    f.write(banner_io.read())

print("✅ Banner generated successfully! Check output.png")

# Test 2: Camera background
print("\n=== Test 2: Camera Background ===")
image_url2 = "https://images.pexels.com/photos/51383/photo-camera-subject-photographer-51383.jpeg"
text2 = "Sigma's new BF camera features a minimalist design, built-in SSD, and L-Mount compatibility. It offers a redesigned interface, 24.6-megapixel resolution, 6K video capture, and hybrid autofocus. Priced at $1,999, shipping in April 2025."
footer2 = "@TheSigmaGalaxy"

print("Downloading camera background...")
bg2 = download_image(image_url2)

print("Generating banner...")
banner_io2 = generate_banner(bg2, text2, footer2)

print("Saving to output_camera.png...")
with open("output_camera.png", "wb") as f:
    f.write(banner_io2.read())

print("✅ Camera banner generated successfully! Check output_camera.png")
