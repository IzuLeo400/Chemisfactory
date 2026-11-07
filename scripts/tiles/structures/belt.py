import pygame

from scripts.tiles.structures.structure import Structure

class Belt(Structure):
    def __init__(self, pos, size, img, rotation=0):
        super().__init__("belt", pos, size, img, build_speed=30, build_difficulty=3, solid=False, rotation=rotation)

    def copy(self):
        return Belt(self.pos, self.size, self.animation, rotation=self.rotation)