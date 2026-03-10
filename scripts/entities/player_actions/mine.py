from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.tiles.item import Item
from scripts.ui_elements.uninteractable import unInteractable
from scripts.ui_elements.window import Window

class Mine(Action):
    """
    The action of mining any of the sources to collect resources

    :param player: the entity preforming the action, probably the player, it would be cool with enemies mining like in hollow knight
    :param ui: The UI class for the whole game to make and destroy the ui elements accompanying the mining
    :param source: The source being mined, this is used to determine the speed of mining and the resources gained
    """
    def __init__(self, player, ui):
        super().__init__(player, "Mine", self.start, self.update, self.end)
        self.ui = ui
        self.progressBar = None
        self.source = None

    def set_source(self, source):
        self.source = source
        
    def start(self):
        self.progress = 0 #full bar is at source.difficulty, this is used to determine how long it takes to mine the source
        self.progressBar = unInteractable("progressBar", self.ui, self.ui.assets["ProgressBar"], 16,
                             (Constants.screen_width/4 - self.source.difficulty/2*16, Constants.screen_height/4 - 1/2*16 + Constants.progress_bar_y_offset), 
                             (self.source.difficulty, 1), is_open=True, border_color=(255, 225, 0))
        
    def update(self):
        #Update the uninteractable from here to make it seem like the player is doing something
        self.progress += self.source.mining_speed / 60
        if self.progress >= self.source.difficulty:
            self.end(False)
        if self.progressBar.items[(int(self.progress), 0)].item is None:
            self.progressBar.items[(int(self.progress), 0)].item = Item("progressbar", (int(self.progress), 0), 16, self.ui.assets["ProgressBar"]["full"])

    def end(self, interrupted):
        if interrupted:
            self.progressBar.delete()
            self.progressBar = None
        else:
            self.ui.add_item(self.source.item)
            self.progressBar.reset()
            self.progress = 0
        