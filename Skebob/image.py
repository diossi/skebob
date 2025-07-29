import pygame
import sys
import os

WIDTH, HEIGHT = int(round(574 * 0.8)), 1280 * 0.8
FPS = 60
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkeys=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkeys is not None:
        for colorkey in colorkeys:
            if colorkey == -1:
                colorkey = image.get_at((1, 1))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen(screen, clock):
    intro_text = ["Играть",
                  "Инструкция",
                  "Авторы"]

    fon = pygame.transform.scale(load_image('skebob_sasha.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (411, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)