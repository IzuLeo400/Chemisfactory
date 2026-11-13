from scripts.constants import Constants
from scripts.entities.action import Action
from scripts.tiles.item import Item
from scripts.tiles.sources import Source
from scripts.tiles.structures.structure import Structure
from scripts.ui_elements.uninteractable import unInteractable
from scripts.ui_elements.window import Window

class ProgressAction(Action):
    '''
    The abstract class for an action that requires a progress bar \n
    progress bar is a rectangle at the bottom of the screen that fills up with squares 

    :param player: -- Player -- the player performing the action
    :param name: -- String -- the name of the action for identification purposes
    :param ui: -- UI -- the ui class for the game to create and destroy ui elements
    :param speed: -- int -- default = 1 -- the speed of the action 
    (one square per speed/60 frames, so speed of 1 is 1 square per second)
    :param difficulty: -- int -- default = 5 -- the amount of squares needed to be filled up to complete the action (size of progress bar)
    '''
    def __init__(self, player, name, ui, speed=1, difficulty=5):
        super().__init__(player, name, self.start, self.update, self.end)
        self.ui = ui
        self.progressBar = None
        self.speed = speed
        self.difficulty = difficulty
        self.source: Source | None = None
        self.structure: Structure | None = None
        self.location: tuple[int, int] | None = None

    def set_location(self, location):
        '''
        sets the location of the action

        :param location: -- tuple(int, int) -- the location on the tilemap that the action is happening (the location of the tile being interacted with)
        '''
        self.location = location
        if location in self.m_entity.tilemap.tilemap:
            tile = self.m_entity.tilemap.tilemap[location]
            if issubclass(tile.__class__, Source):
                self.source = tile
                return True
        self.source = None
        return False

    def set_action_item(self, structure) -> bool:
        '''
        sets the item being used or interacted with in the action \n
        the super method returns True no matter what so you don't have to override it if not necessary
        
        :param structure: -- Structure -- the structure being built or deconstructed or otherwise interacted with

        :return success: -- Boolean -- whether or not successfully set the item \n
        possible fails (return False): there already is an item set or the item given is null
        '''
        return True

    def start(self) -> bool:
        '''
        Called when the action is initialized \n
        Creates a new progress bar

        :return success: -- Boolean -- whether action was successful
        '''
        self.progress = 0 #full bar is at source.difficulty, this is used to determine how long it takes to mine the source
        self.progressBar = unInteractable("progressBar", self.ui, self.ui.assets["ProgressBar"][self.m_name], 16,
                             (Constants.screen_width/4 - self.difficulty/2*16, Constants.screen_height/4 - 1/2*16 + Constants.progress_bar_y_offset), 
                             (self.difficulty, 1), is_open=True, border_color=(255, 225, 0))
        return True
        
    def update(self) -> bool:
        '''
        Update the uninteractable (progress bar) to make it seem like the player is doing something \n

        :return success: -- Boolean -- whether the update succeded
        '''
        self.progress += self.speed / 60
        if self.progress >= self.difficulty:
            return self.end(False)
        elif self.progressBar != None:
            if self.progressBar.items[(int(self.progress), 0)].item == None:
                self.progressBar.items[(int(self.progress), 0)].item = Item("progressbar", (int(self.progress), 0), 16, self.ui.assets["ProgressBar"][self.m_name]["full"])
            return True
        else:
            self.m_entity.action_trigger = "Cancel"
            return self.end(True)
        

    def end(self, interrupted) -> bool:
        '''
        Called at the end the action, whether successful or not

        :param interrupted: -- Boolean -- whether the action was interrupted, like by moving 

        :return success: --Boolean -- whether the whole action succeded
        '''
        if self.progressBar != None:
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