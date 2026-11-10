import math

import pygame

from scripts.exceptions.CustomErrors import UninitiatedValueError
from scripts.tiles.item import Item
from scripts.tiles.sources import Source
from scripts.tiles.tile import Tile


class StructureIO():
    def __init__(self, inputs: dict, outputs: dict):
        self.inputs = inputs
        self.outputs = outputs
        self.io = {"inputs": inputs, "outputs": outputs}
        #example io: {(x_offset, y_offset): tile, (x_offset2, y_offset2): tile2}
        self.connected = False #True when all inputs and outputs exist and are connected

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

    def update_rotation(self, rotation):
        #x' = x * cos(r) - y * sin(r)
        #y' = x * sin(r) + y * cos(r)
        new_inputs = {}
        new_outputs = {}
        for input in self.io["inputs"]:
            new_input = (input[0] * math.cos(math.radians(rotation)) - input[1] * math.sin(math.radians(rotation)), 
                         input[0] * math.sin(math.radians(rotation)) + input[1] * math.cos(math.radians(rotation)))
            new_inputs[new_input] = None
        for output in self.io["outputs"]:
            new_output = (output[0] * math.cos(math.radians(rotation)) -output[1] * math.sin(math.radians(rotation)), 
                          output[0] * math.sin(math.radians(rotation)) + output[1] * math.cos(math.radians(rotation)))
            new_outputs[new_output] = None
        self.inputs = new_inputs
        self.outputs = new_outputs

    def update_positions(self, pos, tilemap, update_neighbors=True):
        for input in self.inputs:
            input_pos = (input[0] + pos[1], input[1] + pos[1])
            if input_pos in tilemap and (issubclass(tilemap[input_pos].__class__, Structure) or (issubclass(tilemap[input_pos].__class__, Source) and tilemap[input_pos].miner != None)):
                self.inputs[input] = tilemap[input_pos]
                if update_neighbors:
                    self.inputs[input].update_io(tilemap, False)
        for output in self.outputs:
            output_pos = (output[0] + pos[1], output[1] + pos[1])
            if output_pos in tilemap and (issubclass(tilemap[output_pos].__class__, Structure) or (issubclass(tilemap[output_pos].__class__, Source) and tilemap[output_pos].miner != None)):
                self.outputs[output] = tilemap[output_pos]
                if update_neighbors:
                    self.outputs[output].update_io(tilemap, False)

    def update_connection(self):
        for input in self.inputs:
            if self.inputs[input] == None:
                self.connected = False
                return False
            if issubclass(self.inputs[input].__class__, Source):
                structure = self.inputs[input].miner
            else:
                structure = self.inputs[input]
            if (-input[0], -input[1]) not in structure.io.outputs or structure.io.outputs[(-input[0], -input[1])] != self:
                self.connected = False
                return False

        for output in self.outputs:
            if self.outputs[output] == None or issubclass(self.outputs[output].__class__, Source):
                self.connected = False
                return False
            else:
                structure = self.outputs[output]
            if (-output[0], -output[1]) not in structure.io.inputs or structure.io.inputs[(-output[0], -output[1])].io is not self:
                self.connected = False
                return False

        self.connected = True
        return True

    
class Structure(Item):
    def __init__(self, name, pos=(None, None), size=16, animation=None, build_speed=1, build_difficulty=4, rotation=0, source=None, solid=True, io=StructureIO(inputs={}, outputs={})):
        super().__init__(name, pos, size, animation, solid=solid, rotation=rotation)
        self.build_speed = build_speed
        self.build_difficulty = build_difficulty
        self.source = source
        self.io = io

    def render(self, surface, offset=(0, 0), img=None, tilemap=True):
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

    def update_io(self, tilemap, update_neighbors=True):
        self.io.update_rotation(self.rotation)
        self.io.update_positions(self.pos, tilemap, update_neighbors)
        self.io.update_connection()

    def copy(self):
        return Structure(self.name, self.pos, self.size, self.animation, self.build_speed, self.build_difficulty, self.rotation, self.source, self.solid)

            
            
        