import pygame

from scripts.tiles.structures.structure import Structure, StructureIO

class Belt(Structure):
    def __init__(self, pos, size, img, rotation=0):
        super().__init__("belt", pos, StructureIO({(-1, 0): None}, {(1, 0): None}, self), size, img, build_speed=30, build_difficulty=3, solid=False, rotation=rotation)
        self.item = None

    def copy(self):
        return Belt(self.pos, self.size, self.animation, rotation=self.rotation)