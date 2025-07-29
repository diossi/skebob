import pygame

pygame.init()


class Item:
    def __init__(self, hp=0, dodge=0, mana=0, magic_attack=0, attack=0, cost=10, image='boots2'):
        self.hp = hp
        self.dodge = dodge
        self.mana = mana
        self.magic_attack = magic_attack
        self.attack = attack
        self.image = image
        self.cost = cost


class RingSilver1(Item):
    def __init__(self):
        super().__init__(attack=5, mana=20, magic_attack=10, cost=10, image='ring1')


class RingSilver2(Item):
    def __init__(self):
        super().__init__(attack=20, mana=50, magic_attack=30, cost=50, image='ring2')


class RingGold1(Item):
    def __init__(self):
        super().__init__(attack=40, mana=100, magic_attack=50, cost=200, image='ring3')


class RingGold2(Item):
    def __init__(self):
        super().__init__(attack=200, mana=500, magic_attack=250, cost=500, image='ring4')


class Helmet1(Item):
    def __init__(self):
        super().__init__(attack=5, hp=50, cost=10, image='helmet1')


class Helmet2(Item):
    def __init__(self):
        super().__init__(attack=10, hp=100, cost=50, image='helmet2')


class Helmet3(Item):
    def __init__(self):
        super().__init__(attack=20, hp=200, cost=300, image='helmet3')


class Helmet4(Item):
    def __init__(self):
        super().__init__(attack=50, hp=500, cost=600, image='helmet4')


class ChestPlate1(Item):
    def __init__(self):
        super().__init__(hp=100, cost=10, image='chestplate1')


class ChestPlate4(Item):
    def __init__(self):
        super().__init__(hp=800, cost=1000, image='chestplate4')


class Boots1(Item):
    def __init__(self):
        super().__init__(hp=50, dodge=10, cost=10, image='boots1')


class Boots2(Item):
    def __init__(self):
        super().__init__(hp=100, dodge=15, cost=100, image='boots2')


class Boots3(Item):
    def __init__(self):
        super().__init__(hp=200, dodge=20, cost=300, image='boots3')


class Boots4(Item):
    def __init__(self):
        super().__init__(hp=500, dodge=30, cost=600, image='boots4')


rings = [RingSilver1(), RingSilver2(), RingGold1(), RingGold2()]
helmets = [Helmet1(), Helmet2(), Helmet3(), Helmet4()]
chestplates = [ChestPlate1(), '', '', ChestPlate4()]
boots = [Boots1(), Boots2(), Boots3(), Boots4()]

purchased_rings = [False, False, False, False]
purchased_helmets = [False, False, False, False]
purchased_chestplates = [False, False, False, False]
purchased_boots = [False, False, False, False]
