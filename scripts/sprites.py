import os

import pygame

BASE_IMG_PATH = 'assets/'


def load_image(path, rotation=0):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    if rotation != 0:
        img = pygame.transform.rotate(img, rotation)
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
    """
    The class that handles the animation of a sprite. It takes in a list of images and cycles through them based on the img_duration parameter. 
    
    :param images: -- List[pygame.Surface] -- The list of images for the animation
    :param img_duration: -- int -- The duration of each image in the animation in frames -- 0 means the animation is static and will not change
    :param loop: -- bool -- Whether the animation should loop
    """

    def __init__(self, images: list[pygame.Surface], img_dur: int=0, loop: bool=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = (img_dur == 0)
        self.frame = 0
        if (images.__class__ != list):
            raise TypeError("images must be a list of pygame.Surface objects")

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.done:
            return False
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration *
                                             len(self.images))
        else:
            self.frame = min(self.frame + 1,
                             self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
        return True

    def img(self):
        return self.images[0] if self.img_duration == 0 else self.images[int(self.frame / self.img_duration)]

    def blit(self, surface, pos):
        for img in self.images:
            img.blit(surface, pos)
