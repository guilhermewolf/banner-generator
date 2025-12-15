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
    """Wrap text to fit within max_width"""
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

def calculate_dynamic_font_size(text, max_width, max_height, font_path, max_size=50, min_size=20):
    """
    Calculate optimal font size to fit text within given dimensions.
    Uses binary search for efficiency.
    """
    def get_text_dimensions(text, font_size):
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(text, font, max_width)
        if not lines:
            return 0, 0

        line_height = int(font.getbbox("A")[3] * 1.2)
        total_height = len(lines) * line_height
        return total_height, len(lines)

    # Binary search for optimal font size
    best_size = min_size
    low, high = min_size, max_size

    while low <= high:
        mid = (low + high) // 2
        height, num_lines = get_text_dimensions(text, mid)

        if height <= max_height:
            best_size = mid
            low = mid + 1  # Try larger
        else:
            high = mid - 1  # Try smaller

    return best_size

def generate_banner(background: Image.Image, text: str, footer: str = "@newsmedia") -> BytesIO:
    """
    Generate banner with OFFICIAL BannerBear specifications
    Based on: BANNERBEAR_OFFICIAL_SPEC.md
    """
    banner = background.copy()
    draw = ImageDraw.Draw(banner)

    # ========== OFFICIAL BANNERBEAR SPECIFICATIONS ==========
    # White content box (rectangle_background)
    BOX_X, BOX_Y = 119, 445  # Official: Y=445 (not 442!)
    BOX_WIDTH, BOX_HEIGHT = 763, 437
    BOX_END_X, BOX_END_Y = BOX_X + BOX_WIDTH, BOX_Y + BOX_HEIGHT  # (882, 882)

    # Accent line at bottom of white box (rectangle_border2)
    ACCENT_LINE_X, ACCENT_LINE_Y = 119, 879
    ACCENT_LINE_WIDTH, ACCENT_LINE_HEIGHT = 763, 14
    ACCENT_LINE_COLOR = "#4F86EC"  # Blue theme (original was #DE3F1C red)

    # Quote icon (svg_quote)
    QUOTE_SIZE = (59, 51)  # Official size from BannerBear
    QUOTE_X, QUOTE_Y = 160, 485

    # Text area (title element)
    TEXT_X, TEXT_Y = 161, 556
    TEXT_MAX_WIDTH = 659
    TEXT_MAX_HEIGHT = 280  # Approximate available height within white box

    # Footer bar (rectangle_border1) - extends to bottom of canvas
    FOOTER_BAR_START_Y = 1001  # Adjusted to extend to bottom
    FOOTER_COLOR = "#4F86EC"  # Blue theme (original was #DE3F1C red)

    # Instagram icon (svg_shape2) - repositioned for single-icon layout
    IG_ICON_SIZE = (26, 26)
    IG_ICON_X = 32  # Moved back to left edge
    IG_ICON_Y = 1030  # Instagram icon moved DOWN

    # Footer text (footer_1) - positioned close to icon, vertically aligned
    FOOTER_TEXT_X = 70  # Close to icon (32 + 26 + 12px gap)
    FOOTER_TEXT_Y = 1027  # Text moved UP

    # ========== LOAD ASSETS ==========
    quote_icon = Image.open(QUOTE_ICON_PATH).convert("RGBA").resize(QUOTE_SIZE)

    # Tint quote icon to blue (#4F86EC)
    quote_data = quote_icon.getdata()
    new_quote_data = []
    for item in quote_data:
        if item[0] < 50 and item[1] < 50 and item[2] < 50:  # If dark/black
            new_quote_data.append((79, 134, 236, item[3]))  # Blue with original alpha
        else:
            new_quote_data.append(item)
    quote_icon.putdata(new_quote_data)

    ig_icon = Image.open(IG_ICON_PATH).convert("RGBA").resize(IG_ICON_SIZE)

    # ========== DYNAMIC FONT SIZING ==========
    optimal_font_size = calculate_dynamic_font_size(
        text, TEXT_MAX_WIDTH, TEXT_MAX_HEIGHT, FONT_PATH, max_size=50, min_size=20
    )

    title_font = ImageFont.truetype(FONT_PATH, optimal_font_size)
    footer_font = ImageFont.truetype(FOOTER_FONT_PATH, 25)

    # ========== DRAW WHITE CONTENT BOX ==========
    draw.rectangle([(BOX_X, BOX_Y), (BOX_END_X, BOX_END_Y)], fill="white")

    # ========== DRAW ACCENT LINE (bottom of white box) ==========
    draw.rectangle([
        (ACCENT_LINE_X, ACCENT_LINE_Y),
        (ACCENT_LINE_X + ACCENT_LINE_WIDTH, ACCENT_LINE_Y + ACCENT_LINE_HEIGHT)
    ], fill=ACCENT_LINE_COLOR)

    # ========== DRAW QUOTE ICON ==========
    banner.paste(quote_icon, (QUOTE_X, QUOTE_Y), quote_icon)

    # ========== DRAW HEADLINE TEXT ==========
    lines = wrap_text(text, title_font, TEXT_MAX_WIDTH)
    line_height = int(title_font.getbbox("A")[3] * 1.2)
    text_y = TEXT_Y

    for line in lines:
        draw.text((TEXT_X, text_y), line, font=title_font, fill="black")
        text_y += line_height

    # ========== DRAW BLUE FOOTER BAR ==========
    # Footer extends from FOOTER_BAR_START_Y to bottom of canvas (Y=1080)
    draw.rectangle((0, FOOTER_BAR_START_Y, WIDTH, HEIGHT), fill=FOOTER_COLOR)

    # ========== DRAW INSTAGRAM ICON ==========
    banner.paste(ig_icon, (IG_ICON_X, IG_ICON_Y), ig_icon)

    # ========== DRAW FOOTER TEXT ==========
    draw.text((FOOTER_TEXT_X, FOOTER_TEXT_Y), footer, font=footer_font, fill="white")

    # ========== OUTPUT ==========
    output = BytesIO()
    banner.save(output, format="JPEG", quality=95)
    output.seek(0)
    return output
