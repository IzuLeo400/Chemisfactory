import pygame

from scripts.tiles.structures.structure import Structure

class Belt(Structure):
    def __init__(self, pos, size, img):
        super().__init__("belt", pos, size, img)
