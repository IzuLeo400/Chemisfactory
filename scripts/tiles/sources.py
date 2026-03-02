import math
import pygame
from scripts.constants import Constants
from scripts.tiles.tile import Tile

class Source(Tile):
    def __init__(self, pos, size, img, solid):
        super().__init__(pos, size, img, solid)
        self.mining = False

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
        #surface.blit(pygame.Surface((4, 4)), (self.pos[0] * self.size + Constants.tile_size / 2 - 2 - offset[0], self.pos[1] * self.size + Constants.tile_size / 2 - 2 - offset[1]))
        super().render(surface, offset)

class Hydrogen(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=False)

class Oxygen(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=False)

class Iron(Source):
    def __init__(self, pos, img, size=16):
        super().__init__(pos, size, img, solid=True)