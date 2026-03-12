from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.entities.player_actions.progress_action import ProgressAction
from scripts.tiles.item import Item
from scripts.ui_elements.uninteractable import unInteractable
from scripts.ui_elements.window import Window

class Build(ProgressAction):
    """
    The action of building structures

    :param player: the player preforming the action
    :param ui: The UI class for the whole game to make and destroy the ui elements accompanying the building
    """
    def __init__(self, player, ui):
        super().__init__(player, "Build", ui)
        self.source = None
        self.structure = None
    
    def set_item(self, structure):
        self.structure = structure
        if structure is not None:
            self.speed = structure.build_speed 
            self.difficulty = structure.build_difficulty 

    def start(self):
        if self.structure is not None:
            return super().start()
        else:
            self.end(True)
            return False
        
    def set_source(self, source):
        self.source = source

    def end(self, interrupted):
        if not interrupted:
            self.source.add_miner(self.structure.img)
            self.ui.remove_item()
            if self.ui.manager.get_selected_item() is None:
                return super().end(True)
        return super().end(interrupted)
        