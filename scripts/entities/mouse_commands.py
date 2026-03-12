import pygame

from scripts.constants import Constants
from scripts.tiles.sources import Source

def source_click(self, action):
    if issubclass(self.hover_tile.__class__, Source):
        if self.hover_tile.in_range(self.center_pose(), depth=1):
                self.action_trigger = action
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
                self.entity_actions[action].set_source(self.hover_tile)
                self.entity_actions[action].set_item(self.ui.manager.get_selected_item())
        else:
            #Player clicked on source but was too far away
            pass

def left_click(self):
    source_click(self, "Mine")

def right_click(self):
    source_click(self, "Build")
    
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