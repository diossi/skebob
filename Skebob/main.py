import time
import pygame
import random
import datetime

from maps import *
from image import *
from pers import *
from shells import *

print((1280 - int(round(574 * 0.8))) / 2)
WIDTH, HEIGHT = 1280, int(round(1280 * 0.8))
FPS = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
is_move = False

change_x, change_y = 0, 0
old_time = time.time()
new_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            flag_end = 'exit'
            break
    
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w):
                player.direction = 'up'
                player.move_hero()
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                player.direction = 'down'
                player.move_hero()
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                player.direction = 'left'
                player.move_hero()
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                player.direction = 'right'
                player.move_hero()
            elif event.key == pygame.K_q:
                if player.direction == 'up':
                    change_y = -6
                    change_x = 0
                elif player.direction == 'down':
                    change_y = 6
                    change_x = 0
                elif player.direction == 'left':
                    change_x = -6
                    change_y = 0
                elif player.direction == 'right':
                    change_x = 6
                    change_y = 0
                harcho.limit = 0
                harcho.rect.x = player.pos[0] * 48
                harcho.rect.y = player.pos[1] * 48
                old_time = time.time()
            elif event.key == pygame.K_SPACE:
                cal.rect.x = player.pos[0] * 48 + 6
                cal.rect.y = player.pos[1] * 48 + 6
    if not running:
        break

    new_time = time.time()
    if new_time - old_time > 0.01:
        old_time = time.time()
        harcho.update(change_x, change_y)

    screen.fill((113, 221, 238))
    background_group.draw(screen)
    all_sprites.draw(screen)
    cal_group.draw(screen)
    harcho_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

pygame.quit()