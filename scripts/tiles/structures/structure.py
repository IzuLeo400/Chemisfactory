import pygame

from scripts.exceptions.UninitiatedValueError import UninitiatedValueError
from scripts.tiles.item import Item
from scripts.tiles.tile import Tile

class Structure(Item):
    def __init__(self, name, pos=(None, None), size=16, animation=None, build_speed=1, build_difficulty=4, rotation=0, source=None, solid=True, structure_io=None):
        super().__init__(name, pos, size, animation, solid=solid, rotation=rotation)
        self.build_speed = build_speed
        self.build_difficulty = build_difficulty
        self.source = source
        self.structure_io = structure_io

    def render(self, surface, offset=(0, 0), tilemap=True):
        self.animation.update()
        if self.source is not None:
            self.source.render(surface, offset)
        if self.pos is not None:
            if tilemap:
                surface.blit(pygame.transform.rotate(self.animation.img(), self.rotation),
                                        (self.pos[0] * self.size - offset[0],
                                        self.pos[1] * self.size - offset[1]))     
                return
        else:
            raise UninitiatedValueError("Tile position is None, cannot render tile without a position.")
        
        super().render(surface, offset)

    def copy(self):
        return Structure(self.name, self.pos, self.size, self.animation, self.build_speed, self.build_difficulty, self.rotation, self.source, self.solid)

class StructureIO():
    def __init__(self, inputs: dict, outputs: dict):
        self.inputs = inputs
        self.outputs = outputs
        self.io = {"inputs": inputs, "outputs": outputs}
        #example io: {(x_offset, y_offset): tile, (x_offset2, y_offset2): tile2}

    def get_output_tiles(self):
        tiles = []
        for output in self.outputs:
            tiles.append(self.outputs[output])
        return tiles

    def get_input_tiles(self):
        tiles = []
        for input in self.inputs:
            tiles.append(self.inputs[input])
        return tiles

    def update_io_for_rotation(self, rotation):
        #x' = x * cos(r) - y * sin(r)
        #y' = x * sin(r) + y * cos(r)
        (x + math.cos(math.radians(r)) * self.tile_size, 
                                                                    y - math.sin(math.radians(r)) * self.tile_size)
        new_inputs = {}
        new_outputs = {}
        for input in self.inputs:
            new_input = self.rotate_offset(input, rotation)
            new_inputs[new_input] = self.inputs[input]
        for output in self.outputs:
            new_output = self.rotate_offset(output, rotation)
            new_outputs[new_output] = self.outputs[output]
        self.inputs = new_inputs
        self.outputs = new_outputs
        