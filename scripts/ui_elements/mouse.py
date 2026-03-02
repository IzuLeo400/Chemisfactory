import pygame


class Cursor:
  def __init__(self, mouse, img, tile_size):
    self.mouse = mouse
    self.img = img
    self.tile_size = tile_size
    self.x = 0
    self.y = 0

  def pose(self) -> tuple[int, int]:
    return (self.x, self.y)
  
  def mouse_click(self) -> str:
    if self.mouse.left_click():
      return  "left"
    if self.mouse.right_click():
      return "right"
    if self.mouse.middle_click():
      return "middle"
    return ""

  def update(self, offset=(0, 0)):
    mouse_pose = self.mouse.get_pose()
    mouse_pose = (mouse_pose[0]//2, mouse_pose[1]//2)
    self.x = (mouse_pose[0] + offset[0]) // self.tile_size
    self.y = (mouse_pose[1] + offset[1]) // self.tile_size
    

  def render(self, surface, offset=(0, 0)):
    if not self.mouse.over_ui():
      surface.blit(self.img, (self.x * self.tile_size - offset[0], self.y * self.tile_size - offset[1]))

class Mouse:
  def __init__(self):
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    #mouse buttons        left, middle, right 
    self.mouse_pressed = (False, False, False)
    self.last_mouse_pressed = (False, False, False)
    self.used = False
    self.hover = ""

  def update(self):
    self.last_mouse_pressed = self.mouse_pressed
    self.mouse_pressed = self.get_pressed()
    self.used = False
    self.hover = ""

  def over_ui(self) -> bool:
    if self.hover == "ui":
      return True
    return False

  def left_click(self) -> bool:
    if (not self.last_mouse_pressed[0]) and self.mouse_pressed[0] and not self.used:
      return True
    return False
  
  def left_pressed(self) -> bool:
    return self.get_pressed()[0]
      
  def right_click(self) -> bool:
    if (not self.last_mouse_pressed[2]) and self.mouse_pressed[2] and not self.used:
      return True
    return False
  
  def right_pressed(self) -> bool:
    return self.get_pressed()[2]

  def middle_click(self) -> bool:
    if (not self.last_mouse_pressed[1]) and self.mouse_pressed[1] and not self.used:
      return True
    return False
  
  def middle_pressed(self) -> bool:
    return self.get_pressed()[1]

  def get_pose(self) -> tuple[int, int]:
    return pygame.mouse.get_pos()
  
  def get_pressed(self) -> tuple[bool, bool, bool]:
    return pygame.mouse.get_pressed()
  
  def click_used(self):
    self.used = True

  def get_click_used(self) -> bool:
    return self.used

  def hover_over_ui(self):
    self.hover = "ui"