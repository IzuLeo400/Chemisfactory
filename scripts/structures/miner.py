import pygame
from scripts.structures.structure import Structure


class Miner(Structure):
    def __init__(self, pos, size, img, source):
        super().__init__(pos, size, img)
        self.source = source


    def render(self, surface, offset=(0, 0), tilemap=True):
        if self.source is not None:
            self.source.render(surface, offset)
        if tilemap:
            surface.blit(pygame.transform.rotate(self.img, self.rotation),
                                    (self.pos[0] * self.size - offset[0],
                                    self.pos[1] * self.size - offset[1]))     
        else:
            surface.blit(self.img, (offset[0], offset[1]))
