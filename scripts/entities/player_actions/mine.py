from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.ui_elements.window import Window

class Mine(Action):
    """
    The action of mining any of the sources to collect resources

    :param player: the entity preforming the action, probably the player though it would be cool to have enemies mining like in hollow knight
    :param ui: The UI class for the whole game to make and destroy the ui elements accompanying the mining
    """
    def __init__(self, player, ui):
        super.__init__(player, "Mine", self.start, self.update, self.end)
        self.ui = ui
        self.progressBar = None
        
        
    def start(self):
        self.progressBar = Window("progressBar", self.ui, self.ui.assets["ProgressBar"], 
                             (Constants.screen_width/4 - Constants.progress_bar_width/2, Constants.screen_height/2), 
                             (Constants.progress_bar_width, Constants.progress_bar_height), is_open=True, border_color=(255, 225, 0))
        
    def update(self):
        pass

    def end(self, interrupted):
        self.progressBar.delete()
        self.progressBar = None
        if not interrupted:
            pass
        