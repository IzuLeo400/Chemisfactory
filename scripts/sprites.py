import os

import pygame

BASE_IMG_PATH = 'assets/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_tile_sheet(path, start_pose=(0, 0), area=(1, 1), flipped=False, remove=[], tile_size=16):
    sprite_sheet = load_image(path)

    tiles = []
    
    idx = 0
    for x in range(area[0]):
        for y in range(area[1]):
            if idx not in remove:
                surface = pygame.Surface((tile_size, tile_size))
                rect = pygame.Rect((x + start_pose[0]) * tile_size, (y + start_pose[1]) * tile_size, tile_size, tile_size)
                surface.blit(sprite_sheet, (0, 0), rect)
                surface.set_colorkey((0, 0, 0))
                if flipped:
                    surface = pygame.transform.flip(surface, True, False)
                tiles.append(surface)
            idx += 1
    return tiles


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration *
                                             len(self.images))
        else:
            self.frame = min(self.frame + 1,
                             self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
