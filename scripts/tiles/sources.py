import math
import pygame
from scripts.constants import Constants
from scripts.tiles.tile import Tile

class Source(Tile):
    """
    Initialize a source tile.

    :param pos: -- Tuple (x, y) -- The position of the source tile on the tilemap
    :param size: -- int -- The size of the source tile.
    :param img: -- pygame.Surface -- The image for the source tile.
    :param solid: -- bool -- Whether the tile has collisions
    :param mining_speed: -- float -- The speed at which the progress bar fills up, this is in tiles per second
    :param difficulty: -- int -- The size of the progress bar in tiles, this is used to determine how long it takes to mine the source, the higher the difficulty, the longer it takes to mine
    """
    def __init__(self, pos, size, img, solid=True, mining_speed=1, difficulty=5):
        super().__init__(pos, size, img, solid)
        self.mining = False
        self.mining_speed = mining_speed
        self.difficulty = difficulty

    def add_miner(self, img):
        self.img.blit(img, (0, 0))
        self.mining = True

    def in_range(self, pose, depth=1):
        x = self.pos[0] * self.size - pose[0] + Constants.tile_size / 2 
        y = self.pos[1] * self.size - pose[1] + Constants.tile_size / 2 
        if math.sqrt(x**2 + y**2) < depth * Constants.tile_size - 2:
            return True
        return False
    
    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset)

class Hydrogen(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=False, mining_speed=2, difficulty=3)

class Oxygen(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=False, mining_speed=3, difficulty=5)

class Iron(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=True, mining_speed=1, difficulty=7)