import math

import pygame

from scripts.exceptions.CustomErrors import UninitiatedValueError
from scripts.tiles.item import Item
from scripts.tiles.sources import Source
from scripts.tiles.tile import Tile


class StructureIO():
    def __init__(self, inputs: dict, outputs: dict, structure):
        self.inputs = inputs
        self.outputs = outputs
        self.io = {"inputs": inputs, "outputs": outputs}
        #example io: {(x_offset, y_offset): tile, (x_offset2, y_offset2): tile2}
        self.connected = False #True when all inputs and outputs exist and are connected
        self.m_structure: Structure = structure #Set in the creation of the Structure Class

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
        #x' = vx * cos(r) - vy * sin(r) + x
        #y' = vx * sin(r) + vy * cos(r) + y
        new_inputs = {}
        new_outputs = {}
        for input in self.io["inputs"]:
            new_input = (self.fix_trig(input[0] * math.cos(math.radians(rotation)) - input[1] * math.sin(math.radians(rotation))), 
                         self.fix_trig(- input[0] * math.sin(math.radians(rotation)) + input[1] * math.cos(math.radians(rotation))))
            new_inputs[new_input] = None
        for output in self.io["outputs"]:
            new_output = (self.fix_trig(output[0] * math.cos(math.radians(rotation)) - output[1] * math.sin(math.radians(rotation))), 
                          self.fix_trig(- output[0] * math.sin(math.radians(rotation)) + output[1] * math.cos(math.radians(rotation))))
            new_outputs[new_output] = None
        self.inputs = new_inputs
        self.outputs = new_outputs
        print("new inputs", new_inputs)
        print("new outputs", new_outputs)

    def fix_trig(self, value):
        if (abs(value) < 0.1):
            return 0
        return value

    def update_positions(self, pos, tilemap, update_neighbors=True):
        for input in self.inputs:
            input_pos = (input[0] + pos[0], input[1] + pos[1])
            #print("input", input) print("pos", pos) print("input pos: ", input_pos)
            if input_pos in tilemap:
                self.inputs[input] = tilemap[input_pos]
                if update_neighbors:
                    if issubclass(tilemap[input_pos].__class__, Structure):
                        self.inputs[input].update_io(tilemap, False)
                        #print(f"updating tile @ {input_pos}, its new output is {self.inputs[input].update_io(tilemap, False)}")
                    elif issubclass(tilemap[input_pos].__class__, Source) and tilemap[input_pos].miner != None:
                        self.inputs[input].miner.update_io(tilemap, False)
                        #print(f"updating tile @ {input_pos}, its new output is {self.inputs[input].miner.update_io(tilemap, False)}")
                
        for output in self.outputs:
            output_pos = (output[0] + pos[0], output[1] + pos[1])
            #print("output pos: ", output_pos)
            if output_pos in tilemap:
                self.outputs[output] = tilemap[output_pos]
                if update_neighbors:
                    if issubclass(tilemap[output_pos].__class__, Structure):
                        self.outputs[output].update_io(tilemap, False)

        self.update_connection()

    def update_connection(self):
        for input in self.inputs:
            if self.inputs[input] == None:
                #print("input is null")
                self.connected = False
                return False
            if issubclass(self.inputs[input].__class__, Source):
                structure = self.inputs[input].miner
            else:
                structure = self.inputs[input]
            if structure == None:
                self.connected = False
                return False
            if (-input[0], -input[1]) not in structure.io.outputs or structure.io.outputs[(-input[0], -input[1])] != self.m_structure:
                self.connected = False
                return False

        for output in self.outputs:
            if self.outputs[output] == None or issubclass(self.outputs[output].__class__, Source):
                self.connected = False
                return False
            else:
                structure = self.outputs[output]
            if (-output[0], -output[1]) in structure.io.inputs:
                tile = structure.io.inputs[(-output[0], -output[1])]
                if (issubclass(tile.__class__, Source) or tile != self.m_structure):
                    self.connected = False
                    return False
            else:
                self.connected = False
                return False

        self.connected = True
        return True

    def copy(self):
        return StructureIO(self.io["inputs"], self.io["outputs"], self.m_structure)
    
class Structure(Item):
    def __init__(self, name, pos, io, size=16, animation=None, build_speed=1, build_difficulty=4, rotation=0, source=None, solid=True):
        super().__init__(name, pos, size, animation, solid=solid, rotation=rotation)
        self.build_speed = build_speed
        self.build_difficulty = build_difficulty
        self.source = source
        self.io: StructureIO = io

    def render(self, surface, offset=(0, 0), img=None, tilemap=True, debug=False):
        self.animation.update()
        if self.source is not None:
            self.source.render(surface, offset)
            if (debug and self.pos != None):
                pygame.draw.rect(surface, (0, 200, 0) if self.io.connected else (200, 0, 0), 
                pygame.Rect((self.pos[0] * self.size - offset[0], self.pos[1] * self.size - offset[1]), (4, 4)))
        if self.pos != None:
            if tilemap:
                pos = (self.pos[0] * self.size - offset[0],
                        self.pos[1] * self.size - offset[1])
                surface.blit(pygame.transform.rotate(self.animation.img(), self.rotation), pos)   
                if (debug):
                    pygame.draw.rect(surface, (0, 200, 0) if self.io.connected else (200, 0, 0), pygame.Rect(pos, (4, 4)))
                
                return
        else:
            raise UninitiatedValueError("Tile position is None, cannot render tile without a position.")
        
        super().render(surface, offset)

    def update_io(self, tilemap, update_neighbors=True):
        self.io.update_rotation(self.rotation)
        self.io.update_positions(self.pos, tilemap, update_neighbors) 
        return self.io.outputs

    def copy(self):
        return Structure(self.name, self.pos, self.io.copy(), self.size, self.animation, self.build_speed, self.build_difficulty, self.rotation, self.source, self.solid)

            
            
        