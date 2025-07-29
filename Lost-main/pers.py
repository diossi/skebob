from items import *
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


class Background(pygame.sprite.Sprite):
    def __init__(self, background_name, pos_x, pos_y):
        super().__init__(background_group, all_sprites)
        self.image = load_image(background_name, -2)
        self.image = pygame.transform.scale(self.image, (3840, 3840))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Specifications(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = pygame.transform.scale(load_image('stats.png', -1), (50, 50))
        self.rect = self.image.get_rect().move(285, 5)


class Backpack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = pygame.transform.scale(load_image('backpack.png', -1), (60, 60))
        self.rect = self.image.get_rect().move(225, 0)
        self.items = []
        self.active_ring = None
        self.active_helmet = None
        self.active_chestplate = None
        self.active_boots = None


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)

        self.image = player_image
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.direction = 'up'

        self.hp = 100
        self.full_hp = 100
        self.mana = 10
        self.full_mana = 10

        self.magic_attack = 10
        self.attack = 2
        self.dodge = 10

        self.strength = 0
        self.agility = 0
        self.intelligence = 0

        self.experience = 0
        self.lvl = 1
        self.required_experience_to_raise_the_level = [0, 15, 50, 120, 260, 500, 1000]
        self.required_experience_to_raise_the_level.extend([10000 + 10000 * i for i in range(100)])
        self.points_lvl = 0

        self.gold = 0

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
        x, y = self.pos
        if (x == 19 and y == 5) or (x == 20 and y == 5) or (x == 21 and y == 4) or (x == 21 and y == 3) or \
                (x == 18 and y == 4) or (x == 18 and y == 3) or (x == 76 and y == 4) or (x == 76 and y == 5) or \
                (x == 8 and y == 67) or (x == 7 and y == 67) or (x == 6 and y == 68) or (x == 6 and y == 69) or \
                (x == 7 and y == 70) or (x == 8 and y == 70) or (x == 9 and y == 69) or (x == 9 and y == 68):
            self.hp = self.full_hp
            self.mana = self.full_mana

    def get_pos_attack(self):
        if self.direction == 'up':
            return self.pos[0], self.pos[1] - 1
        elif self.direction == 'down':
            return self.pos[0], self.pos[1] + 1
        elif self.direction == 'left':
            return self.pos[0] - 1, self.pos[1]
        elif self.direction == 'right':
            return self.pos[0] + 1, self.pos[1]


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, field_size):
        self.field_size = field_size
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = WIDTH // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = HEIGHT // 2 - (target.rect.y + target.rect.h // 2)


class Mob:
    def __init__(self, full_hp=10, attack=20, dodge=30, image='player_walk_up.png', x=10, y=10,
                 difference_x=1, difference_y=1, name='player_walk', xp=1, gold=2):
        super().__init__(mobs_group, all_sprites)
        self.full_hp = full_hp
        self.hp = self.full_hp
        self.attack = attack
        self.dodge = dodge
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(self.pos[0] * tile_width, self.pos[1] * tile_height)
        self.name = name
        self.spawn_pos = (x, y, difference_x, difference_y)
        self.xp = xp
        self.health_bar = HealthBarMob(self.full_hp, self.rect)
        self.gold = gold
        self.type = 'mob'

    def retaliation(self, direction):
        if direction == 'down':
            self.image = pygame.transform.scale(load_image(self.name + "_up.png"), (48, 48))
        elif direction == 'up':
            self.image = pygame.transform.scale(load_image(self.name + "_down.png"), (48, 48))
        elif direction == 'right':
            self.image = pygame.transform.scale(load_image(self.name + "_left.png"), (48, 48))
        elif direction == 'left':
            self.image = pygame.transform.scale(load_image(self.name + "_right.png"), (48, 48))

    def dead(self):
        spawn_x = self.spawn_pos[0]
        spawn_y = self.spawn_pos[1]
        random_x = random.randint(-self.spawn_pos[2], self.spawn_pos[2])
        random_y = random.randint(-self.spawn_pos[3], self.spawn_pos[3])
        while spawn_x + self.spawn_pos[2] < self.pos[0] + random_x \
                or self.pos[0] + random_x < spawn_x - self.spawn_pos[2]:
            random_x = random.randint(-self.spawn_pos[2], self.spawn_pos[2])
        while spawn_y + self.spawn_pos[3] < self.pos[1] + random_y \
                or self.pos[1] + random_y < spawn_y - self.spawn_pos[3]:
            random_y = random.randint(-self.spawn_pos[3], self.spawn_pos[3])

        self.pos = (self.pos[0] + random_x, self.pos[1] + random_y)
        self.rect.x += random_x * 48
        self.rect.y += random_y * 48
        self.health_bar.rect.x += random_x * 48
        self.health_bar.rect.y += random_y * 48
        self.health_bar.hp = self.full_hp
        self.image = pygame.transform.scale(load_image(self.name + "_down.png"), (48, 48))
        self.hp = self.full_hp


class HealthBarMob(pygame.sprite.Sprite):
    def __init__(self, hp, rect):
        super().__init__(health_bars_group, all_sprites)
        self.hp = hp
        self.image = pygame.font.SysFont(None, 20)
        self.image = self.image.render(str(self.hp), True, 'red', 'grey')
        self.rect = rect.copy()
        self.rect.y -= 20
        self.rect.x += 24

    def update_bar(self):
        self.image = (pygame.font.SysFont(None, 20)).render(str(self.hp), True, 'red', 'grey')


class Axolot(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=10, attack=2, dodge=5, image='axolot_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='axolot', xp=2, gold=2)


class Dragon(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=20, attack=4, dodge=10, image='dragon_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='dragon', xp=4, gold=4)


class Mole(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=3000, attack=6, dodge=10, image='mole_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='mole', xp=6, gold=6)


class Bamboo(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=50, attack=10, dodge=15, image='bamboo_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='bamboo', xp=10, gold=10)


class Larva(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=70, attack=12, dodge=15, image='larva_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='larva', xp=20, gold=20)


class Eye(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=100, attack=15, dodge=20, image='eye_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='eye', xp=30, gold=100)


class Cyclope(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=200, attack=30, dodge=25, image='cyclope_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='cyclope', xp=100, gold=150)


class Reptile(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=300, attack=40, dodge=30, image='reptile_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='reptile', xp=200, gold=200)


class Beast(Mob, pygame.sprite.Sprite):
    def __init__(self, x, y, difference_x, difference_y):
        super().__init__(full_hp=400, attack=50, dodge=30, image='beast_down.png', x=x, y=y,
                         difference_x=difference_x, difference_y=difference_y, name='beast', xp=300, gold=300)


class QuestMob:
    def __init__(self, image='inspector', x=10, y=10, texts=[], max_quest=1, required_kills=[],
                 types=[], reward_gold=[], reward_xp=[]):
        super().__init__(quest_mobs_group, all_sprites)
        self.image = pygame.transform.scale(load_image(image + '.png'), (48, 48))
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])
        self.texts = texts
        self.max_quest = max_quest
        self.types = types
        self.quest = 0
        self.required_kills = required_kills
        self.kill = 0
        self.type = 'quest_mob'
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.quest_active = False
        self.quest_finish = False

    def open_text(self, screen):
        screen.blit(dialog_text, (120, 600))
        text = pygame.font.SysFont(None, 30).render(self.texts[self.quest], True, 'black')
        screen.blit(text, (155, 665))
        pygame.draw.rect(screen, (131, 91, 81), (1020, 750, 250, 40))
        text2 = pygame.font.SysFont(None, 50).render('Понятно', True, 'black')
        screen.blit(text2, (1068, 756))


class Inspector(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(image='inspector', x=x, y=y,
                         texts=['Рядом с деревней есть странные существа. Убей 2 и получишь награду',
                                'Помоги убить других существа. Убей 2 и отзову тех рыцарей',
                                'Спасибо, ты очень помог нашей деревне'],
                         max_quest=2, required_kills=[2, 2, 0], types=['axolot', 'dragon', ''], reward_gold=[0, 10, 30],
                         reward_xp=[0, 10, 30])


class Villager(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('villager', x, y,
                         ['Рядом с нашей деревней есть зеленые существа. Убей 3 и получишь награду',
                          'Помоги убить других существа с этой локации. Убей 2 и тебе откроется доступ на 3 локацию',
                          'Спасибо за помощь!'],
                         2, [3, 2, 0], ['bamboo', 'larva', ''], [0, 100, 200], [0, 100, 200])


class Villager2(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('villager2', x, y,
                         ['Рядом с нашей деревней есть голубые существа. Убей 3 и получишь награду',
                          'Помоги убить других существа с этой локации. Убей 2 и я построю мост через реку',
                          'Спасибо за помощь!'],
                         2, [3, 2, 0], ['eye', 'cyclope', ''], [0, 500, 1000], [0, 500, 1000])


class OldMan(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('oldman', x, y,
                         ['Убей 10 драконов которые пробрались в замок и помогу вернуться тебе в твой мир',
                          'Спасибо тебе, за это я отправлю тебя в твой мир!'],
                         2, [10, 0], ['beast', ''], [0, 0], [0, 0])


class Villager3(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('villager3', x, y)


class Villager4(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('villager4', x, y)


class Monk(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('monk', x, y)


class Master(QuestMob, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__('master', x, y)


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(quest_mobs_group, all_sprites)
        self.image = pygame.transform.scale(load_image('knight.png', -1), (48, 48))
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(self.pos[0] * tile_width, self.pos[1] * tile_height)
        self.type = 'stay_mob'


def open_backpack(screen):
    pygame.draw.rect(screen, (206, 206, 206), (150, 125, 1140, 650))
    pygame.draw.rect(screen, (0, 0, 0), (150, 125, 1140, 650), 5)
    pygame.draw.line(screen, (255, 0, 0), (1298, 122), (1332, 88), 7)
    pygame.draw.line(screen, (255, 0, 0), (1298, 88), (1332, 122), 6)

    text_hp = pygame.font.SysFont(None, 35).render("Хп: " + str(player.hp), True, "black")
    text_mana = pygame.font.SysFont(None, 35).render("Мана: " + str(player.mana), True, "black")
    text_attack = pygame.font.SysFont(None, 35).render("Атака: " + str(player.attack), True, "black")
    text_magic_attack = pygame.font.SysFont(None, 35).render("Магическая атака: " + str(player.magic_attack),
                                                             True, "black")
    text_dodge = pygame.font.SysFont(None, 35).render("Уворот: " + str(player.dodge), True, "black")

    screen.blit(text_hp, (695, 135))
    screen.blit(text_mana, (695, 163))
    screen.blit(text_attack, (695, 191))
    screen.blit(text_magic_attack, (695, 219))
    screen.blit(text_dodge, (695, 247))

    for j in range(8):
        if j < 5:
            pygame.draw.line(screen, (0, 0, 0), (150, 275 + 100 * j), (950, 275 + 100 * j), 4)
        if j == 7:
            pygame.draw.line(screen, (0, 0, 0), (150 + (j + 1) * 100, 125), (150 + (j + 1) * 100, 774), 4)
        else:
            pygame.draw.line(screen, (0, 0, 0), (150 + (j + 1) * 100, 275), (150 + (j + 1) * 100, 774), 4)
        if j < 4:
            pygame.draw.rect(screen, (0, 0, 0), (975, 150 + 166 * j, 100, 100), 4)
            if backpack.active_ring and j == 0:
                image_active_ring = pygame.transform.scale(load_image(backpack.active_ring.image + '.png'), (92, 92))
                screen.blit(image_active_ring, (979, 154 + 166 * j))

                text_ring1 = pygame.font.SysFont(None, 30).render("Бонус к мане: " + str(backpack.active_ring.mana),
                                                                  True, "black")
                text_ring2 = pygame.font.SysFont(None, 30).render("Бонус к атаке: " + str(backpack.active_ring.attack),
                                                                  True, "black")
                text_ring3 = pygame.font.SysFont(None, 30).render("Бонус к магической", True, "black")
                text_ring4 = pygame.font.SysFont(None, 30).render("атаке: " + str(backpack.active_ring.magic_attack),
                                                                  True, "black")

                screen.blit(text_ring1, (1085, 154 + 166 * j + 1))
                screen.blit(text_ring2, (1085, 154 + 166 * j + 26))
                screen.blit(text_ring3, (1085, 154 + 166 * j + 51))
                screen.blit(text_ring4, (1085, 154 + 166 * j + 76))

            if backpack.active_helmet and j == 1:
                image_active_helmet = pygame.transform.scale(load_image(backpack.active_helmet.image + '.png'),
                                                             (92, 92))
                screen.blit(image_active_helmet, (979, 154 + 166 * j))

                text_ring1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + str(backpack.active_helmet.hp),
                                                                  True, "black")
                text_ring2 = pygame.font.SysFont(None, 30).render("Бонус к атаке: " +
                                                                  str(backpack.active_helmet.attack), True, "black")

                screen.blit(text_ring1, (1085, 154 + 166 * j + 1))
                screen.blit(text_ring2, (1085, 154 + 166 * j + 26))

            if backpack.active_chestplate and j == 2:
                image_active_chestplate = pygame.transform.scale(load_image(backpack.active_chestplate.image + '.png'),
                                                                 (92, 92))
                screen.blit(image_active_chestplate, (979, 154 + 166 * j))

                text_ring1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + str(backpack.active_chestplate.hp),
                                                                  True, "black")

                screen.blit(text_ring1, (1085, 154 + 166 * j + 1))

            if backpack.active_boots and j == 3:
                image_active_boots = pygame.transform.scale(load_image(backpack.active_boots.image + '.png'), (92, 92))
                screen.blit(image_active_boots, (979, 154 + 166 * j))

                text_ring1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + str(backpack.active_boots.hp),
                                                                  True, "black")
                text_ring2 = pygame.font.SysFont(None, 30).render("Бонус к увороту: " +
                                                                  str(backpack.active_boots.dodge), True, "black")

                screen.blit(text_ring1, (1085, 154 + 166 * j + 1))
                screen.blit(text_ring2, (1085, 154 + 166 * j + 26))

    image_gold = pygame.font.SysFont(None, 100).render('Золото: ' + str(player.gold), True, 'black', (206, 206, 206))
    screen.blit(image_gold, (200, 170))

    items_in_backpack = len(backpack.items)

    count_items = 0
    for i in range(5):
        for j in range(8):
            if count_items == items_in_backpack:
                break
            count_items += 1
            exec(f'image_item{i}{j} = pygame.transform.scale(load_image(backpack.items[8 * i + j].image + ".png", -1), '
                 f'(92, 92))')
            exec(f'screen.blit(image_item{i}{j}, (154 + 100 * j, 279 + 100 * i))')
        if count_items == items_in_backpack:
            break


def open_specifications(screen):
    pygame.draw.rect(screen, (206, 206, 206), (150, 125, 1140, 650))
    pygame.draw.rect(screen, (0, 0, 0), (150, 125, 1140, 650), 5)
    pygame.draw.rect(screen, (0, 0, 0), (530, 125, 760, 436), 5)
    pygame.draw.rect(screen, (0, 0, 0), (910, 125, 380, 436), 5)
    pygame.draw.line(screen, (0, 0, 0), (150, 558), (1290, 558), 5)
    pygame.draw.line(screen, (255, 0, 0), (1298, 122), (1332, 88), 7)
    pygame.draw.line(screen, (255, 0, 0), (1298, 88), (1332, 122), 6)

    image_num_strength = pygame.font.SysFont(None, 50).render(str(player.strength), True, 'black', (206, 206, 206))
    image_num_agility = pygame.font.SysFont(None, 50).render(str(player.agility), True, 'black', (206, 206, 206))
    image_num_intelligence = pygame.font.SysFont(None, 50).render(str(player.intelligence), True, 'black',
                                                                  (206, 206, 206))
    screen.blit(image_num_strength, (350 - (image_num_strength.get_width() // 2), 215))
    screen.blit(image_num_agility, (730 - (image_num_agility.get_width() // 2), 215))
    screen.blit(image_num_intelligence, (1110 - (image_num_intelligence.get_width() // 2), 215))

    image_num_lvl = pygame.font.SysFont(None, 50).render(str(player.lvl), True, 'black', (206, 206, 206))
    screen.blit(image_num_lvl, (720 - (image_num_lvl.get_width() // 2), 570))

    pygame.draw.rect(screen, (255, 255, 51), (250, 650, 940 * ((player.experience -
                                                                player.required_experience_to_raise_the_level
                                                                [player.lvl - 1]) /
                                                               (player.required_experience_to_raise_the_level
                                                                [player.lvl] -
                                                                player.required_experience_to_raise_the_level
                                                                [player.lvl - 1])), 50))
    pygame.draw.rect(screen, (0, 0, 0), (250, 650, 940, 50), 3)

    image_num_experience = pygame.font.SysFont(None, 50).render(str(player.experience -
                                                                    player.required_experience_to_raise_the_level
                                                                    [player.lvl - 1]) + ' /', True, 'black')
    image_num_required_experience = pygame.font.SysFont(None, 50).render(
        str(player.required_experience_to_raise_the_level[player.lvl] -
            player.required_experience_to_raise_the_level[player.lvl - 1]), True, 'black')
    screen.blit(image_num_experience, (725 - image_num_experience.get_width(), 660))
    screen.blit(image_num_required_experience, (690 + image_num_required_experience.get_width(), 660))

    image_bonus_strength_1 = pygame.font.SysFont(None, 20).render('Бонус к хп: ' + str(player.strength * 10), True,
                                                                  'black')
    image_bonus_strength_2 = pygame.font.SysFont(None, 20).render('Бонус к атаке: ' + str(player.strength), True,
                                                                  'black')
    screen.blit(image_bonus_strength_1, (200, 280))
    screen.blit(image_bonus_strength_2, (400, 280))

    image_bonus_agility_1 = pygame.font.SysFont(None, 20).render('Бонус к увороту: ' + str(player.agility), True,
                                                                 'black')
    image_bonus_agility_2 = pygame.font.SysFont(None, 20).render('Бонус к атаке: ' + str(player.agility * 3), True,
                                                                 'black')
    screen.blit(image_bonus_agility_1, (580, 280))
    screen.blit(image_bonus_agility_2, (780, 280))

    image_bonus_intelligence_1 = pygame.font.SysFont(None, 20).render('Бонус к мане: ' + str(player.intelligence * 10),
                                                                      True, 'black')
    image_bonus_intelligence_2 = pygame.font.SysFont(None, 20).render('Бонус к атаке магией: ' +
                                                                      str(player.intelligence * 2), True, 'black')
    screen.blit(image_bonus_intelligence_1, (960, 280))
    screen.blit(image_bonus_intelligence_2, (1120, 280))
    screen.blit(strength_icon, (315, 145))
    screen.blit(agility_icon, (695, 145))
    screen.blit(intelligence_icon, (1075, 145))

    for i in range(3):
        pygame.draw.rect(screen, (0, 0, 0), (390 + 380 * i, 175, 40, 10))
        pygame.draw.rect(screen, (0, 0, 0), (405 + 380 * i, 160, 10, 40))


def open_shop(screen, num_shop):

    pygame.draw.rect(screen, (206, 206, 206), (150, 125, 1140, 650))
    pygame.draw.rect(screen, (0, 0, 0), (150, 125, 1140, 650), 5)
    pygame.draw.line(screen, (255, 0, 0), (1298, 122), (1332, 88), 7)
    pygame.draw.line(screen, (255, 0, 0), (1298, 88), (1332, 122), 6)
    pygame.draw.line(screen, (0, 0, 0), (150, 275), (1289, 275), 4)
    image_gold = pygame.font.SysFont(None, 100).render('Золото: ' + str(player.gold), True, 'black')
    screen.blit(image_gold, (300, 170))

    for i in range(2):
        pygame.draw.rect(screen, (0, 0, 0), (216 + 550 * i, 341, 150, 150), 4)
        pygame.draw.rect(screen, (0, 0, 0), (216 + 550 * i, 558, 150, 150), 4)

    exec(f'image_item1 = pygame.transform.scale(load_image("ring{num_shop}.png"), (150, 150))')
    exec(f'image_item2 = pygame.transform.scale(load_image("helmet{num_shop}.png"), (150, 150))')
    if num_shop == 1 or num_shop == 4:
        exec(f'image_item3 = pygame.transform.scale(load_image("chestplate{num_shop}.png"), (150, 150))')
    exec(f'image_item4 = pygame.transform.scale(load_image("boots{num_shop}.png"), (150, 150))')

    exec(f'text_cost_ring = pygame.font.SysFont(None, 30).render("Цена: " + '
         f'str(rings[{num_shop - 1}].cost), True, "black")')
    exec(f'text_cost_helmet = pygame.font.SysFont(None, 30).render("Цена: " + '
         f'str(helmets[{num_shop - 1}].cost), True, "black")')
    if num_shop == 1 or num_shop == 4:
        exec(f'text_cost_chestplate = pygame.font.SysFont(None, 30).render("Цена: " + '
             f'str(chestplates[{num_shop - 1}].cost), True, "black")')
    exec(f'text_cost_boots = pygame.font.SysFont(None, 30).render("Цена: " + '
         f'str(boots[{num_shop - 1}].cost), True, "black")')

    exec(f'screen.blit(text_cost_ring, (376, 471))')
    exec(f'screen.blit(text_cost_helmet, (376, 688))')
    if num_shop == 1 or num_shop == 4:
        exec(f'screen.blit(text_cost_chestplate, (926, 471))')
    exec(f'screen.blit(text_cost_boots, (926, 688))')

    exec(f'text_ring1 = pygame.font.SysFont(None, 30).render("Бонус к мане: " + '
         f'str(rings[{num_shop - 1}].mana), True, "black")')
    exec(f'text_ring2 = pygame.font.SysFont(None, 30).render("Бонус к атаке: " + '
         f'str(rings[{num_shop - 1}].attack), True, "black")')
    exec(f'text_ring3 = pygame.font.SysFont(None, 30).render("Бонус к магической атаке: " + '
         f'str(rings[{num_shop - 1}].magic_attack), True, "black")')

    exec(f'text_helmet1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + '
         f'str(helmets[{num_shop - 1}].hp), True, "black")')
    exec(f'text_helmet2 = pygame.font.SysFont(None, 30).render("Бонус к атаке: " + '
         f'str(helmets[{num_shop - 1}].attack), True, "black")')

    if num_shop == 1 or num_shop == 4:
        exec(f'text_chestplate1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + '
             f'str(chestplates[{num_shop - 1}].hp), True, "black")')

    exec(f'text_boots1 = pygame.font.SysFont(None, 30).render("Бонус к хп: " + '
         f'str(boots[{num_shop - 1}].hp), True, "black")')
    exec(f'text_boots2 = pygame.font.SysFont(None, 30).render("Бонус к увороту: " + '
         f'str(boots[{num_shop - 1}].dodge), True, "black")')

    exec(f'screen.blit(text_helmet1, (376, 559))')
    exec(f'screen.blit(text_helmet2, (376, 584))')

    if num_shop == 1 or num_shop == 4:
        exec(f'screen.blit(text_chestplate1, (926, 342))')

    exec(f'screen.blit(text_boots1, (926, 559))')
    exec(f'screen.blit(text_boots2, (926, 584))')

    exec(f'screen.blit(text_ring1, (376, 342))')
    exec(f'screen.blit(text_ring2, (376, 367))')
    exec(f'screen.blit(text_ring3, (376, 392))')

    exec(f'screen.blit(image_item1, (216, 341))')
    exec(f'screen.blit(image_item2, (216, 558))')
    if num_shop == 1 or num_shop == 4:
        exec(f'screen.blit(image_item3, (766, 341))')
    exec(f'screen.blit(image_item4, (766, 558))')


def get_pos_in_backpack(x, y):
    start_x_backpack, start_y_backpack = 150, 275
    if 800 > x - start_x_backpack > 0 and 500 > y - start_y_backpack > 0:
        return (x - start_x_backpack) // 100, (y - start_y_backpack) // 100
    return -1, -1


move_hero = 48
tile_width, tile_height = 48, 48

player_image = load_image('player_walk_up.png', -1)
all_sprites = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
quest_mobs_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
health_bars_group = pygame.sprite.Group()
tile_images = {}
background = Background('rpg_map1.png', 0, 0)
player = Player(5, 35)
player_icon = load_image('player_icon.png', -2)
player_icon = pygame.transform.scale(player_icon, (50, 50))
strength_icon = pygame.transform.scale(load_image('strength.png', -1), (70, 70))
agility_icon = pygame.transform.scale(load_image('agility.png', -1), (70, 70))
intelligence_icon = pygame.transform.scale(load_image('intelligence.png', -1), (70, 70))
dialog_text = pygame.transform.scale(load_image('dialog_window.png', -1), (300 * 4, 58 * 4))
backpack = Backpack()
