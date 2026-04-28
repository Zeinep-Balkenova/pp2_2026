"""
tools.py — Drawing tool implementations for TSIS2 Paint App
"""
 
import pygame
from collections import deque
 
 
# ── Brush sizes ──────────────────────────────────────────────────────────────
BRUSH_SIZES = {1: 2, 2: 5, 3: 10}   # key → shortcut digit, value → px width
 
 
# ── Flood fill (bucket) ───────────────────────────────────────────────────────
def flood_fill(surface: pygame.Surface, x: int, y: int, fill_color: tuple):
    """BFS flood fill on *surface* starting at (x, y) with *fill_color*."""
    width, height = surface.get_size()
 
    # Clamp click to canvas
    if not (0 <= x < width and 0 <= y < height):
        return
 
    target_color = surface.get_at((x, y))[:3]   # ignore alpha
    fill_rgb = fill_color[:3]
 
    if target_color == fill_rgb:
        return  # nothing to do
 
    visited = [[False] * height for _ in range(width)]
    queue = deque()
    queue.append((x, y))
    visited[x][y] = True
 
    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill_color)
 
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < width and 0 <= ny < height
                    and not visited[nx][ny]
                    and surface.get_at((nx, ny))[:3] == target_color):
                visited[nx][ny] = True
                queue.append((nx, ny))
 
 
# ── Shape drawing helpers ─────────────────────────────────────────────────────
def draw_right_triangle(surface, color, x1, y1, x2, y2, width):
    """Right-angle triangle: right angle at bottom-left."""
    points = [(x1, y2), (x1, y1), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)
 
 
def draw_equilateral_triangle(surface, color, x1, y1, x2, y2, width):
    """Equilateral triangle fitted inside the drag rectangle."""
    cx = (x1 + x2) / 2
    points = [(cx, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)
 
 
def draw_diamond(surface, color, x1, y1, x2, y2, width):
    """Diamond (rhombus) fitted inside the drag rectangle."""
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, points, width)
 
 
def draw_square(surface, color, x1, y1, x2, y2, width):
    """Force equal sides based on the shorter drag dimension."""
    side = min(abs(x2 - x1), abs(y2 - y1))
    sx = x1 if x2 > x1 else x1 - side
    sy = y1 if y2 > y1 else y1 - side
    pygame.draw.rect(surface, color, (sx, sy, side, side), width)
 
 
# ── Generic shape dispatcher ──────────────────────────────────────────────────
def draw_shape(surface, tool, color, x1, y1, x2, y2, brush_size):
    w = brush_size  # outline width (0 = filled)
 
    if tool == "rect":
        rx, ry = min(x1, x2), min(y1, y2)
        rw, rh = abs(x2 - x1), abs(y2 - y1)
        pygame.draw.rect(surface, color, (rx, ry, rw, rh), w)
 
    elif tool == "square":
        draw_square(surface, color, x1, y1, x2, y2, w)
 
    elif tool == "circle":
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        rx, ry = abs(x2 - x1) // 2, abs(y2 - y1) // 2
        r = max(rx, ry, 1)
        pygame.draw.circle(surface, color, (cx, cy), r, w)
 
    elif tool == "right_tri":
        draw_right_triangle(surface, color, x1, y1, x2, y2, w)
 
    elif tool == "eq_tri":
        draw_equilateral_triangle(surface, color, x1, y1, x2, y2, w)
 
    elif tool == "diamond":
        draw_diamond(surface, color, x1, y1, x2, y2, w)
 
    elif tool == "line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), w)
