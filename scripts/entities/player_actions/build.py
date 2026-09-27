from typing import Literal

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
        self.source: Source | None = None
        self.structure: Structure | None = None
    
    def set_action_item(self, structure):
        self.structure = structure
        if structure != None:
            self.speed = structure.build_speed 
            self.difficulty = structure.build_difficulty 

    def start(self) -> bool:
        if self.structure != None:
            return super().start()
        else:
            self.end(True)
            return False
        
    def set_action_source(self, source):
        self.source = source

    def end(self, interrupted):
        if not interrupted:
            if self.source != None and self.structure != None:
                self.source.add_miner(self.structure.img)
                self.ui.remove_item()
            else:
                self.m_entity.action_trigger = "Cancel"
                return super().end(True)
        return super().end(True)
        