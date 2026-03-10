import pygame

from scripts.tiles.item import Item
from scripts.tiles.tile import Tile

class Structure(Item):
    def __init__(self, name, pos=(None, None), size=16, img=None, rotation=0):
        super().__init__(name, pos, size, img, solid=True, rotation=rotation)

    def render(self, surface, offset=(0, 0), tilemap=True):
        if self.source is not None:
            self.source.render(surface, offset)
        if tilemap:
            surface.blit(pygame.transform.rotate(self.img, self.rotation),
                                    (self.pos[0] * self.size - offset[0],
                                    self.pos[1] * self.size - offset[1]))     
        else:
            super().render(surface, offset)