from scripts.ui_elements.interactable import Interactable
from scripts.ui_elements.hotbar import Hotbar
from scripts.ui_elements.inventory import Inventory
from scripts.ui_elements.mouse import Cursor
from scripts.constants import Constants 
from scripts.ui_elements.text import Text
from scripts.ui_elements.window import Window

class Manager():
    def __init__(self, selected_tile=(None, None), interactable=None):
        self.selected_tile = selected_tile
        self.interactable = interactable

    def set_selected_tile(self, selected_tile):
        self.selected_tile = selected_tile

    def get_selected_tile(self) -> tuple[int, int]:
        return self.selected_tile
    
    def set_interactable(self, interactable):
        self.interactable = interactable

    def get_interactable(self) -> Interactable:
        return self.interactable

class UI:
    def __init__(self, game, assets, input, tile_size):
        self.input = input
        self.game = game
        self.assets = assets
        self.tile_size = tile_size
        self.text = Text(assets["Font"])
        self.open_interactables = {}
        self.all_windows = {}
        self.render_order = []

        self.hotbar = Hotbar("hotbar", self, assets["Inventory"], self.text, tile_size, 
                             ( Constants.screen_width/4 - self.tile_size*Constants.hotbar_width/2, Constants.screen_height/2 - self.tile_size*2), 
                             (Constants.hotbar_width, 1), self.input.get_hotkeys, is_open=True)
        
        self.inventory = Inventory("inventory", self, assets["Inventory"], self.text, tile_size, 
                                      (Constants.screen_width/4 - tile_size*(Constants.inventory_width-1)/2, Constants.screen_height/4 - self.tile_size*Constants.inventory_height/2),
                                      (Constants.inventory_width, Constants.inventory_height), 
                                      self.input.get_hotkeys, Constants.inventory_border, Constants.inventory_top_border, draggable=True, exit=True)
        
        self.cursor = Cursor(self.input.mouse, assets["Cursor"], Constants.tile_size)

        self.manager = Manager()
        
    def update(self, offset=(0, 0)):
        self.input.update_mouse()
        self.cursor.update(offset)

        order_copy = self.render_order.copy()
        order_copy.reverse()

        for i in order_copy:
            interactable = self.open_interactables[i]
            interactable.update(self.input.mouse)

        for i in self.all_windows.copy():
            interactable = self.all_windows[i]
            interactable.background_update()

    def release_item_drag(self, mouse_pose, origin):
        for i in self.open_interactables:
            interactable = self.open_interactables[i]
            if interactable.mouse_over_window(mouse_pose):
                idx = ((mouse_pose[0]-interactable.x)//interactable.tile_size, (mouse_pose[1]-interactable.y)//interactable.tile_size)
                if idx in interactable.items:
                    return interactable.release_item_drag(idx, origin, origin.manager.get_drag_quantity())
        return False

    def render(self, surface):
        print(self.render_order)
        for name in self.render_order:
            interactable = self.open_interactables[name]
            interactable.render(surface)      

    def render_cursor(self, surface, offset=(0, 0)):
        self.cursor.render(surface, offset)  