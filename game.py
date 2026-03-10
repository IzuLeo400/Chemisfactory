import pygame

from scripts.tiles.structures.miner import Miner
from scripts.tiles.item import Item
from scripts.ui_elements.inputs import Input
from scripts.ui_elements.mouse import Mouse
from scripts.entities.player import Player
from scripts.tiles.tilemap import Tilemap
from scripts.sprites import load_image, load_images, Animation, load_tile_sheet
from scripts.constants import Constants
from scripts.ui_elements.ui import UI

class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Chemisfactory")
        self.screen = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))
        self.display = pygame.Surface((Constants.display_width, Constants.display_height))

        self.clock = pygame.time.Clock()
        
        self.assets = {
            "Sources": {
                "HydrogenSource": load_image('Tiles/Sources/HydrogenSource.png'),
                "OxygenSource": load_image('Tiles/Sources/OxygenSource.png'),
                "IronSource": load_image('Tiles/Sources/IronSource.png'),
            },
            "Tiles": {
                
            },
            "Player": {
                "Idle": {
                    "s": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 0), area=(2, 1), tile_size=32), img_dur=12),
                    "d": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 1), area=(2, 1), tile_size=32), img_dur=12),
                    "w": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 2), area=(2, 1), tile_size=32), img_dur=12),
                    "a": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 1), area=(2, 1), tile_size=32, flipped=True), img_dur=12),
                },
                "Walk": {
                    "s": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 3), area=(4, 1), tile_size=32)),
                    "d": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 4), area=(4, 1), tile_size=32)),
                    "w": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 5), area=(4, 1), tile_size=32)),
                    "a": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(0, 4), area=(4, 1), tile_size=32, flipped=True)),
                },
                "Mine": {
                    "s": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(4, 0), area=(4, 1), tile_size=32), img_dur=12),
                    "d": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(4, 1), area=(4, 1), tile_size=32), img_dur=12),
                    "w": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(4, 2), area=(4, 1), tile_size=32), img_dur=12),
                    "a": Animation(load_tile_sheet('Player/action_spritesheet.png', start_pose=(4, 1), area=(4, 1), tile_size=32, flipped=True), img_dur=12),
                }
            },
            "UI":{
                "Cursor": load_image('UI/Cursor.png'),
                "Inventory":
                {
                    None: load_image('UI/hotbar.png'),
                    "exit": load_image('UI/exit.png'),
                    "selected": load_image('UI/selected.png')
                },
                "Font": 
                {
                    "0": load_image('UI/font/0.png'),
                    "1": load_image('UI/font/1.png'),
                    "2": load_image('UI/font/2.png'),
                    "3": load_image('UI/font/3.png'),
                    "4": load_image('UI/font/4.png'),
                    "5": load_image('UI/font/5.png'),
                    "6": load_image('UI/font/6.png'),
                    "7": load_image('UI/font/7.png'),
                    "8": load_image('UI/font/8.png'),
                    "9": load_image('UI/font/9.png'),
                },
                "ProgressBar":{
                    "Mine": {
                        None: load_image('UI/emptyProgressBar.png'),
                        "full": load_image('UI/fullProgressBar.png'),
                    },
                }, 
            },
            "Background": load_image('Background/background.jpg'),
            "Structures": {
                "Miner": load_image('Tiles/Buldings/Miner.png')
            },
            "Items": {
                "Hydrogen": load_image('Items/Hydrogen.png'),
                "Oxygen": load_image('Items/Oxygen.png'),
                "Iron": load_image('Items/Iron.png'),
            }
        }

        self.tilemap = Tilemap(self)

        self.scroll = [-Constants.screen_width/4 + Constants.tile_size/2, -Constants.screen_height/4 + Constants.tile_size]

        self.mouse = Mouse()

        self.input = Input(self.mouse)

        self.ui = UI(self, self.assets["UI"], self.input, Constants.inventory_tile_size)

        # self.ui.inventory.items[(0, 0)].set_item(Item("Iron", (0, 0), 16, self.assets["Items"]["Iron"]), 6)
        # self.ui.inventory.items[(1, 0)].set_item(Item("Hydrogen", (0, 1), 16, self.assets["Items"]["Hydrogen"]), 7)
        # self.ui.inventory.items[(0, 1)].set_item(Item("Oxygen", (1, 0), 16, self.assets["Items"]["Oxygen"]), 9)
        self.ui.hotbar.items[(0, 0)].set_item(Miner((0, 0), Constants.tile_size, self.assets["Structures"]["Miner"], None), 1)

        self.player = Player(self, (0, 0), (6, 6), (13, 16))
        
    def run(self):
        while True:
            self.game_loop()

    def game_loop(self):
        self.display.blit(self.assets["Background"], (0, 0))

        self.input.update_keyboard()

        self.player.update_movement(self.input.movement)

        self.scroll[0] += (self.player.rect().centerx -
                           self.display.get_width() / 2 - self.scroll[0]) / 20
        self.scroll[1] += (self.player.rect().centery -
                           self.display.get_height() / 2 - self.scroll[1]) / 20
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.ui.update(render_scroll)

        self.player.update_actions()

        self.tilemap.render(self.display, render_scroll)
        self.ui.render_cursor(self.display, render_scroll)
        self.player.render(self.display, render_scroll)
        self.ui.render(self.display)

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0))
        pygame.display.update()
        self.clock.tick(60)

Game().run()