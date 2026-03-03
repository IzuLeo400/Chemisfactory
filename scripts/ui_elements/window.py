import pygame
from scripts.constants import Constants


class Manager:
    def __init__(self, ui):
        self.ui = ui
        self.window_drag = False
        self.drag_pose = (None, None)

    def initiate_window_drag(self, mouse_pose):
        self.window_drag = True
        self.drag_pose = mouse_pose

    def end_window_drag(self):
        self.window_drag = False

    def get_window_drag(self) -> bool:
        if self.window_drag:
            return True
        return False
    
    def set_drag_pose(self, pose):
        self.drag_pose = pose

    def get_drag_pose(self) -> tuple[int, int]:
        return self.drag_pose
    
    def dragging(self) -> bool:
        if self.window_drag:
            return True
        return False

class Window:
    def __init__(self, id, ui, assets, pose=(0, 0), size=(0, 0), border=0, top_border=0, img=None, draggable=False, exit=False, is_open=False, border_color=((30, 30, 30))):
        self.id = id
        self.ui = ui
        self.assets = assets
        self.size = size
        self.border = border
        self.top_border = top_border
        self.border_color = border_color
        self.img = img
        self.draggable = draggable
        self.exit = exit
        self.x = pose[0]
        self.y = pose[1]
        self.manager = Manager(ui)

        if is_open:
            self.open()
        else:
            self.close()

        self.ui.all_windows[id] = self

    def background_update(self):
        #This is meant to be overriden by subclases and called at all times (even when not visible) 
        return

    def update(self, mouse):
        mouse_pose = mouse.get_pose()
        mouse_pose = (mouse_pose[0]//2, mouse_pose[1]//2)
        self.update_drag(mouse, mouse_pose)
        self.update_click(mouse, mouse_pose)

    def update_drag(self, mouse, mouse_pose):
        if not mouse.left_pressed():
            if self.manager.get_window_drag():
                self.manager.end_window_drag()
        elif self.manager.dragging() and self.manager.get_drag_type() == "left":
            drag_pose = self.manager.get_drag_pose()
            if self.manager.get_window_drag():
                self.x = self.x - (drag_pose[0] - mouse_pose[0])
                self.y = self.y - (drag_pose[1] - mouse_pose[1])
                self.limit_drag(mouse_pose)
            self.manager.set_drag_pose(mouse_pose)

    def update_click(self, mouse, mouse_pose):
        if self.mouse_over_window(mouse_pose):
            mouse.hover_over_ui()
            if mouse.left_click():
                    self.inventory_click(mouse_pose)
                    self.prioritize_render()
                    mouse.click_used()

    def limit_drag(self, mouse_pose):
        self.limit_window_drag()
        self.limit_drag_out_of_bounds(mouse_pose)
        
    def limit_window_drag(self):
        if self.x < self.border:
            self.x = self.border
        elif self.x > Constants.display_width - self.border - self.size[0]:
            self.x = Constants.display_width - self.border - self.size[0]
        if self.y < self.top_border:
            self.y = self.top_border
        if self.y > Constants.display_height - self.border - self.size[1]:
            self.y = Constants.display_height - self.border - self.size[1]

    def limit_drag_out_of_bounds(self, mouse_pose):
        if mouse_pose[0] < 0 or mouse_pose[0] > Constants.display_width:
            self.stop_all_drag()
        if mouse_pose[1] < 0 or mouse_pose[1] > Constants.display_height:
            self.stop_all_drag()

    def stop_all_drag(self):
        if self.manager.get_window_drag():
            self.manager.end_window_drag()

    def mouse_over_window(self, mouse_pose) -> bool:
        if mouse_pose[0] > self.x - self.border and mouse_pose[0] < self.x + self.size[0] + self.border:
            if mouse_pose[1] > self.y - self.top_border and mouse_pose[1] < self.y + self.size[1] + self.border:
                return True
        return False
    
    def mouse_over_exit(self, mouse_pose) -> bool:
        if self.exit:
            if mouse_pose[0] > self.x + self.size[0] - Constants.tile_size and mouse_pose[0] < self.x + self.size[0]:
                if mouse_pose[1] > self.y - self.top_border + self.border/2 and mouse_pose[1] < self.y - self.border/2:
                    return True
        return False
    
    def inventory_click(self, mouse_pose, type="left"):
        if type == "left":
            if self.exit and self.mouse_over_exit(mouse_pose):
                    self.close()
                    return
            self.manager.initiate_window_drag(mouse_pose, type)

    def prioritize_render(self):
        if self.id in self.ui.render_order:
            self.ui.render_order.pop(self.ui.render_order.index(self.id))
        self.ui.render_order.append(self.id)

    def remove_render(self):
        if self.id in self.ui.render_order:
            self.ui.render_order.pop(self.ui.render_order.index(self.id))

    def close(self):
        self.is_open = False
        if self.id in self.ui.open_interactables:
            self.ui.open_interactables.pop(self.id)
        self.remove_render()

    def open(self):
        self.is_open = True
        self.ui.open_interactables[self.id] = self
        self.prioritize_render()

    def delete(self):
        self.close()
        if self.id in self.ui.all_windows:
            self.ui.all_windows.pop(self.id)

    def render(self, surface):
        top_border = self.top_border
        border = self.border+1
        outline = pygame.Surface((self.size[0]+self.border*2,
                           self.size[1]+self.border*(top_border/border)))
        outline.fill(self.border_color)
        surface.blit(outline, (self.x - self.border, self.y - self.top_border))
        if self.img is not None:
            surface.blit(self.img, (self.x, self.y))
        if self.exit:
            surface.blit(self.assets["exit"],
                        (self.x + self.tile_size * (self.size[0] - 1),
                        self.y - self.top_border + self.border/2))
