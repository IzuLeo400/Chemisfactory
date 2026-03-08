import pygame

from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.tiles.sources import Source


def left_click(self):
        pass

def right_click(self):
    if issubclass(self.hover_tile.__class__, Source):
        if self.hover_tile.in_range(self.center_pose(), depth=1):
                self.action_trigger = "Mine"
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
        else:
            #Player clicked on source but was too far away
            pass

def middle_click(self):
    pass

def left_hold(self):
        pass

def right_hold(self):
    pass

def middle_hold(self):
    pass

def left_release(self):
        pass

def right_release(self):
    if self.action.m_name == "Mine":
        self.action_trigger = "Cancel"

def middle_release(self):
    pass