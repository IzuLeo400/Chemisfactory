import pygame

from scripts.tiles.structures.structure import Structure, StructureIO

class Belt(Structure):
    def __init__(self, pos, size, img, rotation=0):
        super().__init__("belt", pos, size, img, build_speed=30, build_difficulty=3, solid=False, rotation=rotation, io=StructureIO(inputs={(-1, 0): None}, outputs={(1, 0): None}))
        self.item = None

    def copy(self):
        return Belt(self.pos, self.size, self.animation, rotation=self.rotation)