import pygame

from scripts.tiles.structures.structure import Structure, StructureIO

class Miner(Structure):
    def __init__(self, pos, size, img, build_speed=1, build_difficulty=4, rotation=0, source=None, solid=True):
        super().__init__("miner", pos, StructureIO({}, {(1, 0): None}, self), size, img, build_speed=build_speed, build_difficulty=build_difficulty, rotation=rotation, source=source, solid=solid)

    def copy(self):
        return Miner(self.pos, self.size, self.animation, build_speed=self.build_speed, build_difficulty=self.build_difficulty, rotation=self.rotation, source=self.source, solid=self.solid)