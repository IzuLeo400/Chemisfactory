from scripts.ui_elements.interactable import Interactable

class Hotbar(Interactable):
    def __init__(self, id, ui, assets, text, tile_size, pose, size, get_hotkeys, border=1, top_border=1, draggable=False, exit=False, is_open=False, border_color=((30, 30, 30))):
        super().__init__(id, ui, assets, text, tile_size, pose, size, border, top_border, draggable, exit, is_open, border_color)
        self.get_hotkeys = get_hotkeys

    def update(self, mouse):
        super().update(mouse)
        self.manage_hotkeys()

    def manage_hotkeys(self):
        hotkeys = self.get_hotkeys()
        for idx in range(hotkeys.__len__()):
            if idx > 9:
                return 
            if hotkeys[idx]:
                self.manager.set_selected_tile((idx, 0))
                return 