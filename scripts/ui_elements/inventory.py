from scripts.ui_elements.interactable import Interactable

class Inventory(Interactable):
    def __init__(self, id, ui, assets, text, tile_size, pose, size, get_hotkeys, border=1, top_border=1, draggable=False, exit=False, is_open=False, border_color=((30, 30, 30))):
        super().__init__(id, ui, assets, text, tile_size, pose, size, border, top_border, draggable, exit, is_open, border_color)
        self.get_hotkeys = get_hotkeys
        self.last_open = False
    
    def background_update(self):
        if self.get_hotkeys()[10]:
            if not self.last_open:
                self.last_open = True
                if self.is_open:
                    self.close()
                else:
                    self.open()
        else:
            self.last_open = False

    def update(self, mouse):
        super().update(mouse)
        #print(self.x, self.y)