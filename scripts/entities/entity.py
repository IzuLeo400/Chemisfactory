import math
import pygame

from scripts.entities.action import Action
from pygame.rect import Rect
from scripts.entities.player_actions.mine import Mine
from scripts.sprites import Animation

class PhysicsEntity:
    """
    The abstract class for an entity with collisions
    
    :param game: -- Game -- The actual main class controlling the entire game
    :param e_type: -- String -- The type of the entity (ie: "player")
    :param pos: -- Tuple(x, y) -- The position of the player in the world measured in pixels
    :param size: -- Tuple(width, height) -- actual size of hitbox of the entity
    :param sprite_offset: -- Tuple(x, y) -- the offset from the top left of the entity image to the top left of its hitbox
    """
    def __init__(self, game, e_type, pos, size, sprite_offset):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        #tuple(float, float) -- the speed of the entity measued in pixels (x, y) 
        self.velocity = [0, 0]
        #dictionary{} -- the collisions of each direction (mapped to a bool)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.sprite_offset = sprite_offset
        #Action class -- the current action being preformed by the entity -- if no action then None
        self.action = Action(self)
        self.animation = Animation([], 1)
        #String -- the direction the player is facing using 'w' 'a' 's' 'd' 
        self.direction = "s"
        #Actions preformable by any entity
        self.entity_actions = {"Idle": Action(self, "Idle"), "Walk": Action(self, "Walk")}
        self.set_action("Idle")
        
    def set_action(self, action):
        """
        sets the action to the new action in entity_actions

        :param action: -- String -- the key to the entity_actions dictionary (ie: "Idle")
        """
        if action != self.action.m_name and self.entity_actions[action].start():
            #print(f"Changing action from {self.action.m_name} to {action}")
            self.action.end(interrupted=True)
            self.action = self.entity_actions[action]
            self.animation = self.game.assets[self.type][self.action.m_name][self.direction].copy()

    def set_direction(self, direction):
        """
        changes the direction of the animation

        :param direction: -- String -- the direction the player is facing using 'w' 'a' 's' 'd' 
        """
        if self.direction != direction:
            self.direction = direction
            self.animation = self.game.assets[self.type][self.action.m_name][self.direction].copy()

    def rect(self) -> Rect:
        """
        :return: The pygame rectangle that contains the position and hitbox of the entity
        :rtype: Rect
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
 
    def update(self, tilemap, movement=(0, 0)):
        """
        The movement and collisions control for the entity
        
        :param tilemap: -- Tilemap -- all the tiles in the game
        :param movement: -- Tuple(double, double) -- the movement of the entity (x, y)
        """
        #Reset collisions
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0], movement[1])
        
        #Check x movement - if it collides with another rect then move to edge of rect instead
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, depth=1):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        #Check y movement - if it collides with another rect then move to edge of rect instead
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, depth=1):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        #Updates the animation after the movement
        self.animation.update()
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0] - self.sprite_offset[0], self.pos[1] - offset[1] - self.sprite_offset[1]))
        #Render Hitbox:
        #surf.blit(pygame.Surface(self.rect().size), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

