import pygame

from scripts.constants import Constants
from scripts.tiles.sources import Source
from scripts.tiles.structures.miner import Miner
from scripts.tiles.structures.structure import Structure

def source_click(self, action):
    if issubclass(self.hover_tile.__class__, Source):
        if self.hover_tile.in_range(self.center_pose(), depth=1):
                if action == "Build" and (self.ui.manager.get_selected_item().__class__ != Miner or self.hover_tile.mining):
                    #Attempting to build a structure that is not a miner on a source || Attempting to build a miner on a source that is already being mined
                    return
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
        else:
            #Player clicked on source but was too far away
            pass

def off_source_build(self):
    item = self.ui.manager.get_selected_item()
    if item.__class__ == Miner:
        #Player is trying to build a miner off a source
        return
    if self.hover_tile != None and issubclass(self.hover_tile.__class__, Source):
        #Player is trying to build on a source
        return
    if self.hover_tile != None and issubclass(self.hover_tile.__class__, Structure):
        #Player is trying to build on another structure
        return
    if item != None and issubclass(item.__class__, Structure):
        #Actually start build action
        self.action_trigger = "Build"
        self.entity_actions["Build"].set_location(self.hover_pose)
        self.entity_actions["Build"].set_action_item(item)

def left_click(self):
    source_click(self, "Mine")

def right_click(self):
    source_click(self, "Build")
    off_source_build(self)
    
def middle_click(self):
    pass

def left_hold(self):
        pass

def right_hold(self):
    pass

def middle_hold(self):
    pass

def left_release(self):
    if self.action.m_name == "Mine":
        self.action_trigger = "Cancel"

def right_release(self):
    if self.action.m_name == "Build":
        self.action_trigger = "Cancel"

def middle_release(self):
    pass