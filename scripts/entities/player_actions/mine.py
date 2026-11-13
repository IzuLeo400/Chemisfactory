from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.entities.player_actions.progress_action import ProgressAction
from scripts.tiles.item import Item
from scripts.tiles.sources import Source
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
        self.source: Source | None = None

    def set_location(self, location):
        '''
        Sets the location of the source being mined, \n 
        Sets the speed and difficulty of the mining action associated with that source

        :param location: -- tuple(int, int) -- the location of the source on the tilemap

        :returns success: -- Boolean -- if the location is valid (is on the tilemap and has a source)
        '''
        if (super().set_location(location)):
            if self.source != None:
                self.speed = self.source.mining_speed
                self.difficulty = self.source.difficulty
                return True
        return False

    def end(self, interrupted) -> bool:
        '''
        Method called when ending the action \n
        If the action completed without interrupt it will give the player the atom item depending on the source they are mining from

        :param interrupted: -- Boolean -- whether the action is interrupted, like by moving

        :returns success: -- Boolean -- whether the whole action was successful
        '''
        if not interrupted:
            if self.source != None:
                self.ui.add_item(self.source.item)
            else:
                self.m_entity.action_trigger = "Cancel"
                return super().end(True)
        return super().end(interrupted)
        