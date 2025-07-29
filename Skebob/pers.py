import pygame
import os
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1440, 900
FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == -2:
        return image
    elif colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)

        self.image = player_image
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.direction = 'up'

    def move_hero(self):
        if self.direction == 'up':
            self.pos = (self.pos[0], self.pos[1] - 1)
            self.rect = self.image.get_rect().move(self.rect.x, self.rect.y - move_hero)
        elif self.direction == 'down':
            self.pos = (self.pos[0], self.pos[1] + 1)
            self.rect = self.image.get_rect().move(self.rect.x, self.rect.y + move_hero)
        elif self.direction == 'left':
            self.pos = (self.pos[0] - 1, self.pos[1])
            self.rect = self.image.get_rect().move(self.rect.x - move_hero, self.rect.y)
        elif self.direction == 'right':
            self.pos = (self.pos[0] + 1, self.pos[1])
            self.rect = self.image.get_rect().move(self.rect.x + move_hero, self.rect.y)


class Background(pygame.sprite.Sprite):
    def __init__(self, background_name, pos_x, pos_y):
        super().__init__(background_group, all_sprites)
        self.image = load_image(background_name, -2)
        self.image = pygame.transform.scale(self.image, (int(round(574 * 0.8)), 1280 * 0.8))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


move_hero = 48
tile_width, tile_height = 48, 48

player_image = load_image('skebob.jpg', -1)
all_sprites = pygame.sprite.Group()
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
background = Background('skebob_sasha.jpg', 9, 0)
player = Player(1, 1)
