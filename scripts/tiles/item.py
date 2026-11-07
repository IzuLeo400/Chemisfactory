from scripts.tiles.tile import Tile

class Item(Tile):
    def __init__(self, name, pos=(None, None), size=16, animation=None, solid=False, rotation=0):
        super().__init__(pos, size, animation, solid, rotation)
        self.name = name

    def render(self, surface, offset=(0, 0), tilemap=False):
        surface.blit(self.animation.img(), (offset[0], offset[1]))

    def rotate(self):
        self.rotation = (self.rotation - 90) % 360
