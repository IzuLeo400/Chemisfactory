from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.entities.player_actions.progress_action import ProgressAction
from scripts.tiles.item import Item
from scripts.ui_elements.uninteractable import unInteractable
from scripts.ui_elements.window import Window

class Mine(ProgressAction):
    """
    The action of mining any of the sources to collect resources

    :param player: the entity preforming the action, probably the player, it would be cool with enemies mining like in hollow knight
    :param ui: The UI class for the whole game to make and destroy the ui elements accompanying the mining
    """
    def __init__(self, player, ui):
        super().__init__(player, "Mine", ui)
        self.source = None

    def set_item(self, item):
        pass

    def set_source(self, source):
        self.source = source
        self.speed = source.mining_speed
        self.difficulty = source.difficulty

    def end(self, interrupted):
        if not interrupted:
            self.ui.add_item(self.source.item)
        super().end(interrupted)
        