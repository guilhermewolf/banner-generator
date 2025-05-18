from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Paths from .env or fallback
FONT_PATH = os.getenv("FONT_PATH", "assets/Chivo-Bold.ttf")
FOOTER_FONT_PATH = os.getenv("FOOTER_FONT_PATH", "assets/Chivo-Regular.ttf")
QUOTE_ICON_PATH = os.getenv("QUOTE_ICON_PATH", "assets/quote.png")
IG_ICON_PATH = os.getenv("IG_ICON_PATH", "assets/instagram.png")

# Canvas dimensions
WIDTH, HEIGHT = 1080, 1080

def download_image(url: str) -> Image.Image:
    response = httpx.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGB").resize((WIDTH, HEIGHT))

def wrap_text(text, font, max_width):
    words = text.split()
    lines, current_line = [], ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)
    return lines

def generate_banner(background: Image.Image, text: str, footer: str = "@newsmedia") -> BytesIO:
    banner = background.copy()
    draw = ImageDraw.Draw(banner)

    # Load assets
    quote_icon = Image.open(QUOTE_ICON_PATH).convert("RGBA").resize((59, 51))
    ig_icon = Image.open(IG_ICON_PATH).convert("RGBA").resize((26, 26))

    # Load fonts
    title_font = ImageFont.truetype(FONT_PATH, 50)
    footer_font = ImageFont.truetype(FOOTER_FONT_PATH, 25)

    # Draw white content box
    draw.rectangle([(119, 442), (119 + 763, 442 + 437)], fill="white")

    # Draw quote icon
    banner.paste(quote_icon, (160, 485), quote_icon)

    # Draw headline text
    max_text_width = 659
    lines = wrap_text(text, title_font, max_text_width)
    line_height = int(title_font.getbbox("A")[3] * 1.2)
    text_y = 556
    for line in lines:
        draw.text((161, text_y), line, font=title_font, fill="black")
        text_y += line_height

    #draw.rectangle([(bar_x, bar_y), (bar_x + bar_width, HEIGHT)], fill="#DE3F1C")
    #draw.rectangle((0, 1016, 1080, 1080), fill="blue", outline="black")
    draw.rectangle((0, 1016, 1080, 1080), fill="#4F86EC")

    # Paste Instagram icon in red bar
    banner.paste(ig_icon, (32, 1027), ig_icon)

    # Draw footer text
    draw.text((70, 1030), footer, font=footer_font, fill="white")

    # Output image to memory
    output = BytesIO()
    banner.save(output, format="JPEG", quality=95)
    output.seek(0)
    return output
