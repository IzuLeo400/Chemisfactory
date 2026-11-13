import pygame

from scripts.constants import Constants
from scripts.tiles.sources import Source
from scripts.tiles.structures.miner import Miner
from scripts.tiles.structures.structure import Structure
from scripts.tiles.tile import Tile

def source_click(self, action) -> bool:
    if issubclass(self.hover_tile.__class__, Source):
        if self.hover_tile.in_range(self.center_pose(), depth=1):
                if (action == "Build" and (self.ui.manager.get_selected_item().__class__ != Miner) or (self.hover_tile.mining and action != "Deconstruct")) or (action == "Deconstruct" and not self.hover_tile.mining):
                    #Attempting to build a structure that is not a miner on a source || Attempting to build a miner on a source that is already being mined || Attempting to deconstruct a source that is not being mined
                    return False
                self.action_trigger = action

                #Have the playe look at the source to increase realism
                offset = (self.pos[0] - self.hover_tile.pos[0] * Constants.tile_size - 5, self.pos[1] - self.hover_tile.pos[1] * Constants.tile_size - 5)
                if abs(offset[0]) > abs(offset[1]):
                    if offset[0] > 0:
                        self.direction = "a"
                    else:
                        self.direction = "d"
                else:
                    if offset[1] > 0:
                        self.direction = "w"
                    else:
                        self.direction = "s"
                        
                self.entity_actions[action].set_location(self.hover_pose)
                self.entity_actions[action].set_action_item(self.ui.manager.get_selected_item())
                #print(f"Starting {action} action on {self.hover_tile} at {self.hover_pose}")
                return True
        else:
            #Out of range to build or mine
            pass
    return False

def off_source_build(self) -> bool:
    item = self.ui.manager.get_selected_item()
    if not Tile.in_range_static(self.hover_pose, self.center_pose(), depth=2):
        #Out of range to build
        return False
    if item.__class__ == Miner:
        #Player is trying to build a miner off a source
        return False
    if self.hover_tile != None and issubclass(self.hover_tile.__class__, Source):
        #Player is trying to build on a source
        return False
    if self.hover_tile != None and issubclass(self.hover_tile.__class__, Structure):
        #Player is trying to build on another structure
        return False
    if item != None and issubclass(item.__class__, Structure):
        #Actually start build action
        self.action_trigger = "Build"
        self.entity_actions["Build"].set_location(self.hover_pose)
        self.entity_actions["Build"].set_action_item(item)
        return True
    return False

def off_source_deconstruct(self) -> bool:
    if not Tile.in_range_static(self.hover_pose, self.center_pose(), depth=2):
        #Out of range to deconstruct
        return False
    if self.hover_tile != None and issubclass(self.hover_tile.__class__, Structure):
        #Actually start deconstruct action
        self.action_trigger = "Deconstruct"
        self.entity_actions["Deconstruct"].set_location(self.hover_pose)
        self.entity_actions["Deconstruct"].set_action_item(self.hover_tile)
        return True
    return False

def left_click(self) -> bool:
    '''
    runnable method by the player when a left click occurs (off ui)

    handles mining and deconstruction (both on and off source)
    '''
    if (source_click(self, "Deconstruct")):
        return True
    if (source_click(self, "Mine")):
        return True
    if (off_source_deconstruct(self)):
        return True
    return False

def right_click(self) -> bool:
    if (source_click(self, "Build")):
        return True
    if (off_source_build(self)):
        return True
    return False
    
def middle_click(self):
    pass

def left_hold(self):
        pass

def right_hold(self):
    pass

def middle_hold(self):
    pass

def left_release(self):
    if self.action.m_name == "Mine" or self.action.m_name == "Deconstruct":
        self.action_trigger = "Cancel"

def right_release(self):
    if self.action.m_name == "Build":
        self.action_trigger = "Cancel"

def middle_release(self):
    pass