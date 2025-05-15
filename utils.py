from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import httpx
import os

from dotenv import load_dotenv
load_dotenv()

# Asset paths from .env or defaults
FONT_PATH = os.getenv("FONT_PATH", "assets/Inter-Bold.ttf")
FOOTER_FONT_PATH = os.getenv("FOOTER_FONT_PATH", "assets/Inter-Regular.ttf")
QUOTE_ICON_PATH = os.getenv("QUOTE_ICON_PATH", "assets/quote.png")
IG_ICON_PATH = os.getenv("IG_ICON_PATH", "assets/instagram.png")

# Canvas constants
WIDTH, HEIGHT = 1080, 1080
CARD_MARGIN = 60
CARD_PADDING = 60
QUOTE_ICON_SIZE = 60
IG_ICON_SIZE = 28
BOTTOM_BAR_HEIGHT = 40

def download_image(url: str) -> Image.Image:
    response = httpx.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGB")

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

def generate_banner(background: Image.Image, text: str, footer: str = "@TheSignalDaily") -> BytesIO:
    bg = background.resize((WIDTH, HEIGHT))
    banner = bg.copy()
    draw = ImageDraw.Draw(banner)

    # Fonts
    title_font = ImageFont.truetype(FONT_PATH, 42)
    footer_font = ImageFont.truetype(FOOTER_FONT_PATH, 26)

    # Icons
    quote_icon = Image.open(QUOTE_ICON_PATH).convert("RGBA").resize((QUOTE_ICON_SIZE, QUOTE_ICON_SIZE))
    ig_icon = Image.open(IG_ICON_PATH).convert("RGBA").resize((IG_ICON_SIZE, IG_ICON_SIZE))

    # Text block
    max_text_width = WIDTH - 2 * (CARD_MARGIN + CARD_PADDING)
    lines = wrap_text(text, title_font, max_text_width)
    line_height = title_font.getbbox("A")[3] + 12
    text_block_height = len(lines) * line_height

    card_height = QUOTE_ICON_SIZE + 20 + text_block_height + CARD_PADDING * 2 + 20
    card_top = HEIGHT - card_height - BOTTOM_BAR_HEIGHT - 40
    card_bottom = card_top + card_height
    card_left = CARD_MARGIN
    card_right = WIDTH - CARD_MARGIN

    # White card
    draw.rectangle([(card_left, card_top), (card_right, card_bottom)], fill="white")

    # Quote icon
    banner.paste(
        quote_icon,
        (card_left + CARD_PADDING, card_top + CARD_PADDING),
        quote_icon
    )

    # Text
    text_x = card_left + CARD_PADDING
    text_y = card_top + CARD_PADDING + QUOTE_ICON_SIZE + 20
    for line in lines:
        draw.text((text_x, text_y), line, font=title_font, fill="black")
        text_y += line_height

    # Underline
    underline_y = card_bottom - CARD_PADDING // 2
    draw.line(
        [(card_left + CARD_PADDING, underline_y),
         (card_right - CARD_PADDING, underline_y)],
        fill=(0, 123, 255),
        width=4
    )

    # Blue bottom bar
    bar_top = HEIGHT - BOTTOM_BAR_HEIGHT
    draw.rectangle([(0, bar_top), (WIDTH, HEIGHT)], fill=(181, 215, 243))

    # Footer text + icon in the blue bar
    ig_y = bar_top + (BOTTOM_BAR_HEIGHT - IG_ICON_SIZE) // 2
    banner.paste(ig_icon, (CARD_MARGIN, ig_y), ig_icon)
    draw.text(
        (CARD_MARGIN + IG_ICON_SIZE + 10, ig_y + 2),
        footer,
        font=footer_font,
        fill="black"
    )

    # Output
    output = BytesIO()
    banner.save(output, format="JPEG", quality=95)
    output.seek(0)
    return output
