#!/usr/bin/env python3
"""
Generate a premium product mockup for "Guia de Precificação para Confeiteiras"
Philosophy: Saccharine Cartography — warm artisanal precision, botanical exactitude
"""

import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

FONTS_DIR = r"C:\Users\Samuel Felipe\.claude\skills\canvas-design\canvas-fonts"

# Colors
CREAM      = (250, 246, 240)       # #FAF6F0
CARAMEL    = (193, 127,  62)       # #C17F3E
DARK_BROWN = ( 61,  43,  31)       # #3D2B1F
LIGHT_GOLD = (220, 175, 110)       # lighter caramel accent
DEEP_BROWN = ( 40,  26,  16)       # near-black for deep shadow
WARM_WHITE = (255, 252, 247)       # near white for highlights
MID_CREAM  = (240, 228, 210)       # mid-tone cream

# Canvas: 800x1066 — will be tilted and placed on 900x1100 final canvas
COVER_W, COVER_H = 800, 1066
FINAL_W, FINAL_H = 900, 1150

def load_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_circle_pattern(draw, cx, cy, radius, color, alpha_factor=1.0):
    """Draw a single precise circle outline"""
    r = int(radius)
    bbox = [cx - r, cy - r, cx + r, cy + r]
    draw.ellipse(bbox, outline=color, width=1)

def draw_botanical_sphere(img, cx, cy, radius, base_color, highlight_color):
    """Draw a precisely rendered sphere with gradient shading — like botanical illustration"""
    draw = ImageDraw.Draw(img)
    r = int(radius)
    # Build sphere layer by layer — concentric ellipses with varying opacity
    for i in range(r, 0, -1):
        t = i / r  # 1 at edge, 0 at center
        # Shade: darker at edges, lighter toward highlight
        factor = t * t
        c = tuple(int(base_color[j] * factor + highlight_color[j] * (1 - factor)) for j in range(3))
        bbox = [cx - i, cy - i, cx + i, cy + i]
        draw.ellipse(bbox, fill=c, outline=None)
    # Specular highlight — small bright ellipse offset up-left
    hx = cx - int(r * 0.25)
    hy = cy - int(r * 0.28)
    hr = max(2, int(r * 0.22))
    for i in range(hr, 0, -1):
        t = i / hr
        c = tuple(int(highlight_color[j] * (1 - t) + WARM_WHITE[j] * t) for j in range(3))
        draw.ellipse([hx - i, hy - i, hx + i, hy + i], fill=c)

def draw_delicate_circle(draw, cx, cy, r, color, width=1):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)

def draw_thin_line(draw, x1, y1, x2, y2, color, width=1):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

def create_cover():
    """Create the main book cover (flat, 800x1066)"""
    img = Image.new("RGBA", (COVER_W, COVER_H), CREAM + (255,))
    draw = ImageDraw.Draw(img)

    # ── Background subtle texture: very fine diagonal hatching ──
    hatch_color = (235, 224, 208, 80)
    hatch_draw = ImageDraw.Draw(img)
    step = 18
    for i in range(-COVER_H, COVER_W + COVER_H, step):
        hatch_draw.line([(i, 0), (i + COVER_H, COVER_H)], fill=hatch_color, width=1)

    # ── Border system: three nested precise rectangles ──
    # Outer border
    M1 = 28
    draw.rectangle([M1, M1, COVER_W - M1, COVER_H - M1],
                   outline=CARAMEL, width=2)
    # Inner thin border
    M2 = 38
    draw.rectangle([M2, M2, COVER_W - M2, COVER_H - M2],
                   outline=(*CARAMEL, 120), width=1)
    # Innermost hairline
    M3 = 48
    draw.rectangle([M3, M3, COVER_W - M3, COVER_H - M3],
                   outline=(*CARAMEL, 60), width=1)

    # ── Top ornamental band ──
    band_y1, band_y2 = 68, 102
    draw.rectangle([M1, band_y1, COVER_W - M1, band_y2],
                   fill=DARK_BROWN, outline=None)
    # Fine lines inside band
    draw.line([(M1 + 8, band_y1 + 4), (COVER_W - M1 - 8, band_y1 + 4)],
              fill=(*CARAMEL, 160), width=1)
    draw.line([(M1 + 8, band_y2 - 4), (COVER_W - M1 - 8, band_y2 - 4)],
              fill=(*CARAMEL, 160), width=1)

    # ── Botanical decoration zone — upper quadrant ──
    # Large background circle (faint, cream-on-cream) — compositional anchor
    cx_main = COVER_W // 2
    cy_main = 460
    R_main = 210

    # Ghost ring (large, very faint)
    for r_offset in range(0, 6):
        alpha = 35 - r_offset * 5
        if alpha > 0:
            draw.ellipse([cx_main - R_main - r_offset, cy_main - R_main - r_offset,
                          cx_main + R_main + r_offset, cy_main + R_main + r_offset],
                         outline=(*CARAMEL, alpha), width=1)

    # Precise concentric rings — botanical diagram style
    for r in [195, 180, 165, 148, 120, 95, 72]:
        opacity = 40 if r > 130 else 60 if r > 100 else 80
        draw.ellipse([cx_main - r, cy_main - r, cx_main + r, cy_main + r],
                     outline=(*CARAMEL, opacity), width=1)

    # Radial lines — like a compass rose, very thin
    num_radials = 24
    for i in range(num_radials):
        angle = (i / num_radials) * 2 * math.pi
        r_inner = 68
        r_outer = 195
        x1 = cx_main + r_inner * math.cos(angle)
        y1 = cy_main + r_inner * math.sin(angle)
        x2 = cx_main + r_outer * math.cos(angle)
        y2 = cy_main + r_outer * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(*CARAMEL, 30), width=1)

    # ── Central brigadeiro cluster — botanical illustration ──
    # Main large brigadeiro
    draw_botanical_sphere(img, cx_main, cy_main, 54,
                          base_color=(80, 48, 28),
                          highlight_color=(140, 88, 52))
    # Chocolate drip suggestion: dark teardrop below
    drip_draw = ImageDraw.Draw(img)
    drip_draw.ellipse([cx_main - 12, cy_main + 48, cx_main + 12, cy_main + 64],
                      fill=(65, 38, 20), outline=None)

    # Granule dots on top (the sprinkles)
    granule_positions = [
        (-8, -38), (4, -42), (-3, -30), (10, -36), (-14, -30),
        (6, -26), (-6, -44), (2, -20), (14, -28), (-12, -22),
    ]
    for gx, gy in granule_positions:
        gr = 3
        draw_botanical_sphere(img, cx_main + gx, cy_main + gy, gr,
                               base_color=(55, 30, 12),
                               highlight_color=(100, 62, 28))

    # Small satellite brigadeiros
    satellite_data = [
        (cx_main - 90, cy_main + 30, 34),
        (cx_main + 88, cy_main + 20, 30),
        (cx_main - 60, cy_main - 70, 26),
        (cx_main + 65, cy_main - 62, 22),
        (cx_main + 20, cy_main + 85, 20),
        (cx_main - 30, cy_main + 90, 18),
    ]
    for sx, sy, sr in satellite_data:
        draw_botanical_sphere(img, sx, sy, sr,
                               base_color=(78, 46, 25),
                               highlight_color=(130, 82, 46))
        # micro granules
        for angle in [0, 60, 120, 180, 240, 300]:
            a = math.radians(angle)
            mgx = sx + int((sr * 0.4) * math.cos(a))
            mgy = sy + int((sr * 0.55) * math.sin(a)) - int(sr * 0.2)
            draw_botanical_sphere(img, mgx, mgy, 2,
                                   base_color=(50, 28, 10),
                                   highlight_color=(90, 55, 22))

    # ── Fine measurement lines — scientific/cartographic style ──
    # Horizontal rule lines flanking the center composition
    rule_color = (*CARAMEL, 70)
    for y_offset in [-130, 130]:
        y_r = cy_main + y_offset
        draw.line([(M3 + 20, y_r), (cx_main - 240, y_r)], fill=rule_color, width=1)
        draw.line([(cx_main + 240, y_r), (COVER_W - M3 - 20, y_r)], fill=rule_color, width=1)
        # tick marks
        for tick_x in range(M3 + 20, cx_main - 240, 16):
            h = 5 if (tick_x - M3 - 20) % 48 == 0 else 3
            draw.line([(tick_x, y_r - h // 2), (tick_x, y_r + h // 2)],
                      fill=rule_color, width=1)

    # ── Decorative corner flourishes — four corners ──
    flourish_size = 40
    corners = [
        (M2 + 4, M2 + 4, 1, 1),
        (COVER_W - M2 - 4, M2 + 4, -1, 1),
        (M2 + 4, COVER_H - M2 - 4, 1, -1),
        (COVER_W - M2 - 4, COVER_H - M2 - 4, -1, -1),
    ]
    for fx, fy, dx, dy in corners:
        # L-shaped corner mark
        draw.line([(fx, fy), (fx + dx * flourish_size, fy)], fill=CARAMEL, width=2)
        draw.line([(fx, fy), (fx, fy + dy * flourish_size)], fill=CARAMEL, width=2)
        # Small dot at corner
        draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=CARAMEL)

    # ── Typography zone ──
    font_title     = load_font("Lora-Bold.ttf", 70)
    font_subtitle  = load_font("Italiana-Regular.ttf", 36)
    font_label     = load_font("InstrumentSans-Regular.ttf", 16)
    font_tagline   = load_font("Lora-Italic.ttf", 20)
    font_small     = load_font("InstrumentSans-Regular.ttf", 13)

    # ── Upper label in band ──
    band_label = "MÉTODO DE PRECIFICAÇÃO"
    bbox = draw.textbbox((0, 0), band_label, font=font_small)
    bw = bbox[2] - bbox[0]
    draw.text(((COVER_W - bw) // 2, band_y1 + 8),
              band_label, fill=LIGHT_GOLD, font=font_small)

    # ── Main title: "Guia de Precificação" ──
    title_y = 126
    # "GUIA DE" — smaller, spaced
    guia_label = "G U I A   D E"
    bbox = draw.textbbox((0, 0), guia_label, font=font_label)
    bw = bbox[2] - bbox[0]
    draw.text(((COVER_W - bw) // 2, title_y), guia_label,
              fill=DARK_BROWN, font=font_label)

    # "Precificação" — large elegant serif
    prec_text = "Precificação"
    bbox = draw.textbbox((0, 0), prec_text, font=font_title)
    bw = bbox[2] - bbox[0]
    # Subtle shadow for the main title
    draw.text(((COVER_W - bw) // 2 + 2, title_y + 26),
              prec_text, fill=(*CARAMEL, 80), font=font_title)
    draw.text(((COVER_W - bw) // 2, title_y + 24),
              prec_text, fill=DARK_BROWN, font=font_title)

    # ── Thin rule below title ──
    rule_y = title_y + 106
    rule_x1 = (COVER_W // 2) - 120
    rule_x2 = (COVER_W // 2) + 120
    draw.line([(rule_x1, rule_y), (rule_x2, rule_y)], fill=CARAMEL, width=1)
    # Center diamond on rule
    cx_d = COVER_W // 2
    draw.polygon([(cx_d - 5, rule_y), (cx_d, rule_y - 5),
                  (cx_d + 5, rule_y), (cx_d, rule_y + 5)], fill=CARAMEL)

    # ── Subtitle: "para Confeiteiras" ──
    sub_text = "para Confeiteiras"
    bbox = draw.textbbox((0, 0), sub_text, font=font_subtitle)
    bw = bbox[2] - bbox[0]
    draw.text(((COVER_W - bw) // 2, rule_y + 14),
              sub_text, fill=CARAMEL, font=font_subtitle)

    # ── Thin decorative line below subtitle ──
    sub_rule_y = rule_y + 58
    draw.line([(rule_x1 - 40, sub_rule_y), (rule_x2 + 40, sub_rule_y)],
              fill=(*DARK_BROWN, 80), width=1)

    # ── Lower section: content labels — botanical tag style ──
    lower_y_start = 700

    # Thin horizontal separator
    sep_y = lower_y_start - 10
    draw.line([(M3 + 20, sep_y), (COVER_W - M3 - 20, sep_y)],
              fill=(*CARAMEL, 100), width=1)

    # Four method pillars — labeled as fine tags
    pillars = [
        ("I N G R E D I E N T E S", M3 + 30),
        ("M Ã O   D E   O B R A", M3 + 185),
        ("C U S T O S   F I X O S", M3 + 350),
        ("L U C R O", M3 + 530),
    ]
    for pillar_text, px in pillars:
        bbox = draw.textbbox((0, 0), pillar_text, font=font_small)
        pw = bbox[2] - bbox[0]
        draw.text((px, lower_y_start), pillar_text,
                  fill=(*DARK_BROWN, 140), font=font_small)

    # Dots between pillars
    for dot_x in [M3 + 170, M3 + 335, M3 + 520]:
        draw.ellipse([dot_x - 2, lower_y_start + 4, dot_x + 2, lower_y_start + 8],
                     fill=(*CARAMEL, 150))

    # ── Small tagline ──
    tagline = "Brigadeiros · Bolo no Pote · Trufas"
    bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    bw = bbox[2] - bbox[0]
    draw.text(((COVER_W - bw) // 2, lower_y_start + 28),
              tagline, fill=(*CARAMEL, 180), font=font_tagline)

    # ── Bottom band ──
    bottom_y1 = COVER_H - M1 - 52
    bottom_y2 = COVER_H - M1
    draw.rectangle([M1, bottom_y1, COVER_W - M1, bottom_y2],
                   fill=DARK_BROWN, outline=None)
    draw.line([(M1 + 8, bottom_y1 + 4), (COVER_W - M1 - 8, bottom_y1 + 4)],
              fill=(*CARAMEL, 160), width=1)
    draw.line([(M1 + 8, bottom_y2 - 4), (COVER_W - M1 - 8, bottom_y2 - 4)],
              fill=(*CARAMEL, 160), width=1)

    # Bottom text
    font_bottom = load_font("InstrumentSans-Regular.ttf", 14)
    bottom_text = "G U I A   C O M P L E T O   D E   P R E C I F I C A Ç Ã O"
    bbox = draw.textbbox((0, 0), bottom_text, font=font_bottom)
    bw = bbox[2] - bbox[0]
    draw.text(((COVER_W - bw) // 2, bottom_y1 + 12),
              bottom_text, fill=LIGHT_GOLD, font=font_bottom)

    return img

def create_mockup():
    """Composite the cover at angle on a neutral background with shadow"""
    cover = create_cover()

    # Final canvas — warm off-white background
    bg_color = (245, 238, 228)
    final = Image.new("RGBA", (FINAL_W, FINAL_H), bg_color + (255,))

    # Subtle background gradient vignette (darkened corners)
    vignette = Image.new("RGBA", (FINAL_W, FINAL_H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    # radial-ish vignette via concentric rects
    for i in range(80):
        alpha = int(i * 1.2)
        vdraw.rectangle([i, i, FINAL_W - i, FINAL_H - i],
                        outline=(30, 18, 10, alpha), width=1)
    final = Image.alpha_composite(final, vignette)

    # Rotate cover slightly
    ANGLE = -5.0
    cover_rotated = cover.rotate(ANGLE, expand=True, resample=Image.BICUBIC)

    # Scale down to fit nicely
    scale = 0.72
    new_w = int(cover_rotated.width * scale)
    new_h = int(cover_rotated.height * scale)
    cover_rotated = cover_rotated.resize((new_w, new_h), Image.LANCZOS)

    # Position centered
    paste_x = (FINAL_W - new_w) // 2 + 5
    paste_y = (FINAL_H - new_h) // 2 - 10

    # ── Cast shadow ──
    shadow_offset_x = 22
    shadow_offset_y = 28
    shadow = Image.new("RGBA", final.size, (0, 0, 0, 0))
    shadow_mask = Image.new("L", (new_w, new_h), 0)
    # Build shadow from cover's alpha
    cover_alpha = cover_rotated.split()[3]
    shadow_mask.paste(cover_alpha, (0, 0))
    # Darken shadow
    shadow_layer = Image.new("RGBA", (new_w, new_h), (20, 10, 5, 180))
    shadow.paste(shadow_layer,
                 (paste_x + shadow_offset_x, paste_y + shadow_offset_y),
                 mask=shadow_mask)
    # Blur shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    final = Image.alpha_composite(final, shadow)

    # ── Secondary softer shadow (ambient) ──
    shadow2 = Image.new("RGBA", final.size, (0, 0, 0, 0))
    shadow2_layer = Image.new("RGBA", (new_w, new_h), (15, 8, 4, 100))
    shadow2.paste(shadow2_layer,
                  (paste_x + shadow_offset_x + 6, paste_y + shadow_offset_y + 6),
                  mask=shadow_mask)
    shadow2 = shadow2.filter(ImageFilter.GaussianBlur(radius=32))
    final = Image.alpha_composite(final, shadow2)

    # ── Paste the cover ──
    final.paste(cover_rotated, (paste_x, paste_y), mask=cover_rotated.split()[3])

    # ── Subtle edge highlight on cover (left edge gleam) ──
    # Already handled by cover border design

    # Convert to RGB for PNG export
    final_rgb = Image.new("RGB", (FINAL_W, FINAL_H), bg_color)
    final_rgb.paste(final, mask=final.split()[3])

    # Resize to exactly 600x800
    final_out = final_rgb.resize((600, 800), Image.LANCZOS)

    return final_out

if __name__ == "__main__":
    out_path = r"c:/Users/Samuel Felipe/OneDrive/Área de Trabalho/SaaS/Low Ticket Lucrativo/Kit Doce Lucro - Entregaveis/assets/mockup-guia.png"
    print("Generating mockup...")
    img = create_mockup()
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path}")
    print(f"Size: {img.size}")
