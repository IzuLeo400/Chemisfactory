from scripts.tiles.tile import Tile

class Item(Tile):
    def __init__(self, name, pos=(None, None), size=16, img=None, solid=False, rotation=0):
        super().__init__(pos, size, img, solid, rotation)
        self.name = name

    def render(self, surface, offset=(0, 0), tilemap=False):
        surface.blit(self.img, (offset[0], offset[1]))