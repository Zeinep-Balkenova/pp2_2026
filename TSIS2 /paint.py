"""
paint.py — TSIS2 Extended Paint Application
Builds on Exercises 10 & 11 with: pencil, line, fill, text, brush sizes, Ctrl+S save.
"""
 
import pygame
import sys
from datetime import datetime
from tools import (
    flood_fill, draw_shape, BRUSH_SIZES
)
 
# ── Constants ─────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1100, 700
TOOLBAR_W = 200
CANVAS_X = TOOLBAR_W
CANVAS_W = WIDTH - TOOLBAR_W
CANVAS_H = HEIGHT
 
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG    = (30, 30, 40)      # toolbar background
PANEL = (45, 45, 58)      # button background
SEL   = (90, 130, 220)    # selected highlight
TEXT_COL = (220, 220, 230)
 
PALETTE = [
    (0,   0,   0),    # black
    (255, 255, 255),  # white
    (220,  50,  50),  # red
    ( 50, 200,  80),  # green
    ( 60, 120, 230),  # blue
    (255, 200,   0),  # yellow
    (255, 140,   0),  # orange
    (180,  60, 220),  # purple
    ( 30, 200, 200),  # cyan
    (200, 100, 150),  # pink
    (120,  80,  40),  # brown
    (150, 150, 150),  # gray
]
 
TOOLS = [
    ("pencil",    "Pencil (P)"),
    ("line",      "Line (L)"),
    ("rect",      "Rectangle (R)"),
    ("square",    "Square (Q)"),
    ("circle",    "Circle (C)"),
    ("right_tri", "Rt Triangle (T)"),
    ("eq_tri",    "Eq Triangle (E)"),
    ("diamond",   "Diamond (D)"),
    ("fill",      "Fill (F)"),
    ("text",      "Text (X)"),
    ("eraser",    "Eraser (A)"),
]
 
TOOL_KEYS = {
    pygame.K_p: "pencil",
    pygame.K_l: "line",
    pygame.K_r: "rect",
    pygame.K_q: "square",
    pygame.K_c: "circle",
    pygame.K_t: "right_tri",
    pygame.K_e: "eq_tri",
    pygame.K_d: "diamond",
    pygame.K_f: "fill",
    pygame.K_x: "text",
    pygame.K_a: "eraser",
}
 
 
# ── UI helpers ────────────────────────────────────────────────────────────────
def draw_button(surface, rect, label, selected, font, small=False):
    color = SEL if selected else PANEL
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (70, 70, 90), rect, 1, border_radius=6)
    txt = font.render(label, True, TEXT_COL)
    surface.blit(txt, txt.get_rect(center=rect.center))
 
 
def make_toolbar_layout(font_sm):
    """Return list of (rect, tool_key) for tool buttons."""
    buttons = []
    pad, bw, bh = 8, TOOLBAR_W - 16, 30
    y = 10
    for key, label in TOOLS:
        rect = pygame.Rect(pad, y, bw, bh)
        buttons.append((rect, key))
        y += bh + 4
    return buttons, y
 
 
# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint — Extended Tools")
    clock = pygame.time.Clock()
 
    font_sm = pygame.font.SysFont("segoeui", 13)
    font_md = pygame.font.SysFont("segoeui", 16)
    font_text = pygame.font.SysFont("segoeui", 24)   # for text tool
 
    # Canvas surface (white background)
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(WHITE)
 
    # State
    current_tool = "pencil"
    current_color = BLACK
    brush_key = 2                          # 1/2/3 → thin/medium/thick
    drawing = False
    start_pos = None
    prev_pos = None
 
    # Text tool state
    text_mode = False
    text_cursor = None   # (x, y) on canvas
    text_buffer = ""
 
    # Status message
    status_msg = ""
    status_timer = 0
 
    # Build toolbar layout
    tool_buttons, next_y = make_toolbar_layout(font_sm)
 
    # Brush size button rects
    pad = 8
    bsz_y = next_y + 10
    bsz_labels = {1: "Thin (1)", 2: "Med (2)", 3: "Thick (3)"}
    bsz_rects = {}
    bw = (TOOLBAR_W - 16 - 8) // 3
    for i, k in enumerate([1, 2, 3]):
        rx = pad + i * (bw + 4)
        bsz_rects[k] = pygame.Rect(rx, bsz_y, bw, 26)
 
    # Palette swatches
    pal_y = bsz_y + 40
    swatch_size = 22
    swatches = []
    cols = 6
    for idx, col in enumerate(PALETTE):
        r = idx // cols
        c = idx % cols
        sx = pad + c * (swatch_size + 2)
        sy = pal_y + r * (swatch_size + 2)
        swatches.append((pygame.Rect(sx, sy, swatch_size, swatch_size), col))
 
    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS)
 
        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            # ── Key down ──────────────────────────────────────────────────────
            elif event.type == pygame.KEYDOWN:
 
                # Text tool typing
                if text_mode:
                    if event.key == pygame.K_RETURN:
                        # Commit text to canvas
                        if text_buffer:
                            txt_surf = font_text.render(text_buffer, True, current_color)
                            canvas.blit(txt_surf, text_cursor)
                        text_mode = False
                        text_buffer = ""
                        text_cursor = None
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_buffer = ""
                        text_cursor = None
                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            text_buffer += event.unicode
                    continue   # don't process other shortcuts while typing
 
                # Ctrl+S — save
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{ts}.png"
                    pygame.image.save(canvas, filename)
                    status_msg = f"Saved: {filename}"
                    status_timer = 180
                    continue
 
                # Brush size shortcuts
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    brush_key = int(event.unicode)
 
                # Tool shortcuts
                if event.key in TOOL_KEYS:
                    current_tool = TOOL_KEYS[event.key]
 
            # ── Mouse button down ──────────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
 
                # --- Toolbar clicks ---
                # Tool buttons
                for rect, key in tool_buttons:
                    if rect.collidepoint(mx, my):
                        current_tool = key
                        text_mode = False
                        text_buffer = ""
 
                # Brush size buttons
                for k, rect in bsz_rects.items():
                    if rect.collidepoint(mx, my):
                        brush_key = k
 
                # Palette swatches
                for rect, col in swatches:
                    if rect.collidepoint(mx, my):
                        current_color = col
 
                # --- Canvas clicks ---
                if mx >= CANVAS_X:
                    cx, cy = mx - CANVAS_X, my
 
                    if current_tool == "fill":
                        flood_fill(canvas, cx, cy, current_color)
 
                    elif current_tool == "text":
                        text_mode = True
                        text_cursor = (cx, cy)
                        text_buffer = ""
 
                    else:
                        drawing = True
                        start_pos = (cx, cy)
                        prev_pos = (cx, cy)
 
            # ── Mouse button up ────────────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and start_pos:
                    mx, my = event.pos
                    if mx >= CANVAS_X:
                        cx, cy = mx - CANVAS_X, my
                        bs = BRUSH_SIZES[brush_key]
 
                        if current_tool == "eraser":
                            er = bs * 5
                            pygame.draw.rect(canvas, WHITE,
                                             (cx - er // 2, cy - er // 2, er, er))
                        elif current_tool not in ("pencil",):
                            # Shapes & line: commit on release
                            draw_shape(canvas, current_tool, current_color,
                                       start_pos[0], start_pos[1], cx, cy, bs)
 
                drawing = False
                start_pos = None
                prev_pos = None
 
            # ── Mouse motion ───────────────────────────────────────────────────
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    mx, my = event.pos
                    if mx >= CANVAS_X:
                        cx, cy = mx - CANVAS_X, my
                        bs = BRUSH_SIZES[brush_key]
 
                        if current_tool == "pencil":
                            if prev_pos:
                                pygame.draw.line(canvas, current_color,
                                                 prev_pos, (cx, cy), bs)
                            prev_pos = (cx, cy)
 
                        elif current_tool == "eraser":
                            er = bs * 5
                            pygame.draw.rect(canvas, WHITE,
                                             (cx - er // 2, cy - er // 2, er, er))
                            prev_pos = (cx, cy)
 
                        else:
                            prev_pos = (cx, cy)  # just track for preview
 
        # ── Render ────────────────────────────────────────────────────────────
        screen.fill(BG)
 
        # Draw canvas
        screen.blit(canvas, (CANVAS_X, 0))
 
        # Preview (for shape tools while dragging)
        if drawing and start_pos and prev_pos and current_tool not in ("pencil", "eraser"):
            bs = BRUSH_SIZES[brush_key]
            preview = canvas.copy()
            draw_shape(preview, current_tool, current_color,
                       start_pos[0], start_pos[1], prev_pos[0], prev_pos[1], bs)
            screen.blit(preview, (CANVAS_X, 0))
 
        # Text preview
        if text_mode and text_cursor:
            preview_canvas = canvas.copy()
            txt_surf = font_text.render(text_buffer + "|", True, current_color)
            preview_canvas.blit(txt_surf, text_cursor)
            screen.blit(preview_canvas, (CANVAS_X, 0))
 
        # Canvas border
        pygame.draw.rect(screen, (70, 70, 90), (CANVAS_X, 0, CANVAS_W, CANVAS_H), 2)
 
        # ── Toolbar ───────────────────────────────────────────────────────────
        # Tool buttons
        for rect, key in tool_buttons:
            draw_button(screen, rect, dict(TOOLS)[key], key == current_tool, font_sm)
 
        # Brush size header
        lbl = font_sm.render("Brush Size:", True, TEXT_COL)
        screen.blit(lbl, (pad, bsz_y - 16))
        for k, rect in bsz_rects.items():
            # show short label
            short = {1: "1", 2: "2", 3: "3"}[k]
            pygame.draw.rect(screen, SEL if k == brush_key else PANEL, rect, border_radius=5)
            pygame.draw.rect(screen, (70, 70, 90), rect, 1, border_radius=5)
            s = font_sm.render(short, True, TEXT_COL)
            screen.blit(s, s.get_rect(center=rect.center))
 
        # Brush preview line
        preview_y = bsz_y + 30
        pygame.draw.line(screen, current_color,
                         (pad, preview_y), (TOOLBAR_W - pad, preview_y),
                         BRUSH_SIZES[brush_key])
 
        # Palette
        pal_lbl = font_sm.render("Colors:", True, TEXT_COL)
        screen.blit(pal_lbl, (pad, pal_y - 16))
        for rect, col in swatches:
            pygame.draw.rect(screen, col, rect, border_radius=3)
            if col == current_color:
                pygame.draw.rect(screen, WHITE, rect, 2, border_radius=3)
 
        # Current color swatch
        cc_y = pal_y + 2 * (swatch_size + 2) + 8
        cc_rect = pygame.Rect(pad, cc_y, TOOLBAR_W - 16, 22)
        pygame.draw.rect(screen, current_color, cc_rect, border_radius=4)
        pygame.draw.rect(screen, WHITE, cc_rect, 1, border_radius=4)
 
        # Shortcuts hint
        hint_y = cc_y + 30
        hints = [
            "Shortcuts:",
            "P/L/R/Q/C/T", "E/D/F/X/A",
            "1/2/3 = size",
            "Ctrl+S = save",
        ]
        for i, h in enumerate(hints):
            hs = font_sm.render(h, True, (130, 130, 160))
            screen.blit(hs, (pad, hint_y + i * 15))
 
        # Status message
        if status_timer > 0:
            status_timer -= 1
            st = font_md.render(status_msg, True, (100, 230, 100))
            screen.blit(st, (CANVAS_X + 10, 8))
 
        # Text mode indicator
        if text_mode:
            tm = font_md.render("TEXT MODE — type, Enter to confirm, Esc to cancel",
                                 True, (255, 200, 60))
            screen.blit(tm, (CANVAS_X + 10, 8))
 
        pygame.display.flip()
 
    pygame.quit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()
