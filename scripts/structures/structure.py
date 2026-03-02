from scripts.tiles.tile import Tile

class Structure(Tile):
    def __init__(self, pos, size, img, rotation=0):
        super().__init__(pos, size, img, solid=True, rotation=rotation)