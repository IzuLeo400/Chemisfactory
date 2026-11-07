import pygame

from scripts.exceptions.UninitiatedValueError import UninitiatedValueError

class Tile:
    def __init__(self, pos, size, animation, solid=True, rotation=0):
        self.pos: tuple[int, int] | None = tuple(pos)
        self.size = size
        self.solid = solid
        self.animation = animation
        self.rotation = rotation

    def render(self, surface, offset=(0, 0)):
        if self.pos is not None:
            surface.blit(pygame.transform.rotate(self.animation.img(), self.rotation),
                                    (self.pos[0] * self.size - offset[0],
                                    self.pos[1] * self.size - offset[1]))
        else:
            raise UninitiatedValueError("Tile position is None, cannot render tile without a position.")
