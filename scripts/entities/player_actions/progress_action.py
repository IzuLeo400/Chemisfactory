from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.tiles.item import Item
from scripts.ui_elements.uninteractable import unInteractable
from scripts.ui_elements.window import Window

class ProgressAction(Action):
    def __init__(self, player, name, ui, speed=1, difficulty=5):
        super().__init__(player, name, self.start, self.update, self.end)
        self.ui = ui
        self.progressBar = None
        self.speed = speed
        self.difficulty = difficulty

    def start(self):
        self.progress = 0 #full bar is at source.difficulty, this is used to determine how long it takes to mine the source
        self.progressBar = unInteractable("progressBar", self.ui, self.ui.assets["ProgressBar"][self.m_name], 16,
                             (Constants.screen_width/4 - self.difficulty/2*16, Constants.screen_height/4 - 1/2*16 + Constants.progress_bar_y_offset), 
                             (self.difficulty, 1), is_open=True, border_color=(255, 225, 0))
        return True
        
    def update(self):
        #Update the uninteractable from here to make it seem like the player is doing something
        self.progress += self.speed / 60
        if self.progress >= self.difficulty:
            self.end(False)
        if self.progressBar.items[(int(self.progress), 0)].item is None:
            self.progressBar.items[(int(self.progress), 0)].item = Item("progressbar", (int(self.progress), 0), 16, self.ui.assets["ProgressBar"][self.m_name]["full"])

    def end(self, interrupted):
        if self.progressBar is not None:
            if interrupted:
                self.progressBar.delete()
                self.progressBar = None
                self.m_entity.action_trigger = "Cancel"
                return False
            else:
                self.progressBar.reset()
                self.progress = 0 
                return True
        else:
            self.m_entity.action_trigger = "Cancel"
            return False