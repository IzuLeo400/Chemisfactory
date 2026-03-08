import pygame
from scripts.ui_elements.window import Manager, Window
from scripts.constants import Constants
from scripts.structures.structure import Structure

class unInteractableManager(Manager):
    def __init__(self, uninteractable, ui):
        super().__init__(ui)
        self.uninteractable = uninteractable
        self.type = None
        self.tile_size = Constants.tile_size
    
    def get_global_selected_tile(self) -> tuple[int, int]:
        return self.ui.manager.get_selected_tile()
    
    def same_interactable(self) -> bool:
        return self.interactable == self.ui.manager.get_interactable()
    
    def get_tile_size(self) -> int:
        return self.uninteractable.tile_size

class unInteractableSlot:
    def __init__(self, pose, assets, tile_size, manager, item=None):
        self.pose = pose
        self.assets = assets
        self.tile_size = tile_size
        self.manager = manager
        self.item = item
    
    def empty(self):
        self.item = None

    def render(self, surface, pose):
        location = (pose[0] + self.pose[0] * self.tile_size,
                    pose[1] + self.pose[1] * self.tile_size)
        tile_difference = (self.tile_size - self.manager.get_tile_size())//2
        base_img = self.assets[None]
        surface.blit(base_img, location)
        if self.item is not None:
            self.render_item(surface, (location[0] + tile_difference, location[1] + tile_difference))

    def render_item(self, surface, location):
        self.item.render(surface, location, tilemap=False)

class unInteractable(Window):
    def __init__(self, id, ui, assets, tile_size, pose=(0, 0), size=(0, 0), border=1, top_border=1, draggable=False, exit=False, is_open=False, border_color=((30, 30, 30))):
        super().__init__(id, ui, assets, pose, size, border, top_border, draggable=draggable, exit=exit, is_open=is_open, border_color=border_color)
        self.tile_size = tile_size
        self.items = {}
        self.manager = unInteractableManager(self, ui)
        self.reset()

    def reset(self):
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.items[(x, y)] = unInteractableSlot((x, y), self.assets, self.tile_size, self.manager)

    def mouse_over_window(self, mouse_pose) -> bool:
        if mouse_pose[0] > self.x - self.border and mouse_pose[0] < self.x + self.tile_size*self.size[0] + self.border:
            if mouse_pose[1] > self.y - self.top_border and mouse_pose[1] < self.y + self.tile_size*self.size[1] + self.border:
                return True
        return False

    def render(self, surface):
        outline = pygame.Surface((self.size[0]*self.tile_size+self.border*2,
                           self.size[1]*self.tile_size+self.border*(self.top_border//self.border+1)))
        outline.fill(self.border_color)
        surface.blit(outline, (self.x - self.border, self.y - self.top_border))
        for item in self.items:
            self.items[item].render(surface, (self.x, self.y))