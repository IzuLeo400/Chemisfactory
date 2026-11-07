import pygame

from scripts.exceptions.UninitiatedValueError import UninitiatedValueError
from scripts.tiles.item import Item
from scripts.tiles.tile import Tile

class Structure(Item):
    def __init__(self, name, pos=(None, None), size=16, animation=None, build_speed=1, build_difficulty=4, rotation=0, source=None, solid=True):
        super().__init__(name, pos, size, animation, solid=solid, rotation=rotation)
        self.build_speed = build_speed
        self.build_difficulty = build_difficulty
        self.source = source

    def render(self, surface, offset=(0, 0), tilemap=True):
        if self.source is not None:
            self.source.render(surface, offset)
        if self.pos is not None:
            if tilemap:
                surface.blit(pygame.transform.rotate(self.animation.img(), self.rotation),
                                        (self.pos[0] * self.size - offset[0],
                                        self.pos[1] * self.size - offset[1]))     
                return
        else:
            raise UninitiatedValueError("Tile position is None, cannot render tile without a position.")
        
        super().render(surface, offset)