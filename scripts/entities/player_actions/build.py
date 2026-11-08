from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.entities.player_actions.progress_action import ProgressAction
from scripts.tiles.item import Item
from scripts.tiles.structures.structure import Structure
from scripts.ui_elements.uninteractable import unInteractable
from scripts.tiles.sources import Source

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
                if self.source != None:
                    self.source.add_miner(self.structure)
                    self.ui.remove_item()
                elif self.structure != None:
                    #print(f"Building {self.structure.name} at {self.location}")
                    self.structure.pos = self.location
                    self.m_entity.tilemap.tilemap[(self.location)] = self.structure.copy()
                    self.ui.remove_item()
                else:
                    return super().end(True)
                self.m_entity.action_trigger = "Cancel"
                return super().end(False)
            else:
                self.m_entity.action_trigger = "Cancel"
                return super().end(True)
        else:
            return super().end(True)
        