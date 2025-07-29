import time
import pygame
import random
import datetime

from windows_image import *
from maps import *
from pers import *
from shells import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

start_screen(screen, clock)
window_with_text(screen, clock)
camera = Camera((40, 40))
tick = 0
txt_map = []
flag_attack = -1
specifications = Specifications()
flag_open_backpack = False
flag_open_specifications = False
flag_open_text = False
flag_open_shop = False
mobs = [Axolot(29, 27, 1, 1), Axolot(37, 25, 1, 1), Dragon(29, 34, 1, 1), Dragon(37, 31, 1, 1), Mole(33, 38, 1, 1),
        Mole(34, 38, 1, 1), Bamboo(48, 4, 1, 1), Bamboo(44, 15, 1, 1), Larva(53, 29, 1, 1), Larva(68, 36, 1, 1),
        Larva(77, 27, 1, 1), Eye(30, 45, 1, 1), Eye(27, 50, 1, 1), Cyclope(20, 60, 1, 1), Cyclope(1, 59, 1, 1),
        Cyclope(24, 78, 1, 1), Reptile(55, 48, 1, 1), Reptile(54, 57, 1, 1), Beast(43, 43, 1, 1), Beast(55, 75, 1, 1),
        Beast(75, 70, 1, 1)]

mobs_quest = [Inspector(20, 14), Villager(64, 13), Villager2(4, 75), OldMan(75, 50), Knight(39, 7), Knight(39, 6),
              Villager3(11, 75), Villager4(4, 65), Monk(27, 76), Master(44, 65), Villager3(67, 51), Villager4(63, 51),
              Monk(61, 77), Master(22, 7), Villager3(27, 14), Villager4(66, 18)]
active_mobs_quest = []
change_x, change_y = 0, 0
old_time = time.time()
new_time = time.time()
flag_end = ''

sum_kill, sum_gold, time_start_game = 0, 0, time.time()


with open('data/map.txt', 'r') as f:
    for line in f.readlines():
        one_line_in_map = ''
        for sim in line:
            if sim == '0':
                one_line_in_map += '0'
            elif sim == 'X':
                one_line_in_map += 'X'
        txt_map.append(list(one_line_in_map))


for mob in mobs:
    txt_map[mob.pos[1]][mob.pos[0]] = mob

for mob_quest in mobs_quest:
    txt_map[mob_quest.pos[1]][mob_quest.pos[0]] = mob_quest


def update_map(new_map):
    for i in range(len(new_map)):
        for j in range(len(new_map[0])):
            if new_map[i][j] == 'X':
                txt_map[i][j] = 'X'


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            flag_end = 'exit'
            break
        if event.type == pygame.KEYDOWN:
            print(event.type == pygame.KEYDOWN)
        if event.type == pygame.KEYDOWN and not flag_open_text and not flag_open_shop and not flag_open_specifications \
                and not flag_open_backpack:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.image = player.image = pygame.transform.scale(load_image('player_walk_up.png'), (48, 48))
                player.direction = 'up'
                if player.pos[1] != 0 and txt_map[player.pos[1] - 1][player.pos[0]] == '0':
                    player.move_hero()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.image = player.image = pygame.transform.scale(load_image('player_walk_down.png'), (48, 48))
                player.direction = 'down'
                if player.pos[1] != 79 and txt_map[player.pos[1] + 1][player.pos[0]] == '0':
                    player.move_hero()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.image = player.image = pygame.transform.scale(load_image('player_walk_left.png'), (48, 48))
                player.direction = 'left'
                if player.pos[0] != 0 and txt_map[player.pos[1]][player.pos[0] - 1] == '0':
                    player.move_hero()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.image = pygame.transform.scale(load_image('player_walk_right.png'), (48, 48))
                player.direction = 'right'
                if player.pos[0] != 79 and txt_map[player.pos[1]][player.pos[0] + 1] == '0':
                    player.move_hero()
            elif event.key == pygame.K_SPACE:
                player.image = eval(f"pygame.transform.scale(load_image('player_attack_{player.direction}.png'), "
                                    f"(48, 48))")
                flag_attack = 0
                x_attack, y_attack = player.get_pos_attack()
                if txt_map[y_attack][x_attack] != '0' and txt_map[y_attack][x_attack] != 'X':
                    mob = txt_map[y_attack][x_attack]
                    if mob.type == 'mob':
                        mob.retaliation(player.direction)
                        player.hp -= mob.attack
                        num_dodge = random.randint(0, 100)
                        if num_dodge > mob.dodge:
                            mob.hp -= player.attack
                            mob.health_bar.hp -= player.attack
                        if num_dodge > player.dodge:
                            player.hp -= mob.attack
                        if mob.hp <= 0:
                            for mob_quest in active_mobs_quest:
                                if mob.name == mob_quest.types[mob_quest.quest]:
                                    mob_quest.kill += 1
                                    if mob_quest.kill == mob_quest.required_kills[mob_quest.quest]:
                                        mob_quest.quest_finish = True

                            player_x, player_y = player.pos
                            mob_x, mob_y = mob.pos
                            txt_map[mob_y][mob_x] = '0'
                            mob.dead()
                            mob_x, mob_y = mob.pos
                            while (mob_x == player_x and mob_y == player_y) or (txt_map[mob_y][mob_x] != '0'):
                                mob.dead()
                                mob_x, mob_y = mob.pos
                            txt_map[mob_y][mob_x] = mob
                            player.experience += mob.xp
                            while player.experience >= player.required_experience_to_raise_the_level[player.lvl]:
                                player.lvl += 1
                                player.points_lvl += 1
                            player.gold += mob.gold
                            sum_gold += mob.gold
                            sum_kill += 1
                        mob.health_bar.update_bar()
            elif event.key == pygame.K_e:
                x_talk, y_talk = player.get_pos_attack()
                if txt_map[y_talk][x_talk] != '0' and txt_map[y_talk][x_talk] != 'X':
                    mob = txt_map[y_talk][x_talk]
                    if mob.type == 'quest_mob':
                        if not mob.quest_active and mob.max_quest != mob.quest + 1:
                            mob.quest_active = True
                            flag_open_text = True
                            quest_mob = mob
                            active_mobs_quest.append(mob)
                            player.gold += mob.reward_gold[mob.quest]
                            sum_gold += mob.reward_gold[mob.quest]
                            player.experience += mob.reward_gold[mob.quest]
                        if mob.quest_active and mob.quest_finish and mob.max_quest != mob.quest:
                            mob.quest_finish = False
                            mob.quest += 1
                            flag_open_text = True
                            quest_mob = mob
                            mob.kill = 0
                            player.gold += mob.reward_gold[mob.quest]
                            player.experience += mob.reward_gold[mob.quest]
                        while player.experience >= player.required_experience_to_raise_the_level[player.lvl]:
                            player.lvl += 1
                            player.points_lvl += 1
                if (x_talk == 30 and y_talk == 4) or (x_talk == 31 and y_talk == 4) or (x_talk == 32 and y_talk == 4) \
                        or (x_talk == 33 and y_talk == 4) or (x_talk == 5 and y_talk == 34):
                    flag_open_shop = True
                    num_shop = 1
                if (x_talk == 70 and y_talk == 4) or (x_talk == 69 and y_talk == 4):
                    flag_open_shop = True
                    num_shop = 2
                if (x_talk == 9 and y_talk == 64) or (x_talk == 10 and y_talk == 64) or (x_talk == 11 and y_talk == 64):
                    flag_open_shop = True
                    num_shop = 3
                if (x_talk == 61 and y_talk == 44) or (x_talk == 62 and y_talk == 44) or \
                        (x_talk == 63 and y_talk == 44):
                    flag_open_shop = True
                    num_shop = 4
            elif event.key == pygame.K_q:
                if player.mana >= 10:
                    player.mana -= 10
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
                    fireball.limit = 0
                    fireball.rect.x = 696
                    fireball.rect.y = 426
                    old_time = time.time()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if backpack.rect.x < x < backpack.rect.x + backpack.rect.width and \
                        backpack.rect.y < y < backpack.rect.y + backpack.rect.height:
                    flag_open_backpack = True
                elif specifications.rect.x < x < specifications.rect.x + specifications.rect.width and \
                        specifications.rect.y < y < specifications.rect.y + specifications.rect.height:
                    flag_open_specifications = True
                if flag_open_specifications and player.points_lvl and 390 < x < 430 and 160 < y < 200:
                    player.points_lvl -= 1
                    player.strength += 1
                    player.full_hp += 10
                    player.attack += 1
                if flag_open_specifications and player.points_lvl and 770 < x < 810 and 160 < y < 200:
                    player.points_lvl -= 1
                    player.agility += 1
                    player.dodge += 1
                    player.attack += 3
                if flag_open_specifications and player.points_lvl and 1150 < x < 1190 and 160 < y < 200:
                    player.points_lvl -= 1
                    player.intelligence += 1
                    player.full_mana += 10
                    player.magic_attack += 2
                if flag_open_specifications and 1296 < x < 1296 + 38 and 87 < y < 87 + 36:
                    flag_open_specifications = False
                if flag_open_backpack:
                    if 1296 < x < 1296 + 38 and 87 < y < 87 + 36:
                        flag_open_backpack = False
                    x_backpack, y_backpack = get_pos_in_backpack(x, y)
                    if x_backpack != -1 and y_backpack != -1 and x_backpack + y_backpack * 8 < len(backpack.items):
                        item = backpack.items[x_backpack + y_backpack * 8]
                        if item.image[:-1] == 'ring':
                            if backpack.active_ring:
                                player.attack -= backpack.active_ring.attack
                                player.full_mana -= backpack.active_ring.mana
                                player.magic_attack -= backpack.active_ring.magic_attack
                            backpack.active_ring = item
                            player.attack += item.attack
                            player.full_mana += item.mana
                            player.magic_attack += item.magic_attack
                        if item.image[:-1] == 'helmet':
                            if backpack.active_helmet:
                                player.attack -= backpack.active_helmet.attack
                                player.full_hp -= backpack.active_helmet.hp
                            backpack.active_helmet = item
                            player.attack += item.attack
                            player.full_hp += item.hp
                        if item.image[:-1] == 'chestplate':
                            if backpack.active_chestplate:
                                player.full_hp -= backpack.active_chestplate.hp
                            backpack.active_chestplate = item
                            player.full_hp += item.hp
                        if item.image[:-1] == 'boots':
                            if backpack.active_boots:
                                player.dodge -= backpack.active_boots.dodge
                                player.full_hp -= backpack.active_boots.hp
                            backpack.active_boots = item
                            player.dodge += item.dodge
                            player.full_hp += item.hp
                if flag_open_shop and 1296 < x < 1296 + 38 and 87 < y < 87 + 36:
                    flag_open_shop = False
                if flag_open_text and 1020 < x < 1020 + 750 and 750 < y < 750 + 40:
                    flag_open_text = False
                if flag_open_shop:
                    if 216 < x < 216 + 150 and 341 < y < 341 + 150 and player.gold >= rings[num_shop - 1].cost:
                        if not purchased_rings[num_shop - 1]:
                            backpack.items.append(rings[num_shop - 1])
                            player.gold -= rings[num_shop - 1].cost
                            purchased_rings[num_shop - 1] = True
                    elif 216 < x < 216 + 150 and 558 < y < 558 + 150 and player.gold >= helmets[num_shop - 1].cost:
                        if not purchased_helmets[num_shop - 1]:
                            backpack.items.append(helmets[num_shop - 1])
                            player.gold -= helmets[num_shop - 1].cost
                            purchased_helmets[num_shop - 1] = True
                    elif 766 < x < 766 + 150 and 341 < y < 341 + 150 and player.gold >= chestplates[num_shop - 1].cost:
                        if not purchased_chestplates[num_shop - 1]:
                            backpack.items.append(chestplates[num_shop - 1])
                            player.gold -= chestplates[num_shop - 1].cost
                            purchased_chestplates[num_shop - 1] = True
                    elif 766 < x < 766 + 150 and 558 < y < 558 + 150 and player.gold >= boots[num_shop - 1].cost:
                        if not purchased_boots[num_shop - 1]:
                            backpack.items.append(boots[num_shop - 1])
                            player.gold -= boots[num_shop - 1].cost
                            purchased_boots[num_shop - 1] = True
    if not running:
        break

    screen.fill((113, 221, 238))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    if mobs[4].full_hp == 3000 and len(active_mobs_quest) == 2 and active_mobs_quest[1].quest == \
            active_mobs_quest[1].max_quest:
        txt_map[38][33].full_hp = 30
        txt_map[38][33].hp = 30
        txt_map[38][33].health_bar.hp = 30
        txt_map[38][33].health_bar.update_bar()

        txt_map[38][34].full_hp = 30
        txt_map[38][34].hp = 30
        txt_map[38][34].health_bar.hp = 30
        txt_map[38][34].health_bar.update_bar()

    if txt_map[53][38] == 'X' and len(active_mobs_quest) == 3 and active_mobs_quest[2].quest == \
            active_mobs_quest[2].max_quest:
        txt_map[53][38] = '0'
        txt_map[53][39] = '0'
        txt_map[53][40] = '0'
        txt_map[53][41] = '0'
        background.image = pygame.transform.scale(load_image('rpg_map2.png', -1), (3840, 3840))

    if len(active_mobs_quest) == 4 and active_mobs_quest[3].quest == active_mobs_quest[3].max_quest - 1 and \
            not flag_open_text:
        flag_end = 'win'
        break

    if player.hp <= 0:
        flag_end = 'lose'
        break

    for mob in mobs:
        if pygame.sprite.collide_mask(fireball, mob):
            change_y, change_x = 0, 0
            fireball.limit = 30
            mob.hp -= player.magic_attack
            mob.health_bar.hp -= player.magic_attack
            if mob.hp <= 0:
                for mob_quest in active_mobs_quest:
                    if mob.name == mob_quest.types[mob_quest.quest]:
                        mob_quest.kill += 1
                        if mob_quest.kill == mob_quest.required_kills[mob_quest.quest]:
                            mob_quest.quest_finish = True

                player_x, player_y = player.pos
                mob_x, mob_y = mob.pos
                txt_map[mob_y][mob_x] = '0'
                mob.dead()
                mob_x, mob_y = mob.pos
                while (mob_x == player_x and mob_y == player_y) or (txt_map[mob_y][mob_x] != '0'):
                    mob.dead()
                    mob_x, mob_y = mob.pos
                txt_map[mob_y][mob_x] = mob
                player.experience += mob.xp
                while player.experience >= player.required_experience_to_raise_the_level[player.lvl]:
                    player.lvl += 1
                    player.points_lvl += 1
                player.gold += mob.gold
                sum_gold += mob.gold
                sum_kill += 1
            mob.health_bar.update_bar()

    new_time = time.time()
    if new_time - old_time > 0.01:
        old_time = time.time()
        fireball.update(change_x, change_y)

    background_group.draw(screen)
    all_sprites.draw(screen)
    mobs_group.draw(screen)
    pygame.draw.rect(screen, (80, 80, 80), (65, 5, 160, 20))
    pygame.draw.rect(screen, (255, 0, 0), (70, 10, 150 * (player.hp / player.full_hp), 10))
    pygame.draw.rect(screen, (80, 80, 80), (65, 25, 120, 20))
    pygame.draw.rect(screen, (0, 0, 255), (70, 30, 110 * (player.mana / player.full_mana), 10))
    pygame.draw.rect(screen, (80, 80, 80), (65, 45, 80, 20))
    pygame.draw.rect(screen, (255, 255, 51), (70, 50, 70 * ((player.experience -
                                                             player.required_experience_to_raise_the_level
                                                             [player.lvl - 1]) /
                                                            (player.required_experience_to_raise_the_level[player.lvl] -
                                                            player.required_experience_to_raise_the_level[player.lvl
                                                                                                          - 1])), 10))
    player_group.draw(screen)
    health_bars_group.draw(screen)
    fireball_group.draw(screen)
    screen.blit(player_icon, (10, 10))
    if mobs_quest[4] and mobs_quest[5] and active_mobs_quest and active_mobs_quest[0] and \
            active_mobs_quest[0].quest == active_mobs_quest[0].max_quest:
        mobs_quest[4].rect.y = 100000000
        mobs_quest[5].rect.y = 100000000
        txt_map[mobs_quest[4].pos[1]][mobs_quest[4].pos[0]] = '0'
        txt_map[mobs_quest[5].pos[1]][mobs_quest[4].pos[0]] = '0'
        mobs_quest[4] = None
        mobs_quest[5] = None

    if flag_open_specifications:
        open_specifications(screen)
    if flag_open_backpack:
        open_backpack(screen)
    if flag_open_text:
        quest_mob.open_text(screen)
    if flag_open_shop:
        open_shop(screen, num_shop)

    if flag_attack == 1:
        player.image = eval(f"pygame.transform.scale(load_image('player_walk_{player.direction}.png'), (48, 48))")
        flag_attack = -1

    pygame.display.flip()
    if flag_attack == 0:
        flag_attack += 1
        time.sleep(0.1)

open_final_window(screen, flag_end, sum_gold, player.experience, player.lvl, sum_kill, time.time() - time_start_game)
pygame.quit()
