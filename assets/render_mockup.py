#!/usr/bin/env python3
"""
Planilha Doce Lucro Pro — Product Mockup
Design Philosophy: Saccharine Ledger
600x800px PNG portrait
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# ── Palette ─────────────────────────────────────────────────────────────────
CREAM      = "#FAF6F0"
CREAM_MID  = "#F0E9DF"
CARAMEL    = "#C17F3E"
CARAMEL_LT = "#D4965A"
DARK_BROWN = "#3D2B1F"
BROWN_MID  = "#6B4D35"
GREEN      = "#6B7C47"
GREEN_LT   = "#8A9F5E"
WHITE      = "#FFFFFF"
RULE_COLOR = "#DDD3C5"
CELL_ALT   = "#F5EDE2"

W, H = 600, 800

FONTS_DIR = r"C:\Users\Samuel Felipe\.claude\skills\canvas-design\canvas-fonts"

def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
    except:
        return ImageFont.load_default()

# ── Load Fonts ───────────────────────────────────────────────────────────────
font_title      = load_font("Lora-Bold.ttf", 22)
font_subtitle   = load_font("WorkSans-Regular.ttf", 10)
font_mono_sm    = load_font("IBMPlexMono-Regular.ttf", 8)
font_mono_bold  = load_font("IBMPlexMono-Bold.ttf", 9)
font_label      = load_font("WorkSans-Regular.ttf", 8)
font_label_bold = load_font("WorkSans-Bold.ttf", 9)
font_badge      = load_font("WorkSans-Bold.ttf", 7)
font_tab        = load_font("WorkSans-Regular.ttf", 8)
font_tab_active = load_font("WorkSans-Bold.ttf", 8)
font_chart_lbl  = load_font("IBMPlexMono-Regular.ttf", 7)
font_kpi_val    = load_font("Lora-Bold.ttf", 18)
font_kpi_lbl    = load_font("WorkSans-Regular.ttf", 7)
font_tagline    = load_font("Lora-Italic.ttf", 11)
font_branding   = load_font("Lora-Bold.ttf", 15)
font_version    = load_font("WorkSans-Regular.ttf", 7)

img  = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def blend(c1, c2, t):
    r1,g1,b1 = hex2rgb(c1)
    r2,g2,b2 = hex2rgb(c2)
    return (int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0,y0,x1,y1 = xy
    r = radius
    if fill:
        draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
        draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
        draw.ellipse([x0, y0, x0+2*r, y0+2*r], fill=fill)
        draw.ellipse([x1-2*r, y0, x1, y0+2*r], fill=fill)
        draw.ellipse([x0, y1-2*r, x0+2*r, y1], fill=fill)
        draw.ellipse([x1-2*r, y1-2*r, x1, y1], fill=fill)
    if outline:
        draw.arc([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0+r, y0, x1-r, y0], fill=outline, width=width)
        draw.line([x0+r, y1, x1-r, y1], fill=outline, width=width)
        draw.line([x0, y0+r, x0, y1-r], fill=outline, width=width)
        draw.line([x1, y0+r, x1, y1-r], fill=outline, width=width)

def center_text(draw, text, y, font, color, x0=0, x1=W):
    bb = draw.textbbox((0,0), text, font=font)
    tw = bb[2]-bb[0]
    x = x0 + (x1-x0-tw)//2
    draw.text((x, y), text, font=font, fill=color)

def right_text(draw, text, y, font, color, right_x):
    bb = draw.textbbox((0,0), text, font=font)
    tw = bb[2]-bb[0]
    draw.text((right_x-tw, y), text, font=font, fill=color)

# ─────────────────────────────────────────────────────────────────────────────
# 1. BACKGROUND TEXTURE — fine horizontal rules across full canvas
# ─────────────────────────────────────────────────────────────────────────────
for y in range(0, H, 14):
    draw.line([(0, y), (W, y)], fill=hex2rgb(RULE_COLOR), width=1)

# ─────────────────────────────────────────────────────────────────────────────
# 2. TOP HEADER BAND
# ─────────────────────────────────────────────────────────────────────────────
HEADER_H = 96
# Solid dark-brown header
draw.rectangle([0, 0, W, HEADER_H], fill=hex2rgb(DARK_BROWN))

# Subtle diagonal-stripe texture on header
for i in range(-HEADER_H, W+HEADER_H, 18):
    draw.line([(i, 0), (i+HEADER_H, HEADER_H)], fill=(255,255,255,12), width=1)

# Thin caramel accent line at header bottom
draw.line([(0, HEADER_H), (W, HEADER_H)], fill=hex2rgb(CARAMEL), width=2)

# Brand title
center_text(draw, "Planilha Doce Lucro Pro", 18, font_title, CREAM)

# Tagline
center_text(draw, "Calculadora de Custos para Confeitaria Profissional", 48, font_tagline, hex2rgb(CARAMEL_LT))

# Version badge
badge_txt = "v 2.0 · Excel & Google Sheets"
bb = draw.textbbox((0,0), badge_txt, font=font_version)
bw = bb[2]-bb[0]+20
bh = bb[3]-bb[1]+8
bx = (W-bw)//2
by = 68
draw_rounded_rect(draw, [bx, by, bx+bw, by+bh], 4, fill=hex2rgb(BROWN_MID))
center_text(draw, badge_txt, by+4, font_version, hex2rgb(CREAM_MID))

# ─────────────────────────────────────────────────────────────────────────────
# 3. TAB ROW
# ─────────────────────────────────────────────────────────────────────────────
TAB_Y    = HEADER_H + 2
TAB_H    = 26
tabs = [
    ("Calculadora de Custo", True),
    ("Histórico",            False),
    ("Simulador de Metas",   False),
    ("Guia de Uso",          False),
]
tab_x = 0
tab_widths = [178, 100, 154, 90]
for (label, active), tw in zip(tabs, tab_widths):
    bg = hex2rgb(CARAMEL) if active else hex2rgb(CREAM_MID)
    fg = hex2rgb(WHITE) if active else hex2rgb(BROWN_MID)
    draw.rectangle([tab_x, TAB_Y, tab_x+tw-1, TAB_Y+TAB_H], fill=bg)
    if not active:
        draw.line([(tab_x+tw-1, TAB_Y), (tab_x+tw-1, TAB_Y+TAB_H)], fill=hex2rgb(RULE_COLOR), width=1)
    # Center text in tab
    bb = draw.textbbox((0,0), label, font=font_tab_active if active else font_tab)
    tx = tab_x + (tw - (bb[2]-bb[0]))//2
    ty = TAB_Y + (TAB_H - (bb[3]-bb[1]))//2
    draw.text((tx, ty), label, font=font_tab_active if active else font_tab, fill=fg)
    tab_x += tw

# Bottom border of tab row
CONTENT_Y = TAB_Y + TAB_H + 1
draw.line([(0, CONTENT_Y-1), (W, CONTENT_Y-1)], fill=hex2rgb(CARAMEL), width=1)

# ─────────────────────────────────────────────────────────────────────────────
# 4. SPREADSHEET BODY — columns + rows
# ─────────────────────────────────────────────────────────────────────────────
BODY_X = 24
BODY_W = W - 48
ROW_H  = 22
COL_HEADERS = ["Ingrediente", "Qtd.", "Unid.", "Custo Unit.", "Custo Total"]
COL_W       = [145, 48, 52, 88, 88]
assert sum(COL_W) == BODY_W, f"col widths sum {sum(COL_W)} != {BODY_W}"

TABLE_Y = CONTENT_Y + 14

# ── Column header row ──
ch_y = TABLE_Y
draw.rectangle([BODY_X, ch_y, BODY_X+BODY_W, ch_y+ROW_H], fill=hex2rgb(DARK_BROWN))
cx = BODY_X
for i, (hdr, cw) in enumerate(zip(COL_HEADERS, COL_W)):
    bb = draw.textbbox((0,0), hdr, font=font_mono_bold)
    tx = cx + (cw - (bb[2]-bb[0]))//2
    draw.text((tx, ch_y+6), hdr, font=font_mono_bold, fill=hex2rgb(CREAM))
    if i < len(COL_HEADERS)-1:
        draw.line([(cx+cw, ch_y+4), (cx+cw, ch_y+ROW_H-4)], fill=hex2rgb(BROWN_MID), width=1)
    cx += cw

# ── Data rows ──
data_rows = [
    ("Farinha de trigo",   "500",  "g",    "R$ 0,012",  "R$ 6,00"),
    ("Manteiga sem sal",   "200",  "g",    "R$ 0,040",  "R$ 8,00"),
    ("Açúcar refinado",    "300",  "g",    "R$ 0,008",  "R$ 2,40"),
    ("Ovos caipira",       "4",    "un",   "R$ 1,200",  "R$ 4,80"),
    ("Chocolate 70%",      "150",  "g",    "R$ 0,095",  "R$ 14,25"),
    ("Creme de leite",     "200",  "ml",   "R$ 0,018",  "R$ 3,60"),
    ("Essência de baunilha","10",  "ml",   "R$ 0,180",  "R$ 1,80"),
    ("Fermento químico",   "10",   "g",    "R$ 0,022",  "R$ 0,22"),
]

row_y = ch_y + ROW_H
for i, row_data in enumerate(data_rows):
    bg = hex2rgb(CREAM) if i % 2 == 0 else hex2rgb(CELL_ALT)
    draw.rectangle([BODY_X, row_y, BODY_X+BODY_W, row_y+ROW_H-1], fill=bg)
    cx = BODY_X
    for j, (cell, cw) in enumerate(zip(row_data, COL_W)):
        is_money = cell.startswith("R$")
        fnt = font_mono_sm
        fg = hex2rgb(DARK_BROWN)
        if j == 4:  # total column — highlight
            fg = hex2rgb(BROWN_MID)
            fnt = font_mono_bold
        if j == 0:
            draw.text((cx+6, row_y+6), cell, font=fnt, fill=fg)
        else:
            bb = draw.textbbox((0,0), cell, font=fnt)
            tx = cx + cw - (bb[2]-bb[0]) - 8
            draw.text((tx, row_y+6), cell, font=fnt, fill=fg)
        if j < len(row_data)-1:
            draw.line([(cx+cw, row_y+3), (cx+cw, row_y+ROW_H-4)], fill=hex2rgb(RULE_COLOR), width=1)
        cx += cw
    # horizontal bottom rule
    draw.line([(BODY_X, row_y+ROW_H-1), (BODY_X+BODY_W, row_y+ROW_H-1)], fill=hex2rgb(RULE_COLOR), width=1)
    row_y += ROW_H

# Outer border of table
draw.rectangle([BODY_X, TABLE_Y, BODY_X+BODY_W, row_y], outline=hex2rgb(CARAMEL), width=1)

# ─────────────────────────────────────────────────────────────────────────────
# 5. TOTALS / FORMULA ROW
# ─────────────────────────────────────────────────────────────────────────────
TOTAL_Y = row_y + 1
draw.rectangle([BODY_X, TOTAL_Y, BODY_X+BODY_W, TOTAL_Y+ROW_H+2], fill=hex2rgb(CARAMEL))
# "TOTAL DE INSUMOS" label
draw.text((BODY_X+8, TOTAL_Y+6), "TOTAL DE INSUMOS", font=font_mono_bold, fill=hex2rgb(CREAM))
# Total value
total_val = "R$ 41,07"
bb = draw.textbbox((0,0), total_val, font=font_mono_bold)
draw.text((BODY_X+BODY_W-(bb[2]-bb[0])-8, TOTAL_Y+6), total_val, font=font_mono_bold, fill=hex2rgb(WHITE))

# ─────────────────────────────────────────────────────────────────────────────
# 6. KPI CARDS ROW
# ─────────────────────────────────────────────────────────────────────────────
KPI_Y   = TOTAL_Y + ROW_H + 2 + 16
KPI_H   = 68
CARD_W  = (BODY_W - 16) // 3
GAP     = 8

kpis = [
    ("Custo Total", "R$ 41,07", CARAMEL),
    ("Preço Sugerido", "R$ 98,57", GREEN),
    ("Margem Lucro", "58,3 %", DARK_BROWN),
]

for i, (lbl, val, clr) in enumerate(kpis):
    cx = BODY_X + i*(CARD_W+GAP)
    draw_rounded_rect(draw, [cx, KPI_Y, cx+CARD_W, KPI_Y+KPI_H], 6, fill=hex2rgb(clr))
    # Value
    bb = draw.textbbox((0,0), val, font=font_kpi_val)
    tw = bb[2]-bb[0]
    draw.text((cx + (CARD_W-tw)//2, KPI_Y+10), val, font=font_kpi_val, fill=hex2rgb(WHITE))
    # Label
    center_text(draw, lbl.upper(), KPI_Y+40, font_kpi_lbl, hex2rgb(CREAM), cx, cx+CARD_W)
    # Thin top accent bar
    draw.rectangle([cx, KPI_Y, cx+CARD_W, KPI_Y+3], fill=hex2rgb(WHITE)+(60,))

# ─────────────────────────────────────────────────────────────────────────────
# 7. MINI BAR CHART — "Distribuição de Custos"
# ─────────────────────────────────────────────────────────────────────────────
CHART_Y = KPI_Y + KPI_H + 18
CHART_H = 92
CHART_X = BODY_X
CHART_W = BODY_W

# Chart background
draw_rounded_rect(draw, [CHART_X, CHART_Y, CHART_X+CHART_W, CHART_Y+CHART_H], 6, fill=hex2rgb(WHITE))
draw_rounded_rect(draw, [CHART_X, CHART_Y, CHART_X+CHART_W, CHART_Y+CHART_H], 6, outline=hex2rgb(RULE_COLOR), width=1)

# Chart title
draw.text((CHART_X+12, CHART_Y+8), "Distribuição de Custos por Ingrediente", font=font_label_bold, fill=hex2rgb(DARK_BROWN))
draw.line([(CHART_X+12, CHART_Y+20), (CHART_X+CHART_W-12, CHART_Y+20)], fill=hex2rgb(RULE_COLOR), width=1)

# Bars
bar_data = [
    ("Farinha",     6.00,  CREAM_MID),
    ("Manteiga",    8.00,  CARAMEL_LT),
    ("Açúcar",      2.40,  CREAM_MID),
    ("Ovos",        4.80,  CARAMEL_LT),
    ("Chocolate",  14.25,  CARAMEL),
    ("Creme",       3.60,  CREAM_MID),
    ("Baunilha",    1.80,  CREAM_MID),
    ("Fermento",    0.22,  CREAM_MID),
]

max_val = max(v for _,v,_ in bar_data)
N = len(bar_data)
bar_area_x = CHART_X + 12
bar_area_w = CHART_W - 24
bar_area_y = CHART_Y + 26
bar_area_h = CHART_H - 42
bw = (bar_area_w - (N-1)*4) // N

for i, (lbl, val, clr) in enumerate(bar_data):
    bx = bar_area_x + i*(bw+4)
    bar_h = int((val/max_val)*bar_area_h)
    by = bar_area_y + bar_area_h - bar_h
    # shadow
    draw.rectangle([bx+2, by+2, bx+bw+2, bar_area_y+bar_area_h+2], fill=hex2rgb(RULE_COLOR))
    # bar
    draw.rectangle([bx, by, bx+bw, bar_area_y+bar_area_h], fill=hex2rgb(clr))
    # top value
    val_str = f"{val:.0f}"
    bb = draw.textbbox((0,0), val_str, font=font_chart_lbl)
    tw = bb[2]-bb[0]
    draw.text((bx+(bw-tw)//2, by-10), val_str, font=font_chart_lbl, fill=hex2rgb(DARK_BROWN))
    # label
    bb2 = draw.textbbox((0,0), lbl, font=font_chart_lbl)
    lw = bb2[2]-bb2[0]
    draw.text((bx+(bw-lw)//2, bar_area_y+bar_area_h+3), lbl, font=font_chart_lbl, fill=hex2rgb(BROWN_MID))

# Highlight bar for max value (Chocolate)
choc_i = 4
bx = bar_area_x + choc_i*(bw+4)
val = bar_data[choc_i][1]
bar_h = int((val/max_val)*bar_area_h)
by = bar_area_y + bar_area_h - bar_h
draw.rectangle([bx, by, bx+bw, bar_area_y+bar_area_h], fill=hex2rgb(CARAMEL))
# accent outline
draw.rectangle([bx, by, bx+bw, bar_area_y+bar_area_h], outline=hex2rgb(DARK_BROWN), width=1)

# ─────────────────────────────────────────────────────────────────────────────
# 8. FORMULA REFERENCE STRIP
# ─────────────────────────────────────────────────────────────────────────────
FORMULA_Y = CHART_Y + CHART_H + 14
draw.rectangle([BODY_X, FORMULA_Y, BODY_X+BODY_W, FORMULA_Y+20], fill=hex2rgb(DARK_BROWN))
formula_txt = "=SOMA(E4:E11)  ·  Preço = Custo / (1 - Margem%)  ·  Margem = 1 - (Custo / Preço)"
bb = draw.textbbox((0,0), formula_txt, font=font_mono_sm)
tw = bb[2]-bb[0]
draw.text((BODY_X + (BODY_W-tw)//2, FORMULA_Y+6), formula_txt, font=font_mono_sm, fill=hex2rgb(CARAMEL_LT))

# ─────────────────────────────────────────────────────────────────────────────
# 9. FOOTER
# ─────────────────────────────────────────────────────────────────────────────
FOOTER_Y = H - 52
draw.rectangle([0, FOOTER_Y, W, H], fill=hex2rgb(DARK_BROWN))
draw.line([(0, FOOTER_Y), (W, FOOTER_Y)], fill=hex2rgb(CARAMEL), width=2)

# Green accent pill
pill_txt = "● Fórmulas automáticas"
pill_x = BODY_X
bb = draw.textbbox((0,0), pill_txt, font=font_badge)
pw = bb[2]-bb[0]+16
draw_rounded_rect(draw, [pill_x, FOOTER_Y+12, pill_x+pw, FOOTER_Y+28], 6, fill=hex2rgb(GREEN))
draw.text((pill_x+8, FOOTER_Y+15), pill_txt, font=font_badge, fill=hex2rgb(WHITE))

pill2_txt = "● 4 abas incluídas"
px2 = pill_x + pw + 8
bb2 = draw.textbbox((0,0), pill2_txt, font=font_badge)
pw2 = bb2[2]-bb2[0]+16
draw_rounded_rect(draw, [px2, FOOTER_Y+12, px2+pw2, FOOTER_Y+28], 6, fill=hex2rgb(CARAMEL))
draw.text((px2+8, FOOTER_Y+15), pill2_txt, font=font_badge, fill=hex2rgb(WHITE))

pill3_txt = "● Guia passo a passo"
px3 = px2 + pw2 + 8
bb3 = draw.textbbox((0,0), pill3_txt, font=font_badge)
pw3 = bb3[2]-bb3[0]+16
draw_rounded_rect(draw, [px3, FOOTER_Y+12, px3+pw3, FOOTER_Y+28], 6, fill=hex2rgb(BROWN_MID))
draw.text((px3+8, FOOTER_Y+15), pill3_txt, font=font_badge, fill=hex2rgb(WHITE))

# Bottom brand line
center_text(draw, "Doce Lucro Pro — precisão que transforma receita em resultado", FOOTER_Y+34, font_version, hex2rgb(CREAM_MID))

# ─────────────────────────────────────────────────────────────────────────────
# 10. FINE POLISH PASS
# ─────────────────────────────────────────────────────────────────────────────
# Outer canvas hairline border
draw.rectangle([0, 0, W-1, H-1], outline=hex2rgb(CARAMEL), width=2)

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
OUT = r"c:/Users/Samuel Felipe/OneDrive/Área de Trabalho/SaaS/Low Ticket Lucrativo/Kit Doce Lucro - Entregaveis/assets/mockup-planilha.png"
img.save(OUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUT}")
