import pygame

class Tile:
    def __init__(self, pos, size, img, solid=True, rotation=0):
        self.pos = list(pos)
        self.size = size
        self.solid = solid
        self.img = img
        self.rotation = rotation

    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.rotate(self.img, self.rotation),
                                 (self.pos[0] * self.size - offset[0],
                                  self.pos[1] * self.size - offset[1]))
