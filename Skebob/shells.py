from pers import *

pygame.init()


class Harcho(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(harcho_group, all_sprites)

        self.image = pygame.transform.scale(load_image('harcho.png', -1), (48, 48))
        self.rect = self.image.get_rect()
        self.limit = 0

    def update(self, change_x, change_y):
        if self.limit < 30:
            self.limit += 1
            self.rect = self.rect.move(change_x, change_y)
        else:
            self.rect.x = 10000


class Cal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cal_group, all_sprites)
        self.image = pygame.transform.scale(load_image('cal.jpg', -1), (36, 36))
        self.rect = self.image.get_rect()
        self.limit = 0


cal_group = pygame.sprite.Group()
harcho_group = pygame.sprite.Group()
cal = Cal()
harcho = Harcho()
