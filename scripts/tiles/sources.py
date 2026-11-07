import math

import pygame
from scripts.constants import Constants
from scripts.exceptions.UninitiatedValueError import UninitiatedValueError
from scripts.sprites import Animation
from scripts.tiles.item import Item
from scripts.tiles.tile import Tile

class Source(Tile):
    """
    Initialize a source tile.

    :param pos: -- Tuple (x, y) -- The position of the source tile on the tilemap
    :param size: -- int -- The size of the source tile.
    :param img: -- pygame.Surface -- The image for the source tile.
    :param solid: -- bool -- Whether the tile has collisions
    :param mining_speed: -- float -- The speed at which the progress bar fills up, this is in tiles per second
    :param difficulty: -- int -- The size of the progress bar in tiles, this is used to determine how long it takes to mine the source, the higher the difficulty, the longer it takes to mine
    """
    def __init__(self, pos, size, img, solid=True, mining_speed=1, difficulty=5, item=None):
        super().__init__(pos, size, img, solid)
        self.mining = False
        self.mining_rotation = 0
        self.mining_speed = mining_speed
        self.difficulty = difficulty
        self.item = item

    def add_miner(self, structure):
        self.mining_rotation = structure.rotation
        self.animation.blit(pygame.transform.rotate(structure.animation.img(), self.mining_rotation), (0, 0))
        self.mining = True
    
    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset)

class Hydrogen(Source):
    def __init__(self, pos, img, size, game):
        super().__init__(pos, size, img, solid=False, mining_speed=2, difficulty=3, item=Item("Hydrogen", animation=game.assets["Items"]["Hydrogen"]))

class Oxygen(Source):
    def __init__(self, pos, img, size, game):
        super().__init__(pos, size, img, solid=False, mining_speed=3, difficulty=5, item=Item("Oxygen", animation=game.assets["Items"]["Oxygen"]))
class Iron(Source):
    def __init__(self, pos, img, size, game):
        super().__init__(pos, size, img, solid=True, mining_speed=1, difficulty=7, item=Item("Iron", animation=game.assets["Items"]["Iron"]))