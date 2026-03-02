import pygame
from scripts.ui_elements.window import Manager, Window
from scripts.constants import Constants
from scripts.structures.structure import Structure

class InteractableManager(Manager):
    def __init__(self, interactable, ui):
        super().__init__(ui)
        self.interactable = interactable
        self.selected_tile = (None, None)
        self.item_drag = False
        self.tile_size = Constants.tile_size
        self.drag_quantity = 0
        self.type = None

    def initiate_window_drag(self, mouse_pose, type):
        super().initiate_window_drag(mouse_pose)
        self.type = type

    def end_window_drag(self):
        super().end_window_drag()
        self.type = None

    def get_window_drag(self) -> bool:
        if self.window_drag:
            return True
        return False
    
    def initiate_item_drag(self, mouse_pose, quantity, type):
        self.item_drag = True
        self.drag_pose = mouse_pose
        self.drag_quantity = quantity
        self.type = type

    def end_item_drag(self):
        self.item_drag = False
        self.drag_pose = (None, None)
        self.drag_quantity = 0
        self.type = None

    def get_item_drag(self) -> bool:
        if self.item_drag:
            return True
        return False

    def get_drag_quantity(self) -> bool:
        return self.drag_quantity

    def get_drag_type(self) -> str:
        return self.type
    
    def set_selected_tile(self, tile):
        self.selected_tile = tile
        self.ui.manager.set_selected_tile(tile)
        self.ui.manager.set_interactable(self.interactable)
    
    def get_selected_tile(self) -> tuple[int, int]:
        return self.selected_tile
    
    def dragging(self) -> bool:
        if self.item_drag or self.window_drag:
            return True
        return False
    
    def get_tile_size(self) -> int:
        return self.tile_size
    
    def get_global_selected_tile(self) -> tuple[int, int]:
        return self.ui.manager.get_selected_tile()
    
    def same_interactable(self) -> bool:
        return self.interactable == self.ui.manager.get_interactable()

class InteractableSlot:
    def __init__(self, pose, assets, text, tile_size, manager, item=None, quantity=None):
        self.pose = pose
        self.assets = assets
        self.text = text
        self.item = item
        self.quantity = quantity
        self.tile_size = tile_size
        self.manager = manager
    
    def empty(self):
        self.item = None
        self.quantity = None

    def subtract(self, quantity):
        if self.quantity <= quantity:
            self.empty()
        else:
            self.quantity -= quantity

    def get_item(self) -> Structure:
        return self.item

    def set_item(self, item, quantity):
        self.item = item
        self.quantity = quantity

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def render(self, surface, pose):
        location = (pose[0] + self.pose[0] * self.tile_size,
                    pose[1] + self.pose[1] * self.tile_size)
        tile_difference = (self.tile_size - self.manager.get_tile_size())//2
        selected = self.pose == self.manager.get_global_selected_tile() and self.manager.same_interactable()
        if selected:
            base_img = self.assets["selected"]
        else:
            base_img = self.assets[None]
        surface.blit(base_img, location)
        if self.item is not None:
            if selected:
                if self.manager.get_drag_quantity() < self.quantity:
                    self.render_item(surface, (location[0] + tile_difference, location[1] + tile_difference))
                    self.render_text(surface, self.quantity-self.manager.get_drag_quantity(), (location[0]+1, location[1]+1))
                if self.manager.get_item_drag():
                    item_pose = (self.manager.get_drag_pose()[0] - self.manager.get_tile_size()//2, self.manager.get_drag_pose()[1] - self.manager.get_tile_size()//2)
                    self.render_item(surface, item_pose)
                    self.render_text(surface, self.manager.get_drag_quantity(), (item_pose[0] - 4, item_pose[1] - 4))
            else:
                self.render_item(surface, (location[0] + tile_difference, location[1] + tile_difference))
                self.render_text(surface, self.quantity, (location[0]+1, location[1]+1))

    def render_item(self, surface, location):
        self.item.render(surface, location, tilemap=False)
            
    def render_text(self, surface, quantity, location):
        self.text.box_render(str(quantity), surface, location)

class Interactable(Window):
    def __init__(self, id, ui, assets, text, tile_size, pose=(0, 0), size=(0, 0), border=1, top_border=1, draggable=False, exit=False, is_open=False, border_color=((30, 30, 30))):
        super().__init__(id, ui, assets, pose, size, border, top_border, draggable=draggable, exit=exit, is_open=is_open, border_color=border_color)
        self.text = text
        self.tile_size = tile_size
        self.items = {}
        self.manager = InteractableManager(self, ui)
        self.reset()

    def reset(self):
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.items[(x, y)] = InteractableSlot((x, y), self.assets, self.text, self.tile_size, self.manager)
        
    def update_drag(self, mouse, mouse_pose):
        if not mouse.left_pressed():
            if self.manager.get_window_drag():
                self.manager.end_window_drag()
            if self.manager.get_item_drag() and self.manager.get_drag_type() == "left":
                self.end_item_drag(mouse_pose)
                self.manager.end_item_drag()
        elif self.manager.dragging() and self.manager.get_drag_type() == "left":
            drag_pose = self.manager.get_drag_pose()
            if self.manager.get_window_drag():
                self.x = self.x - (drag_pose[0] - mouse_pose[0])
                self.y = self.y - (drag_pose[1] - mouse_pose[1])
                self.limit_drag(mouse_pose)
            self.manager.set_drag_pose(mouse_pose)
        if not mouse.right_pressed():
            if self.manager.get_item_drag() and self.manager.get_drag_type() == "right":
                self.end_item_drag(mouse_pose)
                self.manager.end_item_drag()
        elif self.manager.get_item_drag() and self.manager.get_drag_type() == "right":
            self.manager.set_drag_pose(mouse_pose)
        if self.manager.get_item_drag() and not mouse.middle_pressed() and self.manager.get_drag_type() == "middle":
            self.end_item_drag(mouse_pose)
            self.manager.end_item_drag()        
        elif self.manager.get_item_drag() and self.manager.get_drag_type() == "middle":
            self.manager.set_drag_pose(mouse_pose)    

    def update_click(self, mouse, mouse_pose):
        if not mouse.get_click_used():
            if self.mouse_over_window(mouse_pose):
                mouse.hover_over_ui()
                if mouse.left_click():
                        self.inventory_click(mouse_pose, type="left")
                        mouse.click_used()
                if mouse.right_click():
                        self.inventory_click(mouse_pose, type="right")
                        mouse.click_used()
                if mouse.middle_click():
                        self.inventory_click(mouse_pose, type="middle")
                        mouse.click_used()

    def end_item_drag(self, mouse_pose):
        idx = ((mouse_pose[0]-self.x)//self.tile_size, (mouse_pose[1]-self.y)//self.tile_size)
        if idx in self.items:
            selected_tile = self.manager.get_selected_tile()                    
            if self.release_item_drag(idx, self, self.manager.get_drag_quantity()):
                self.items[selected_tile].subtract(self.manager.get_drag_quantity())
        else:
            if self.ui.release_item_drag(mouse_pose, self):
                self.items[self.manager.selected_tile].subtract(self.manager.get_drag_quantity())

    def limit_window_drag(self):
        if self.x < self.border:
            self.x = self.border
        elif self.x > Constants.display_width - self.border - self.size[0] * self.tile_size:
            self.x = Constants.display_width - self.border - self.size[0] * self.tile_size
        if self.y < self.top_border:
            self.y = self.top_border
        if self.y > Constants.display_height - self.border - self.size[1] * self.tile_size:
            self.y = Constants.display_height - self.border - self.size[1] * self.tile_size

    def stop_all_drag(self):
        super().stop_all_drag()
        if self.manager.get_item_drag():
            self.manager.end_item_drag()

    def release_item_drag(self, idx, interactable, quantity) -> bool:
        if idx == self.manager.get_global_selected_tile() and self.manager.same_interactable():
            return False
        selected_tile = interactable.items[interactable.manager.get_selected_tile()]
        hover_tile = self.items[idx]
        if hover_tile.item is None:
            self.items[idx].set_item(selected_tile.get_item(), quantity)
            self.manager.set_selected_tile(idx)
            self.prioritize_render()
            return True
        else:
            if hover_tile.item == selected_tile.item:
                self.items[idx].set_quantity(quantity + hover_tile.get_quantity())
                self.prioritize_render()
                return True
        return False

    def mouse_over_window(self, mouse_pose) -> bool:
        if mouse_pose[0] > self.x - self.border and mouse_pose[0] < self.x + self.tile_size*self.size[0] + self.border:
            if mouse_pose[1] > self.y - self.top_border and mouse_pose[1] < self.y + self.tile_size*self.size[1] + self.border:
                return True
        return False
    
    def mouse_over_exit(self, mouse_pose) -> bool:
        if mouse_pose[0] > self.x + self.tile_size * (self.size[0] - 1) and mouse_pose[0] < self.x + self.tile_size * self.size[0]:
            if mouse_pose[1] > self.y - self.top_border + self.border/2 and mouse_pose[1] < self.y - self.border/2:
                return True
        return False
    
    def inventory_click(self, mouse_pose, type="left"):
        self.prioritize_render()
        idx = ((mouse_pose[0]-self.x)//self.tile_size, (mouse_pose[1]-self.y)//self.tile_size)
        if idx in self.items:
            self.manager.set_selected_tile(idx)
            if self.items[idx].get_item() is not None:
                if type == "left":
                    self.manager.initiate_item_drag(mouse_pose, self.items[idx].get_quantity(), type)
                if type == "right":
                    self.manager.initiate_item_drag(mouse_pose, 1, type)
                if type == "middle":
                    quantity = self.items[idx].get_quantity()
                    if quantity % 2 == 1 or quantity == 0:
                        quantity = quantity//2+1
                    else:
                        quantity = quantity//2
                    self.manager.initiate_item_drag(mouse_pose, quantity, type)
        else: 
            super().inventory_click(mouse_pose, type)

    def render(self, surface):
        outline = pygame.Surface((self.size[0]*self.tile_size+self.border*2,
                           self.size[1]*self.tile_size+self.border*(self.top_border//self.border+1)))
        outline.fill(self.border_color)
        surface.blit(outline, (self.x - self.border, self.y - self.top_border))
        if self.ui.manager.get_interactable() == self:
            selected_tile = self.ui.manager.get_selected_tile()
        else: 
            selected_tile = (None, None)
        for item in self.items:
            if not item == selected_tile:
                self.items[item].render(surface, (self.x, self.y))
        if not selected_tile == (None, None):
            self.items[selected_tile].render(surface, (self.x, self.y))
        if self.exit:
            surface.blit(self.assets["exit"],
                        (self.x + self.tile_size * (self.size[0] - 1),
                        self.y - self.top_border + self.border/2))