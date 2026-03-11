import math
import pygame

from scripts.constants import Constants
from scripts.entities import mouse_commands
from scripts.entities.action import Action
from scripts.entities.player_actions.build import Build
from scripts.entities.player_actions.mine import Mine
from scripts.tiles.sources import Source
from scripts.entities.entity import PhysicsEntity
from scripts.ui_elements.window import Window

class Player(PhysicsEntity):
    """
    The playable entity in the game 

    :param game: -- Game -- The actual main class controlling the entire game
    :param pos: -- Tuple(x, y) -- The position of the player in the world measured in pixels
    :param size: -- Tuple(width, height) -- actual size of hitbox of the player
    :param sprite_offset: -- Tuple(x, y) -- the offset from the top left of the player image to the top left of the hitbox
    """

    def __init__(self, game, pos, size, sprite_offset):

        super().__init__(game, "Player", pos, size, sprite_offset)
        
        #UI class -- used for making and controlling windows
        self.ui = game.ui 
        #Cursor class and mouse class respectively - part of the ui -- Where and when you click
        self.cursor = game.ui.cursor 
        self.mouse = self.cursor.mouse
        #Tilemap class -- contains the Tiles used for collisions 
        self.tilemap = game.tilemap
        #Tile class -- the tile the cursor is currently over -- if not above tile then None
        self.hover_tile = None
        #String -- queue the next action using either "cancel" or the key in the action dictionary
        self.action_trigger = None
        #Tuple(Bool, Bool, Bool) -- True when mouse button is pressed -- [Left, Middle, Right] -- Otherwise False
        self.click_type = [False, False, False]
        #Add player specific action to the possible actions
        self.entity_actions["Mine"] = Mine(self, self.ui)
        self.entity_actions["Build"] = Build(self, self.ui)


    def update_movement(self, movement=(0, 0, 0, 0)):
        """
        Updates the physics and movement of the player
        
        :param movement: -- Tuple(float, float, float, float) -- movement of player (right, left, down, up)
        """
        self.x_movement = (movement[0] - movement[1])
        self.y_movement = (movement[2] - movement[3])
        #If moving diagonally then divide both by hypotenuse of desired movement triangle
        if abs(self.x_movement) > 0 and abs(self.y_movement) > 0:
            self.x_movement /= math.sqrt(2)
            self.y_movement /= math.sqrt(2)
        super().update(self.tilemap, movement=(self.x_movement, self.y_movement))
            
    def update_actions(self):
        """
        Updates the player regarding preformable actions \n
        1 : Resets the hover tile \n
        2 : Updates the mouse input \n
        3 : Updates the animations
        """
        hover_pose = self.cursor.pose()
        if hover_pose in self.tilemap.tilemap:
            self.hover_tile = self.tilemap.tilemap[hover_pose]
        else:
            self.hover_tile = None
        
        self.update_mouse_input()

        self.action.update()

        self.update_animations()

    def update_mouse_input(self):
        """
        Checks for click, hold, and release of each of the three mouse buttons
        """
        self.last_click_type = self.click_type
        self.click_type = self.mouse.get_pressed()
        # print(f"self.click_type: {self.click_type}, self.last_click_type: {self.last_click_type}")
        self.update_mouse_button(2, mouse_commands.left_click, mouse_commands.left_hold, mouse_commands.left_release)
        self.update_mouse_button(1, mouse_commands.middle_click, mouse_commands.middle_hold, mouse_commands.middle_release)
        self.update_mouse_button(0, mouse_commands.right_click, mouse_commands.right_hold, mouse_commands.right_release)
    
    def update_mouse_button(self, button_idx, on_click=None, on_hold=None, on_release=None, on_false=None):
        """
        The helper method for each mouse button
        
        :param button_idx: -- int -- The index of the mouse button being updated (0: left, 1: middle, 2: right)
        :param on_click: -- method -- Ran when the button is first pressed
        :param on_hold: -- method -- Ran while the button is held
        :param on_release: -- method -- Ran when the button is released
        :param on_false: -- method -- Ran while the button is not pressed
        """
        if self.click_type[button_idx]:
            if self.last_click_type[button_idx]:
                if on_hold is not None:
                    on_hold(self)
            else:
                if on_click is not None:
                    on_click(self)
        else:
            if self.last_click_type[button_idx]:
                if on_release is not None:
                    on_release(self)
            else:
                if on_false is not None:
                    on_false(self)

    def center_pose(self) -> tuple[float, float]:
        """
        Get the position in pixels of the center of the player
        
        :return: The position of the player in (x, y)
        :rtype: tuple[float, float]
        """
        return (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2)

    def update_animations(self):
        """
        Updates the players actions and animations \n
        Does not update the actual animation class, that is done in PhysicsEntity.update
        """
        if self.action_trigger == "Cancel":
            self.action_trigger = None
            self.set_action("Idle")
        if self.action_trigger == "Mine":
            self.action_trigger = None
            self.set_action("Mine")  
        if self.action_trigger == "Build":
            self.action_trigger = None
            self.set_action("Build")  
        # print(f"self.action_trigger: {self.action_trigger}, self.action.name: {self.action.m_name}")
        
        if abs(self.x_movement) > 0:
            if self.x_movement > 0:
                self.set_direction("d")
                self.set_action("Walk")
            else:
                self.set_direction("a")
                self.set_action("Walk")
        elif abs(self.y_movement) > 0:
            if self.y_movement > 0:
                self.set_direction("s")
                self.set_action("Walk")
            else:
                self.set_direction("w")
                self.set_action("Walk")
        else:
            if self.action.m_name == "Mine" or self.action.m_name == "Build":
                return
            self.set_action("Idle")      
        