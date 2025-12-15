# Banner Generator

A Python-based banner generator that replicates BannerBear's Instagram post template functionality. Generates professional social media posts with dynamic text sizing and customizable branding.

## Features

- ✅ **Dynamic Text Sizing** - Automatically scales text to fit within content box (20pt-50pt range)
- ✅ **BannerBear Template Accurate** - Pixel-perfect positioning based on official BannerBear specifications
- ✅ **Blue Theme** - Customized for tech/camera brand posts (#4F86EC)
- ✅ **Instagram Optimized** - 1080x1080px square format
- ✅ **Google Drive Integration** - Automatic upload and public URL generation
- ✅ **FastAPI REST API** - Simple HTTP endpoint for banner generation

## Quick Start

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file:

```env
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
```

Add your Google service account credentials to `service_account.json`.

### Run the Server

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production (Docker)
docker build -t banner-generator .
docker run -p 8000:8000 banner-generator
```

## Usage

### API Endpoint

```bash
POST http://localhost:8000/generate-banner

# Form data:
{
  "image_url": "https://example.com/background.jpg",
  "text": "Your headline text here...",
  "footer": "@YourHandle"
}

# Response:
{
  "image_url": "https://drive.google.com/uc?id=..."
}
```

### Python Function

```python
from utils import download_image, generate_banner

# Generate banner
bg = download_image("https://example.com/background.jpg")
banner_io = generate_banner(
    bg,
    text="Your headline here...",
    footer="@YourHandle"
)

# Save to file
with open("output.jpg", "wb") as f:
    f.write(banner_io.read())
```

## Background Image Guidelines

For best results, follow these composition guidelines when creating/selecting background images:

### Safe Zones (1080x1080px canvas)

```
┌─────────────────────────────────┐
│ TOP ZONE (Y: 0-445)            │  ← Main subject HERE
│ ✅ Fully visible                │     (Product, camera, portrait)
│                                 │
├─────────────────────────────────┤
│ WHITE BOX OVERLAY              │
│ (X: 119-882, Y: 445-893)       │  ← AVOID important details
│ ⚠️  Will be covered             │     (Use blur/gradient)
│                                 │
├─────────────────────────────────┤
│ FOOTER BAR (Y: 1001-1080)      │  ← AVOID important details
│ ⚠️  Completely covered          │     (Blue footer bar)
└─────────────────────────────────┘
```

### AI Image Generation Prompts

**For Product/Camera Posts:**
```
"Professional DSLR camera on clean background, camera positioned
in upper third of frame (top 445px), lower portion transitions
to soft gradient or blur, 1:1 square aspect ratio, studio lighting,
product photography, sharp focus on camera"
```

**For General Use:**
```
"[Subject] in upper section of frame, top 445 pixels, middle and
lower area soft gradient fade, 1:1 square format, professional
photography, clean composition"
```

**Key instruction:** Place main subject in top 445 pixels. Middle section (445-893px) should be clean gradient or blur.

## Template Specifications

Based on official BannerBear template with customizations:

| Element | Position | Size | Color |
|---------|----------|------|-------|
| Canvas | - | 1080x1080px | - |
| White Content Box | (119, 445) | 763x437px | #FFFFFF |
| Blue Accent Line | (119, 879) | 763x14px | #4F86EC |
| Quote Icon | (160, 485) | 59x51px | #4F86EC |
| Main Text | (161, 556) | 659px max width | #000000 |
| Footer Bar | (0, 1001) | 1080x79px | #4F86EC |
| Instagram Icon | (32, 1030) | 26x26px | #FFFFFF |
| Footer Text | (70, 1027) | - | #FFFFFF |

See `docs/BANNERBEAR_OFFICIAL_SPEC.md` for complete specifications.

## Project Structure

```
banner-generator/
├── main.py                    # FastAPI server
├── utils.py                   # Core banner generation logic
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .env                       # Environment variables (create this)
├── service_account.json       # Google credentials (create this)
├── assets/                    # Fonts and icons
│   ├── Chivo-Bold.ttf
│   ├── Chivo-Regular.ttf
│   ├── instagram.png
│   └── quote.png
├── docs/                      # Documentation
│   ├── BANNERBEAR_OFFICIAL_SPEC.md    # Official template spec
│   ├── TEMPLATE_SPECIFICATION.md      # Original analysis
│   ├── COMPARISON_REPORT.md           # Comparison report
│   └── FINAL_IMPLEMENTATION_REPORT.md # Implementation summary
├── reference/                 # Reference materials
│   ├── bannerbear/           # BannerBear screenshots
│   └── example.png           # Reference output
└── tests/                    # Test scripts
    ├── test.py               # API test
    └── generate_test.py      # Direct function test
```

## Key Features Explained

### Dynamic Text Sizing

The banner generator automatically adjusts font size (20pt-50pt) to ensure text fits within the white content box:

- **Short text** → Uses maximum 50pt font
- **Medium text** → Scales to optimal size
- **Long text** → Reduces to 20pt minimum
- **White box never resizes** → Only text adapts

This replicates BannerBear's "Text Fit: ON" feature using a binary search algorithm.

### Theme Customization

Original BannerBear template uses RED theme (#DE3F1C). This version uses:
- **Blue theme** (#4F86EC) for tech/camera brands
- Single Instagram icon (original has 3 social icons)
- Simplified footer (removed website URL)

## Testing

```bash
# Run API test
cd tests
python test.py

# Run direct function test
python generate_test.py
```

## Documentation

- **`docs/BANNERBEAR_OFFICIAL_SPEC.md`** - Official BannerBear template specifications
- **`docs/FINAL_IMPLEMENTATION_REPORT.md`** - Complete implementation details
- **`reference/bannerbear/`** - Original BannerBear editor screenshots

## Dependencies

- Python 3.11+
- Pillow (image processing)
- FastAPI (REST API)
- httpx (HTTP client)
- Google API Client (Drive integration)

See `requirements.txt` for complete list.

## License

Proprietary - For internal use only.

## Credits

Template based on BannerBear's news article template with customizations for tech/camera brand social media posts.
