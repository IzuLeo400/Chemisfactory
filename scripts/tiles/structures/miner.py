import pygame

from scripts.tiles.structures.structure import Structure

class Miner(Structure):
    def __init__(self, pos, size, img, source):
        super().__init__("miner", pos, size, img, source=source, solid=True)

    def copy(self):
        return Miner(self.pos, self.size, self.animation, self.source)