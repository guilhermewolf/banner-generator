# Official BannerBear Template Specifications

## Source
Extracted from BannerBear template editor screenshots (bannerbear/ directory)
Date: December 14, 2025

---

## Important Notes

**Original Template vs. Your Adaptation:**
- BannerBear template uses **RED theme** (#DE3F1C)
- You modified it to **BLUE theme** (#4F86EC) for Sigma camera posts
- Original has 3 social icons (Facebook, Instagram, Twitter)
- Your version uses only Instagram icon
- Original has website URL in footer - you removed it

---

## Canvas

- **Size**: 1080x1080px (Instagram square)
- **Format**: JPEG/PNG

---

## Layer Structure (Bottom to Top)

### 1. Background Image
- Full canvas: 1080x1080px
- User-provided image

### 2. rectangle_border1 (Footer Bar)
```
Name: rectangle_border1
Position: X=-62, Y=935
Size: W=1083, H=79
Color: #DE3F1C (ORIGINAL - RED)
       #4F86EC (YOUR VERSION - BLUE)
Purpose: Full-width footer bar
```

**Note**: X=-62 means it extends 62px beyond left edge for full bleed

### 3. rectangle_background (White Content Box)
```
Name: rectangle_background
Position: X=119, Y=445
Size: W=763, H=437
Color: #fff (white)
Purpose: Main content container
```

**CRITICAL**: Note Y=445, not Y=442!

### 4. rectangle_border2 (Accent Line)
```
Name: rectangle_border2
Position: X=119, Y=879
Size: W=763, H=14
Color: #DE3F1C (RED accent line)
Purpose: Bottom border of white box
```

**Note**: You may have removed this in your blue version

### 5. svg_quote (Quote Icon)
```
Name: svg_quote
Position: X=160, Y=485
Size: W=59, H=51
Color: #DE3F1C (ORIGINAL - RED)
       #4F86EC (YOUR VERSION - BLUE)
Format: SVG
Purpose: Quote indicator
```

### 6. title (Main Text/Headline)
```
Name: title
Position: X=161, Y=556
Size: W=659, H=22
Text Fit: ON ⭐
Font: Chivo
Size: 50
Weight: 700 (Bold)
Line Height: 1.2
Horizontal Align: left
Vertical Align: top
Color: Black
```

**KEY FEATURE**: Text Fit is **ON** - this is BannerBear's auto-sizing!
- Height H=22 is minimum/collapsed height
- Text automatically scales font size to fit within W=659
- This is how BannerBear handles dynamic text

### 7. label_tag (Person/Label - Optional)
```
Name: label_tag
Position: X=117, Y=367
Size: W=614, H=68
Text Fit: ON
Font: Chivo
Size: 50
Weight: 700
Line Height: 1
```

**Note**: Used for "OLIVIA WELLSON" in original - you likely don't use this

### 8. subtitle (Date/Subtitle - Optional)
```
Name: subtitle
Position: X=163, Y=813
Size: W=632, H=30
Text Fit: ON
Font: Chivo
Size: 50
Weight: 400
Line Height: 1.2
Horizontal Align: left
Vertical Align: bottom
```

**Note**: Used for "Published on April 12, 2023" - you likely don't use this

### 9. svg_shape1 (Facebook Icon - Removed in your version)
```
Position: X=26, Y=954
Size: W=13, H=26
Color: #fff
```

### 10. svg_shape2 (Instagram Icon)
```
Name: svg_shape2
Position: X=57, Y=954
Size: W=26, H=26
Color: #fff (white)
Format: SVG
Purpose: Instagram icon
```

### 11. svg_shape3 (Twitter Icon - Removed in your version)
```
Position: X=98, Y=956
Size: W=26, H=22
Color: #fff
```

### 12. footer_1 (@Handle Text)
```
Name: footer_1
Position: X=134, Y=954
Size: W=257, H=25
Text Fit: ON
Font: Chivo
Size: 50
Weight: 400 (Regular)
Line Height: 1.2
Horizontal Align: left
Vertical Align: center
Color: White
```

**Your Content**: "@TheSignalDaily" or "@TheSigmaGalaxy"

### 13. footer_2 (Website URL - Removed in your version)
```
Name: footer_2
Position: X=720, Y=955
Size: W=257, H=25
Text Fit: ON
Font: Chivo
Size: 50
Weight: 400
Line Height: 1.2
Horizontal Align: right
Vertical Align: center
Color: White
```

**Original Content**: "newsmediasite.com" - you removed this

---

## Key Differences from Previous Analysis

| Element | Previous (Calculated) | Official (BannerBear) | Difference |
|---------|----------------------|----------------------|------------|
| White Box Y | 442 | **445** | +3px |
| White Box Height | 437 | **437** | ✅ Correct |
| Footer Y | 1016 | **935** | -81px! |
| Footer Height | 64 | **79** | +15px |
| Instagram Icon X | 32 | **57** | +25px |
| Instagram Icon Y | 1035 | **954** | -81px |
| Footer Text X | 70 | **134** | +64px |
| Footer Text Y | 1036 | **954** | -82px |
| Quote Icon Size | 40x35 | **59x51** | Larger |
| Main Text Y | 556 | **556** | ✅ Correct |

---

## Text Fit Feature

BannerBear's **"Text Fit: ON"** setting:
- Automatically adjusts font size to fit text within box width
- Starts at specified font size (50pt)
- Reduces font size if text would overflow
- Maintains aspect ratio and readability
- This is exactly what we implemented with `calculate_dynamic_font_size()`!

---

## Your Modifications for Sigma Template

Changes you made to the original BannerBear template:

1. ✅ Changed theme from RED (#DE3F1C) to BLUE (#4F86EC)
2. ✅ Removed Facebook icon (svg_shape1)
3. ✅ Removed Twitter icon (svg_shape3)
4. ✅ Kept Instagram icon only
5. ✅ Removed website URL (footer_2)
6. ✅ Changed footer text to @TheSigmaGalaxy / @TheSignalDaily
7. ✅ Likely removed label_tag (person name)
8. ✅ Likely removed subtitle (date)
9. ✅ Possibly removed rectangle_border2 (red accent line)

---

## AI Background Generation Guide

Based on official layout:

```
Safe Zones for Background Image (1080x1080px):

1. TOP SECTION (Fully Visible)
   Y: 0-445px (top 445px)
   → Main subject should be here

2. WHITE BOX OVERLAY AREA (Partially/Fully Obscured)
   X: 119-882px, Y: 445-879px
   → Avoid important details here
   → Use blur, gradient, or neutral background

3. ACCENT LINE (if using)
   Y: 879-893px (14px tall red/blue line)
   → Decorative border

4. FOOTER BAR AREA (Completely Obscured)
   Y: 935-1014px (79px tall)
   → Will be covered by blue bar
   → Keep minimal/clean
```

**Optimal Composition**:
- Hero subject: Y=0 to Y=400
- Fade/blur zone: Y=400 to Y=880
- Clean zone: Y=880 to Y=1080

---

## Implementation Checklist

- [ ] Update white box position to Y=445 (from 442)
- [ ] Update footer bar to Y=935, H=79 (from Y=1016, H=64)
- [ ] Update Instagram icon to X=57, Y=954 (from X=32, Y=1035)
- [ ] Update footer text to X=134, Y=954 (from X=70, Y=1036)
- [ ] Keep quote icon at 59x51 (revert from 40x35)
- [ ] Keep dynamic text sizing (Text Fit equivalent)
- [ ] Confirm all positioning matches BannerBear exactly
