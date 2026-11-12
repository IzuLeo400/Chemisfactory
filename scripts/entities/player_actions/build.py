from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.entities.player_actions.progress_action import ProgressAction
from scripts.tiles.item import Item
from scripts.tiles.structures.structure import Structure
from scripts.ui_elements.uninteractable import unInteractable
from scripts.tiles.sources import Source
from scripts.exceptions.CustomErrors import StractureManagementError

class Build(ProgressAction):
    """
    The action of building structures

    :param player: the player preforming the action
    :param ui: The UI class for the whole game to make and destroy the ui elements accompanying the building
    """
    def __init__(self, player, ui):
        super().__init__(player, "Build", ui)
        
    
    def set_action_item(self, structure):
        self.structure = structure
        if structure != None:
            self.speed = structure.build_speed 
            self.difficulty = structure.build_difficulty 
            return True
        return False

    def start(self) -> bool:
        if self.structure != None:
            return super().start()
        else:
            self.end(True)
            return False
        

    def end(self, interrupted):
        if not interrupted:
            if self.structure != None:
                tilemap = self.m_entity.tilemap.tilemap
                if self.source != None:
                    self.structure.pos = self.location
                    if (self.source.add_miner(self.structure.copy())):
                        assert self.source.miner is not None
                        self.source.miner.update_io(tilemap)
                        self.ui.remove_item()
                        
                    else:
                        raise StractureManagementError("Failed to assign Structure to Source \n Possibly already a Structure on the Source")
                else:
                    #print(f"Building {self.structure.name} at {self.location}")
                    self.structure.pos = self.location
                    tilemap[self.location] = self.structure.copy()
                    tilemap[self.location].update_io(tilemap)
                    #print("position: ", self.location)
                    #print("inputs:", tilemap[self.location].io.inputs)
                    #print("outputs:", tilemap[self.location].io.outputs)
                    #print("connected: ", tilemap[self.location].io.connected)
                    self.ui.remove_item()
                self.m_entity.action_trigger = "Cancel"
                #Action Successful
                return super().end(False)
            else:
                raise StractureManagementError("Build action structure is None")
        else:
            #Action is interrupted through regular means
            return super().end(True)
        