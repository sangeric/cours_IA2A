import pygame
import math

TILE_COLORS = {
    "-": (50, 50, 50),
    "plains": (124, 252, 0),
    "forest": (34, 139, 34),
    "mountain": (139, 137, 137),
    "water": (0, 191, 255),
    "sand": (237, 201, 175)
}

def hex_corner(cx, cy, size, i):
    angle_deg = 60 * i
    angle_rad = math.radians(angle_deg)
    return (cx + size * math.cos(angle_rad), cy + size * math.sin(angle_rad))

def draw_hexagone(map, surface, x, y, tile, highlight=False, personnage=False):
    size = map.getSize()
    h = math.sqrt(3) * size
    x_offset = x * 1.5 * size
    y_offset = y * h + (x % 2) * (h / 2)
    cx, cy = x_offset + size, y_offset + h / 2
    couleur = TILE_COLORS.get(tile.getName())
    points = [hex_corner(cx, cy, size, i) for i in range(6)]
    pygame.draw.polygon(surface, couleur, points)
    pygame.draw.polygon(surface, (0, 0, 0), points, 1)
    if highlight:
        pygame.draw.polygon(surface, (255, 0, 0), points, 3)
    if personnage:
        pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(cy)), int(size / 3))

def get_hex_from_pixel(map, px, py):
    size = map.getSize()
    col = int(px / (1.5 * size))
    row_offset = (col % 2) * (math.sqrt(3) * size / 2)
    row = int((py - row_offset) / (math.sqrt(3) * size))
    if 0 <= col < map.getWidth() and 0 <= row < map.getHeight():
        return col, row
    return None
