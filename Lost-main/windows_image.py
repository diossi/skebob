import pygame
import sys
import os

WIDTH, HEIGHT = 1440, 900
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

    fon = pygame.transform.scale(load_image('start_window.jpg'), (WIDTH, HEIGHT))
    coords_text = []
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 220
    for line in intro_text:
        string_rendered = font.render(line, True, 'white', pygame.Color((153, 92, 51)))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 720 - intro_rect.width // 2
        text_coord += intro_rect.height
        coords_text.append((intro_rect.x, intro_rect.y, intro_rect.width, intro_rect.height))
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if coords_text[0][0] + coords_text[0][2] > x > coords_text[0][0] and \
                            coords_text[0][1] + coords_text[0][3] > y > coords_text[0][1]:
                        return
                    elif coords_text[1][0] + coords_text[1][2] > x > coords_text[1][0] and \
                            coords_text[1][1] + coords_text[1][3] > y > coords_text[1][1]:
                        manual(screen, clock)
                        return
                    elif coords_text[2][0] + coords_text[2][2] > x > coords_text[2][0] and \
                            coords_text[2][1] + coords_text[2][3] > y > coords_text[2][1]:
                        authors(screen, clock)
                        return
        pygame.display.flip()
        clock.tick(FPS)


def manual(screen, clock):
    intro_text = ["Передвижение - WASD(стрелочки)",
                  "Атаковать - SPACE(пробел)",
                  "Атаковать магией - Q",
                  'Чтобы получить уровень, нужно убивать монстров или выполнять задания',
                  'При получении уровня вы получаете 1 единицу прокачки, с помощью которой',
                  'вы можете прокачать силу, ловкость и интеллект(на выбор)',
                  'На каждой локации есть магазин(один из домов), чтобы открыть его нужно',
                  'подойти к дому и нажать E']

    fon = pygame.transform.scale(load_image('start_window.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, True, 'white', pygame.Color((153, 92, 51)))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 80)
    string_rendered = font.render('Назад', True, 'white', pygame.Color((153, 92, 51)))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 1200, 30
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if intro_rect.x < x < intro_rect.x + intro_rect.width and \
                            intro_rect.y < y < intro_rect.y + intro_rect.height:
                        start_screen(screen, clock)
                        return
        pygame.display.flip()
        clock.tick(FPS)


def authors(screen, clock):
    intro_text = ["Цырулев А.А.",
                  "Валиев Д.И."]

    fon = pygame.transform.scale(load_image('start_window.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, True, 'white', pygame.Color((153, 92, 51)))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 720 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 80)
    string_rendered = font.render('Назад', True, 'white', pygame.Color((153, 92, 51)))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 1200, 30
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if intro_rect.x < x < intro_rect.x + intro_rect.width and \
                            intro_rect.y < y < intro_rect.y + intro_rect.height:
                        start_screen(screen, clock)
                        return
        pygame.display.flip()
        clock.tick(FPS)


def window_with_text(screen, clock):
    screen.fill('black')
    number_text = 0
    plot_text = [["Вы оказались в каком-то непонятном месте,",
                  "вокруг неизвестная вам земля.",
                  "Вы пытаетесь вспомнить, как вы здесь оказались."],
                 ['Ничего не вспомнив вы решаете осмотреться.',
                  'Увидев записку на земле вы решаете',
                  'ее поднять и прочитать.'],
                 ['Из нее вы понимате, что это не ваш мир',
                  ' и вы оказались в чужом теле.',
                  'Также из нее вы узнаете что в этом мире есть магия.'],
                 ['В конце записки написано, что в этой вселенной есть маг,', 'который может перемещать между мирами.'],
                 ['Вы решаетесь пойти по тропинке,', 'чтобы узнать, как попасть обратно в ваш мир.']]

    fon = pygame.transform.scale(load_image('window_with_text.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] < 720 and number_text != 0:
                        number_text -= 1
                    elif event.pos[0] >= 720:
                        number_text += 1
                    if number_text + 1 > len(plot_text):
                        return
        screen.blit(fon, (0, 0))
        text_coord = 300
        for line in plot_text[number_text]:
            string_rendered = font.render(line, True, (51, 51, 51), (204, 204, 204))
            plot_rect = string_rendered.get_rect()
            text_coord += 15
            plot_rect.top = text_coord
            plot_rect.x = 720 - plot_rect.width // 2
            text_coord += plot_rect.height
            screen.blit(string_rendered, plot_rect)
        pygame.display.flip()
        clock.tick(FPS)


def open_final_window(screen, flag_end, sum_gold, sum_xp, lvl, sum_kill, time):
    if flag_end == 'win':
        text_end = 'Вы выиграли!!!'
    elif flag_end == 'lose':
        text_end = 'Вы погибли :c'
    else:
        text_end = 'Вы вышли'

    text_end = pygame.font.Font(None, 50).render(text_end, True, (51, 51, 51))
    text_gold = pygame.font.Font(None, 50).render('Сумма золота: ' + str(sum_gold), True, (51, 51, 51))
    text_xp = pygame.font.Font(None, 50).render('Сумма опыта: ' + str(sum_xp), True, (51, 51, 51))
    text_lvl = pygame.font.Font(None, 50).render('Ваш уровень: ' + str(lvl), True, (51, 51, 51))
    text_kill = pygame.font.Font(None, 50).render('Сумма убийств: ' + str(sum_kill), True, (51, 51, 51))
    text_time = pygame.font.Font(None, 50).render('Время в игре: ' + str(time // 60) + ' Минут', True, (51, 51, 51))
    text_score = pygame.font.Font(None, 50).render('Общий счет: ' + str(sum_xp + sum_gold + sum_kill + time // 1 + lvl),
                                                   True, (51, 51, 51))

    screen.fill((206, 206, 206))
    
    screen.blit(text_end, (600, 100))
    screen.blit(text_gold, (200, 300))
    screen.blit(text_xp, (200, 500))
    screen.blit(text_lvl, (600, 300))
    screen.blit(text_kill, (1000, 300))
    screen.blit(text_time, (1000, 500))
    screen.blit(text_score, (1000, 700))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
