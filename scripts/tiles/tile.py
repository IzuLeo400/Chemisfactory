import math

import pygame

from scripts.constants import Constants
from scripts.exceptions.UninitiatedValueError import UninitiatedValueError

class Tile:
    def __init__(self, pos, size, animation, solid=True, rotation=0):
        self.pos: tuple[int, int] | None = tuple(pos)
        self.size = size
        self.solid = solid
        self.animation = animation
        self.rotation = rotation

    def render(self, surface, offset=(0, 0)):
        self.animation.update()
        if self.pos is not None:
            surface.blit(pygame.transform.rotate(self.animation.img(), self.rotation),
                                    (self.pos[0] * self.size - offset[0],
                                    self.pos[1] * self.size - offset[1]))
        else:
            raise UninitiatedValueError("Tile position is None, cannot render tile without a position.")

    
    def in_range(self, pose, depth=1):
        return self.in_range_static(self.pos, pose, depth)

    @staticmethod
    def in_range_static(pos1, pos2, depth=1):
        x = pos1[0] * Constants.tile_size - pos2[0] + Constants.tile_size / 2
        y = pos1[1] * Constants.tile_size - pos2[1] + Constants.tile_size / 2
        if math.sqrt(x**2 + y**2) < depth * Constants.tile_size - 2:
            return True
        return False
