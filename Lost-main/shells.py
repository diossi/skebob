from pers import *

pygame.init()


class FireBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(fireball_group, all_sprites)

        self.image = pygame.transform.scale(load_image('fireball.png', -1), (48, 48))
        self.rect = self.image.get_rect()
        self.limit = 0

    def update(self, change_x, change_y):
        if self.limit < 30:
            self.limit += 1
            self.rect = self.rect.move(change_x, change_y)
        else:
            self.rect.x = 10000


fireball_group = pygame.sprite.Group()
fireball = FireBall()
