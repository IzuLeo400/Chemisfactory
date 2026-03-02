import pygame
from scripts.tiles.sources import *

NEIGHBOR_OFFSETS = {1: [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0),(-1, 1), (0, 1), (1, 1)],
                    2: [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2), (-1, -2)]}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        self.tilemap[(-2, -3)] = Hydrogen((-2, -3), self.game.assets["Sources"]["HydrogenSource"], self.tile_size)
        self.tilemap[(-4, -1)] = Oxygen((-4, -1), self.game.assets["Sources"]["OxygenSource"], self.tile_size)
        self.tilemap[(3, 4)] = Iron((3, 4), self.game.assets["Sources"]["IronSource"], self.tile_size)

    def point_to_loc(self, pos):
        return (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

    def loc_to_point(self, loc):
        return (loc[0] * self.tile_size, loc[1] * self.tile_size)

    def tiles_around(self, pos, depth):
        tiles = []
        tile_loc = self.point_to_loc(pos)
        for idx in range(1, depth+1):
            for offset in NEIGHBOR_OFFSETS[idx]:
                check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
                if check_loc in self.tilemap:
                    tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos, depth):
        rects = []
        for tile in self.tiles_around(pos, depth):
            if tile.solid:
                rects.append(
                    pygame.Rect(tile.pos[0] * self.tile_size,
                                tile.pos[1] * self.tile_size, self.tile_size,
                                self.tile_size))
        return rects

    def render(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size,
                       (offset[0] + surface.get_width()) // self.tile_size +
                       1):
            for y in range(
                    offset[1] // self.tile_size,
                (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = (x, y)
                if location in self.tilemap:
                    self.tilemap[(x, y)].render(surface, offset)
                    