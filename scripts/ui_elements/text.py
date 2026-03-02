import pygame

from scripts.constants import Constants

#default letter width = 4px, letter height always 6px
irregular_letters = {"1":3, "7":5}

class Text:
    def __init__(self, assets):
        self.assets = assets
        self.letters = {"0":None, "1":None, "2":None, "3":None, "4":None, "5":None, "6":None, "7":None, "8":None, "9":None,}
        self.fill_alphabet()
        self.letter_gap = Constants.letter_gap
        self.letter_width = Constants.letter_width

    def fill_alphabet(self):
        for letter in self.letters:
            self.letters[letter] = self.assets[letter]
        
    def text_length(self, text) -> int:
        text_length = 0
        for letter in text:
            text_length += self.letter_gap
            if letter in irregular_letters:
                text_length += irregular_letters[letter]
            else:
                text_length += self.letter_width
        return text_length

    def box_render(self, text, surface, pose):
        box = pygame.Surface((self.text_length(text)+1, 8))
        box.fill((62, 185, 133))
        self.render(text, box, (1, 1))
        surface.blit(box, (pose))

    def render(self, text, surface, pose):
        x = pose[0]
        y = pose[1]
        for letter in text:
            surface.blit(self.letters[letter], (x, y))
            x += self.letter_gap
            if letter in irregular_letters:
                x += irregular_letters[letter]
            else:
                x += self.letter_width