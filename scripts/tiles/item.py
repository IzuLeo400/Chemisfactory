from scripts.tiles.tile import Tile

class Item(Tile):
    def __init__(self, name,pos, size, img):
        super().__init__(pos, size, img)
        self.name = name

    def render(self, surface, offset=(0, 0), tilemap=False):
        surface.blit(self.img, (offset[0], offset[1]))