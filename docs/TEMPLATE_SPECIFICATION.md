# Banner Template Specification

## Overview
This document provides exact specifications for the Instagram banner template based on analysis of `example.png`.

---

## Canvas Specifications

- **Output Size**: 1080x1080px (Instagram square format)
- **Format**: JPEG (quality: 95%) or PNG
- **Color Mode**: RGB

---

## Layout Components

### 1. White Content Box

**Purpose**: Container for quote icon and text content

**Specifications** (for 1080x1080px canvas):
```
Position: (119, 442)
Size: 763x437px
End Point: (882, 879)
Background: #FFFFFF (pure white)
```

**Current Code** (utils.py:63):
```python
draw.rectangle([(119, 442), (119 + 763, 1000)], fill="white")
```

**Issues**:
- ❌ Height is 558px (should be 437px)
- ❌ Box extends to Y=1000 (should end at Y=879)

---

### 2. Quote Icon

**Purpose**: Visual indicator for quoted/featured content

**Specifications** (scaled for 1080x1080px):
```
Asset: assets/quote.png
Color: Blue #4F86EC (RGB: 79, 134, 236)
Size: ~40x35px (scaled from example ratio)
Position: Top-left area of white box
Offset from white box:
  - X offset: ~41px from white box left edge
  - Y offset: ~43px from white box top edge
Absolute position: (~160, ~485)
```

**Current Code** (utils.py:44-66):
```python
quote_icon = Image.open(QUOTE_ICON_PATH).convert("RGBA").resize((59, 51))
# Tint to blue...
banner.paste(quote_icon, (160, 485), quote_icon)
```

**Issues**:
- ✅ Position looks correct
- ✅ Blue tinting implemented
- ⚠️ Size might be slightly large (59x51 vs recommended ~40x35)

---

### 3. Text Content

**Purpose**: Main headline/quote text

**Specifications**:
```
Font: Chivo Bold (assets/Chivo-Bold.ttf)
Color: #000000 (black)
Position: Starts at (~161, ~556)
Offset from white box:
  - X offset: ~42px from white box left
  - Y offset: ~114px from white box top
Max width: ~659px (white box width - margins)
Line height: 1.2x font size

**CRITICAL**: Font size should be DYNAMIC
- Text must auto-scale to fit within white box bounds
- White box dimensions are FIXED at 763x437px
- Never resize the white box to accommodate text
```

**Font Size Calculation**:
```python
# Pseudo-algorithm:
max_font_size = 50  # Start here
min_font_size = 20  # Minimum readable size
max_text_width = 659  # pixels
max_text_height = 280  # approximate available height in box

# Binary search or iterative reduction:
while text_height_with_wrapping > max_text_height:
    reduce font_size
    recalculate wrapped lines
    recalculate total height
```

**Current Code** (utils.py:59-73):
```python
title_font = ImageFont.truetype(FONT_PATH, 50)  # FIXED at 50pt
lines = wrap_text(text, title_font, max_text_width)
line_height = int(title_font.getbbox("A")[3] * 1.2)
text_y = 556
for line in lines:
    draw.text((161, text_y), line, font=title_font, fill="black")
    text_y += line_height
```

**Issues**:
- ❌ Font size is FIXED at 50pt (should be dynamic)
- ❌ No check if text overflows white box
- ✅ Text wrapping is implemented
- ✅ Positioning looks correct

---

### 4. Blue Footer Bar

**Purpose**: Branding bar with social media handle

**Specifications** (for 1080x1080px):
```
Position: (0, 1016)
Size: 1080x64px (full width, 64px height)
End Point: (1080, 1080)
Background: #4F86EC (RGB: 79, 134, 236)
```

**Current Code** (utils.py:77):
```python
draw.rectangle((0, 1016, 1080, 1080), fill="#4F86EC")
```

**Status**:
- ✅ Correct position
- ✅ Correct size
- ✅ Correct color

---

### 5. Instagram Icon

**Purpose**: Social media platform indicator

**Specifications**:
```
Asset: assets/instagram.png
Size: 26x26px
Position: (32, 1027)
Offset from footer top: 11px (to center in 64px footer)
Vertical centering: (footer_height - icon_height) / 2
  = (64 - 26) / 2 = 19px
**Correct Y position should be**: 1016 + 19 = 1035px
```

**Current Code** (utils.py:80):
```python
banner.paste(ig_icon, (32, 1027), ig_icon)
```

**Issues**:
- ✅ X position correct (32px from left)
- ❌ Y position is 1027 (should be 1035 for proper centering)

---

### 6. Footer Text (@handle)

**Purpose**: Social media handle/attribution

**Specifications**:
```
Font: Chivo Regular (assets/Chivo-Regular.ttf)
Size: 25pt
Color: #FFFFFF (white)
Position: (70, 1030)
Alignment: Should be vertically centered with Instagram icon

**Vertical Centering Calculation**:
Font baseline should align with icon center
Icon center Y: 1035 + 13 = 1048
Text Y adjustment needed for proper alignment
**Correct Y position**: ~1033px (may need fine-tuning based on font metrics)
```

**Current Code** (utils.py:83):
```python
draw.text((70, 1030), footer, font=footer_font, fill="white")
```

**Issues**:
- ✅ X position correct (70px from left, ~8px spacing from icon)
- ⚠️ Y position might need adjustment for perfect vertical alignment
- ✅ Font and color correct

---

## Code Comparison Summary

### What's Correct ✅
1. Blue footer bar - position, size, color
2. Quote icon - position and color tinting
3. Text wrapping logic
4. Font choices (Chivo Bold/Regular)
5. Instagram icon X position
6. Footer text X position and font

### Critical Issues ❌
1. **White box height** - extends too far (1000px vs 879px)
2. **Text sizing** - FIXED at 50pt instead of DYNAMIC
3. **Instagram icon Y position** - not vertically centered in footer
4. **Footer text Y position** - needs alignment adjustment

### Minor Issues ⚠️
1. Quote icon size might be slightly large
2. No overflow protection for text

---

## AI Background Generation Prompt

Use this prompt when generating backgrounds with AI:

```
Create a 1080x1080px square background image for Instagram.

COMPOSITION REQUIREMENTS:
1. Place main subject/focal point in TOP 440px (Y: 0-440)
2. AVOID important details in MIDDLE SECTION (Y: 442-879)
   → This area will be covered by a white content overlay
3. Keep bottom 64px (Y: 1016-1080) minimal
   → This area will have a blue footer bar
4. Recommended: Hero shot at top, gradient/blur toward middle
5. Safe zones:
   - Primary focus: Y=0 to Y=440
   - Will be visible but partially obscured: Y=0 to Y=1016
   - Completely hidden: Y=442 to Y=879 AND X=119 to X=882

EXAMPLES:
- Product photo: Product in top third, blurred/faded background below
- Landscape: Sky/horizon in top half, ground fades to neutral tone
- Portrait: Face/upper body in top 440px
- Camera: Camera positioned in top section
```

Example DALL-E/Midjourney prompt:
```
"Professional DSLR camera on clean background, camera positioned in upper
portion of frame, lower half fades to soft gradient, 1:1 aspect ratio,
high quality product photography, minimal composition"
```

---

## Next Steps

1. Fix white content box dimensions
2. Implement dynamic text sizing algorithm
3. Adjust Instagram icon and footer text vertical alignment
4. Add overflow protection/warnings
5. Test with various text lengths
6. Document edge cases
