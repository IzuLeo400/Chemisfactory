import sys
import pygame


class Input:
    def __init__(self, mouse):
        self.mouse = mouse
        #movement keys   D      A      S      W
        self.movement = [False, False, False, False]
        #               1      2      3      4      5      6      7      8      9      0      Tab
        self.hotkeys = [False, False, False, False, False, False, False, False, False, False, False]

    def get_movement_keys(self) -> list[bool, bool, bool, bool]:
        return self.movement
    
    def get_hotkeys(self) -> list[bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool]:
        return self.hotkeys

    def update_mouse(self):
        self.mouse.update()

    def update_keyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement[0] = True
                if event.key == pygame.K_a:
                    self.movement[1] = True
                if event.key == pygame.K_s:
                    self.movement[2] = True
                if event.key == pygame.K_w:
                    self.movement[3] = True
                
                if event.key == pygame.K_1:
                    self.hotkeys[0] = True
                if event.key == pygame.K_2:
                    self.hotkeys[1] = True
                if event.key == pygame.K_3:
                    self.hotkeys[2] = True
                if event.key == pygame.K_4:
                    self.hotkeys[3] = True
                if event.key == pygame.K_5:
                    self.hotkeys[4] = True
                if event.key == pygame.K_6:
                    self.hotkeys[5] = True
                if event.key == pygame.K_7:
                    self.hotkeys[6] = True
                if event.key == pygame.K_8:
                    self.hotkeys[7] = True
                if event.key == pygame.K_9:
                    self.hotkeys[8] = True
                if event.key == pygame.K_0:
                    self.hotkeys[9] = True
                if event.key == pygame.K_TAB:
                    self.hotkeys[10] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.movement[0] = False
                if event.key == pygame.K_a:
                    self.movement[1] = False
                if event.key == pygame.K_s:
                    self.movement[2] = False
                if event.key == pygame.K_w:
                    self.movement[3] = False

                if event.key == pygame.K_1:
                    self.hotkeys[0] = False
                if event.key == pygame.K_2:
                    self.hotkeys[1] = False
                if event.key == pygame.K_3:
                    self.hotkeys[2] = False
                if event.key == pygame.K_4:
                    self.hotkeys[3] = False
                if event.key == pygame.K_5:
                    self.hotkeys[4] = False
                if event.key == pygame.K_6:
                    self.hotkeys[5] = False
                if event.key == pygame.K_7:
                    self.hotkeys[6] = False
                if event.key == pygame.K_8:
                    self.hotkeys[7] = False
                if event.key == pygame.K_9:
                    self.hotkeys[8] = False
                if event.key == pygame.K_0:
                    self.hotkeys[9] = False
                if event.key == pygame.K_TAB:
                    self.hotkeys[10] = False