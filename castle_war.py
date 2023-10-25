import pygame as pg
import math
import collections
from Save_spec import *
import os.path

# The code is divided into 6 main part divided into:
# LOAD OF IMAGE (line 16-91);
# CONSTANT (97-176)
# CLASSES (203-1005)
# INSTANCE OF CLASSES (1008-1045)
# FUNCTION (1071-1507)
# MAIN LOOP (1511-1600)

# initialize pygame, font and mixer:
pg.init()
pg.font.init()
pg.mixer.init()

# LOAD IMAGE:

# load image of building of player 1:
WALL_IMAGE_P1 = pg.image.load('sprites/player1/building/wall.png')
TOWER_IMAGE_P1 = pg.image.load('sprites/player1/building/tower.png')
BARRACKS_IMAGE_P1 = pg.image.load('sprites/player1/building/barracks.png')
MINE_IMAGE_P1 = pg.image.load('sprites/player1/building/mine.png')

# load image of building of player 2:
WALL_IMAGE_P2 = pg.image.load('sprites/player2/building/wall.png')
TOWER_IMAGE_P2 = pg.image.load('sprites/player2/building/tower.png')
BARRACKS_IMAGE_P2 = pg.image.load('sprites/player2/building/barracks.png')
MINE_IMAGE_P2 = pg.image.load('sprites/player2/building/mine.png')

# load image of Units:
# list of all type of units (that correspond to a folder)
units_types = ['sword', 'worker', 'bow', 'bow']

# list of tuple with action and corresponding number of frame
animation_types_sword = [('run', 12), ('attack', 8), ('fallen', 6)]
animation_types_worker = [('run', 6), ('dig', 9), ('repair', 4)]
animation_types_archer = [('run', 12), ('shoot', 2), ('fallen', 6)]
animation_types_arrow = [('arrowdiag', 2), ('arrowhor', 2), ('arrowvert', 2)]
animation_types_all = [animation_types_sword, animation_types_worker, animation_types_archer, animation_types_arrow]

# lists that contain images of units
units_animations_player1 = []
units_animations_player2 = []

# iterate for all types of units and load the image of corresponding action and frames:
for i in range(1, 3):
    count = 0
    # iterate for every type of units:
    for animation_type in animation_types_all:
        animation_list = []
        # iterate for every action of a unit:
        for tuples in animation_type:
            temp_list = []
            # iterate for every frame:
            for frame in range(tuples[1]):
                img = pg.image.load(f'sprites/player{i}/{units_types[count]}/{tuples[0]}-{frame}.png')  # load images
                temp_list.append(img)
            animation_list.append(temp_list)
        # add image to the corresponding player:
        if i == 1:
            units_animations_player1.append(animation_list)
        elif i == 2:
            units_animations_player2.append(animation_list)
        count += 1

# add images of worker that run to the mine (obtained by mirror the image of run):
running_to_mine_p1 = []
running_to_mine_p2 = []
# for player 1:
for image in units_animations_player1[1][0]:  # image of running worker
    # flip image
    image = pg.transform.flip(image, True, False)
    running_to_mine_p1.append(image)
units_animations_player1[1].insert(1, running_to_mine_p1)
# image of player 2:
for image in units_animations_player2[1][0]:  # image of running worker:
    image = pg.transform.flip(image, True, False)
    running_to_mine_p2.append(image)
units_animations_player2[1].insert(1, running_to_mine_p2)

# mirror images of worker digging:
dig_animation_p1 = []
dig_animation_p2 = []
# image of player 1:
for image in units_animations_player1[1][2]:
    image = pg.transform.flip(image, True, False)
    dig_animation_p1.append(image)
units_animations_player1[1][2] = dig_animation_p1
# image of player 2:
for image in units_animations_player2[1][2]:
    image = pg.transform.flip(image, True, False)
    dig_animation_p2.append(image)
units_animations_player2[1][2] = dig_animation_p2

# CONSTANT:

# dimension of the screen:
SCREEN_HEIGHT = 250
SCREEN_WIDTH = 1000

# dimension and value of buildings and ground:
GROUND_HEIGHT = 14
GROUND_WIDTH = SCREEN_WIDTH

MINE_HEIGHT = 37
MINE_WIDTH = 58
MINE_POS = 40
MINE2_POS = SCREEN_WIDTH - MINE_POS

BARRACKS_HEIGHT = 50
BARRACKS_WIDTH = 62
BARRACKS_POS = 106

WALL_HEIGHT = 80
WALL_WIDTH = 62
WALL_POS = 180
WALL_HEALTH = 1000
WALL_P1_RIGHT = 211
WALL_P2_LEFT = 851

TOWER_HEIGHT = 160
TOWER_WIDTH = TOWER_IMAGE_P1.get_width()  # tower height  found from the image
TOWER_RANGE = 220
TOWER_REST = 50  # amount of turns of inactivity of the tower after shooting
TOWER_HIT = 5

# Units constant:
UNIT_TRAIN = 80  # amount of turn amount of turns to train a unit
# Worker
WORKER_COST = 1  # amount of resources to train a new worker
WORKER_TRAIN = 80  # amount of turns to train a new worker
WORKER_SPEED = 2  # distance covered in one turn by a running worker
WORKER_PROD = 1  # amount of resources per turn mined by a worker in mine
WORKER_REPAIR = 1  # amount of HP restored per turn by a worker in wall

# Swordsman
SWORD_COST = 5  # amount of resources to train a new swordsman
SWORD_TRAIN = 80  # amount of turns to train a new swordsman
SWORD_SPEED = 4  # distance covered in one turn by a running swordsman
SWORD_RANGE = 10  # maximum distance at which a swordsman can hit a unit
SWORD_HIT = 2  # damage caused by of a swordsman per turn
SWORD_REST = 10  # amount of turns of inactivity of a swordsman after an attack
SWORD_HEALTH = 30  # initial amount of HP of a swordsman

# Archer
ARCHER_COST = 3  # amount of resources to train a new archer
ARCHER_TRAIN = 80  # amount of turns to train a new archer
ARCHER_SPEED = 5  # distance covered in one turn by a running archer
ARCHER_RANGE = 100  # maximum distance at which an archer can send an arrow
ARCHER_REST = 15  # amount of turns of inactivity of an archer after shooting
ARCHER_HEALTH = 20  # initial amount of HP of an archer
ARCHER_HIT = 1  # damage caused by of an arrow shoot by an archer

# Arrow
ARROW_SPEED = 15  # distance covered in one turn by an arrow
ARCHER_ARROW_SPEED = 10  # distance covered in one turn by an archer's arrow
# ARROW_REST = 10  # amount of turns of inactivity the tower after an attack

# define the starting resources:
INIT_RESOURCE = 10
RESOURCE_P1 = INIT_RESOURCE
RESOURCE_P2 = INIT_RESOURCE

# create background:
GROUND = pg.rect.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, 1000, 14)
BACKGROUND = pg.rect.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# list of common unit's constant (swordsman, worker, archer):
units_health = [30, 0, 20]
units_cost = [5, 1, 5]
units_train = [20, 10, 20]
units_speed = [SWORD_SPEED, WORKER_SPEED, ARCHER_SPEED]
delay_animation = [40, 90]  # run, other action

# display of the screen:
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# title:
pg.display.set_caption('Castle War')

# add icon:
icon = pg.image.load('castle.png')
# display an icon near the title
pg.display.set_icon(icon)

# define Win sound:
WIN_SOUND = pg.mixer.Sound(os.path.join('win_sound.mp3'))

# define FPS:
clock = pg.time.Clock()
FPS = 60
# turn duration is equivalent to duration of one frame
TURN_DURATION = (1/FPS)*1000

# Variable that regulate playing and pause:
play = True
pause = False


# DEFINE CLASSES:

# define the buildings classes (wall and tower):
class Mine:
    def __init__(self, player):
        self.player = player
        self.resources = INIT_RESOURCE

    # visualize resources continuously
    def update(self):
        self.visualize_resources()

    # display current resources on screen
    def visualize_resources(self):
        if self.player == 1:
            # visualize resources of player 1
            resource_game_p1 = FONT.render('Resource: ' + str(self.resources), True, (255, 255, 255))
            SCREEN.blit(resource_game_p1, (20, 20))
        elif self.player == 2:
            # visualize resources hp of player 2
            resource_game_p2 = FONT.render('Resource: ' + str(self.resources), True, (255, 255, 255))
            SCREEN.blit(resource_game_p2, (SCREEN_WIDTH - resource_game_p2.get_width() - 20, 20))


class Barrack:
    def __init__(self, player, init_work, init_sword, init_arch):
        self.player = player
        # lists of trained unit:
        self.trained_units = []
        self.train_swordsman = []
        self.train_worker = []
        self.worker_mine = []
        self.worker_tower = []
        self.train_archer = []
        # group of dispatched sprite:
        self.unit_group = pg.sprite.Group()
        # lists of initial units in barrack:
        self.init_work = init_work
        self.init_sword = init_sword
        self.init_arch = init_arch
        # lists of dispatched units
        self.swordsman_active = []
        self.archer_active = []
        self.active_arrow = []
        # variable to keep track of time
        self.up_time = pg.time.get_ticks()
        # delay of dispatched unit when dispatched all together
        self.delay_time = 2 * TURN_DURATION
        # time needed to train a unit
        self.time_train_unit = UNIT_TRAIN*TURN_DURATION
        self.time_train = pg.time.get_ticks()
        # track the availability of the barrack:
        self.empty = True

    # crate new worker
    def new_worker(self):
        if self.player == 1:
            new_worker = Worker(units_health[1], units_cost[1], units_train[1], units_speed[1],
                                units_animations_player1[1],
                                initial_position_p1[0], initial_position_p1[1], 1)

        elif self.player == 2:
            new_worker = Worker(units_health[1], units_cost[1], units_train[1], units_speed[1],
                                units_animations_player2[1],
                                initial_position_p2[0], initial_position_p2[1], 2)
        return new_worker

    # crate new swordsman
    def new_swordsman(self):
        if self.player == 1:
            new_swordsman = Swordsman(units_health[0], units_cost[0], units_train[0], units_speed[0],
                                      units_animations_player1[0],
                                      initial_position_p1[0], initial_position_p1[1], 1)
        elif self.player == 2:
            new_swordsman = Swordsman(units_health[0], units_cost[0], units_train[0], units_speed[0],
                                      units_animations_player2[0],
                                      initial_position_p2[0], initial_position_p2[1], 2)
        return new_swordsman

    # crate new archer
    def new_archer(self):
        if self.player == 1:
            new_archer = Archer(units_health[2], units_cost[2], units_train[2], units_speed[2],
                                units_animations_player1[2],
                                initial_position_p1[0], initial_position_p1[1] - 2, 1)
        elif self.player == 2:
            new_archer = Archer(units_health[2], units_cost[2], units_train[2], units_speed[2],
                                units_animations_player2[2],
                                initial_position_p2[0], initial_position_p2[1] - 2, 2)
        return new_archer

    # crate new worker, add to trained units lists  and set barracks to occupied
    def add_worker(self):
        if self.player == 1:
            new_worker = self.new_worker()
            self.train_worker.append(new_worker)
            self.trained_units.append(new_worker)
        elif self.player == 2:
            new_worker = self.new_worker()
            self.train_worker.append(new_worker)
            self.trained_units.append(new_worker)
        self.empty = False

    # crate new swordsman, add to trained units lists  and set barracks to occupied
    def add_swordsman(self):
        if self.player == 1:
            new_swordsman = self.new_swordsman()
            self.train_swordsman.append(new_swordsman)
            self.trained_units.append(new_swordsman)
        elif self.player == 2:
            new_swordsman = self.new_swordsman()
            self.train_swordsman.append(new_swordsman)
            self.trained_units.append(new_swordsman)
        self.empty = False

    # crate new archer, add to trained units lists  and set barracks to occupied
    def add_archer(self):
        if self.player == 1:
            new_archer = self.new_archer()
            self.train_archer.append(new_archer)
            self.trained_units.append(new_archer)
        elif self.player == 2:
            new_archer = self.new_archer()
            self.train_archer.append(new_archer)
            self.trained_units.append(new_archer)
        self.empty = False

    # check if the barrack is occupied
    def barracks_available(self):
        new_font = pg.font.SysFont('comic sans', 15)
        # if the barrack is occupied visualize a hint into the screen:
        if self.player == 1 and self.empty is False:
            pg.draw.rect(SCREEN, (255, 0, 0), (85, 150, 55, 10))
            write_on_screen('OCCUPIED', '', 85, 150, (255, 255, 255), new_font)
        elif self.player == 2 and self.empty is False:
            pg.draw.rect(SCREEN, (255, 0, 0), (870, 150, 55, 10))
            write_on_screen('OCCUPIED', '', 870, 150, (255, 255, 255), new_font)

    # initialize unit in the barracks
    def initialize_unit(self):
        for worker in range(self.init_work):
            self.add_worker()
        for swordsman in range(self.init_sword):
            self.add_swordsman()
        for archer in range(self.init_arch):
            self.add_archer()

    # check if barracks is available
    def update(self):
        self.barracks_available()
        if self.empty is False:
            if pg.time.get_ticks() - self.time_train > self.time_train_unit:
                self.empty = True
                self.time_train = pg.time.get_ticks()

    # train units using keyboard commands
    def train_units(self):
        # check if barrack is available
        if self.empty is True:
            # train commands for player 1:
            # check if player press training keyboard and (if has enough resources) train unit and subtract resources
            if self.player == 1:
                if event.key == pg.K_q and mine_p1.resources >= WORKER_COST:
                    self.add_worker()
                    mine_p1.resources -= WORKER_COST
                if event.key == pg.K_w and mine_p1.resources >= SWORD_COST:
                    self.add_swordsman()
                    mine_p1.resources -= SWORD_COST
                if event.key == pg.K_e and mine_p1.resources >= ARCHER_COST:
                    self.add_archer()
                    mine_p1.resources -= ARCHER_COST
            # train commands for player 2:
            elif self.player == 2:
                if event.key == pg.K_o and mine_p2.resources >= SWORD_COST:
                    self.add_swordsman()
                    mine_p2.resources -= SWORD_COST
                if event.key == pg.K_p and mine_p2.resources >= WORKER_COST:
                    self.add_worker()
                    mine_p2.resources -= WORKER_COST
                if event.key == pg.K_i and mine_p2.resources >= ARCHER_COST:
                    self.add_archer()
                    mine_p2.resources -= ARCHER_COST

    # dispatched unit if press specific key, and available in barrack, then add them to dispatched unit's lists
    def dispatch_unit(self):
        # for player 1:
        if self.player == 1:
            # check for key and availability in barrack
            if event.key == pg.K_d and len(self.train_swordsman) > 0:
                swordsman = self.train_swordsman.pop()
                self.unit_group.add(swordsman)
                self.swordsman_active.append(swordsman)
            if event.key == pg.K_a and len(self.train_worker) > 0:
                worker = self.train_worker.pop()
                worker.action = 1
                worker.type_action = 1
                self.unit_group.add(worker)
                self.worker_mine.append(worker)
            if event.key == pg.K_s and len(self.train_worker) > 0:
                worker = self.train_worker.pop()
                worker.action = 0
                worker.type_action = 0
                self.unit_group.add(worker)
                self.worker_tower.append(worker)
            if event.key == pg.K_f and len(self.train_archer) > 0:
                archer = self.train_archer.pop()
                self.unit_group.add(archer)
                self.archer_active.append(archer)
            if event.key == pg.K_z and len(self.train_swordsman + self.train_archer) > 0:
                # if press 'unleash all' key add military units to dispatched list
                for unit in self.trained_units:
                    # check for military units only (sword, archer)
                    if type(unit) != Worker and Arrow:
                        dispatch_all_list.append(unit)
                        # delete from barrack dispatched units
                        if unit in self.train_swordsman:
                            self.train_swordsman.remove(unit)
                        if unit in self.train_archer:
                            self.train_archer.remove(unit)
        # for player 2:
        elif self.player == 2:
            if event.key == pg.K_j and len(self.train_swordsman) > 0:
                swordsman = self.train_swordsman.pop()
                self.unit_group.add(swordsman)
                self.swordsman_active.append(swordsman)
            if event.key == pg.K_l and len(self.train_worker) > 0:
                worker = self.train_worker.pop()
                worker.action = 1
                worker.type_action = 1
                self.unit_group.add(worker)
                self.worker_mine.append(worker)
            if event.key == pg.K_k and len(self.train_worker) > 0:
                worker = self.train_worker.pop()
                worker.action = 0
                worker.type_action = 0
                self.unit_group.add(worker)
                self.worker_tower.append(worker)
            if event.key == pg.K_h and len(self.train_archer) > 0:
                archer = self.train_archer.pop()
                self.unit_group.add(archer)
                self.archer_active.append(archer)
            if event.key == pg.K_m and len(self.train_swordsman + self.train_archer) > 0:
                for unit in self.trained_units:
                    if type(unit) != Worker and Arrow:
                        dispatch_all_list.append(unit)
                        if unit in self.train_swordsman:
                            self.train_swordsman.remove(unit)
                        if unit in self.train_archer:
                            self.train_archer.remove(unit)


# define Tower class
class Tower:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.tower_range = TOWER_RANGE  # attack range of tower
        self.hit = TOWER_HIT  # tower's arrow damage
        self.tower_rest = TOWER_REST  # time between two arrows
        self.image = pg.image.load(f'sprites/player{player}/building/tower.png')  # tower's image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.cannon_height = 90  # y coordinate of the position where arrow came from
        self.delay_arrow = TOWER_REST*TURN_DURATION  # 600
        self.current_time = pg.time.get_ticks()

    # attack an enemy
    def attack(self, enemy, player):
        # for player 1:
        if player == 1:
            # find angle of attacking of the arrow using trigonometry
            x_dist = enemy.rect.center[0] - self.rect.centerx
            y_dist = enemy.rect.center[1] - self.cannon_height
            angle = math.atan2(y_dist, x_dist)
            # create an arrow that point to the enemy:
            arrow = Arrow(ARROW_SPEED, units_animations_player1[3], self.rect.centerx, self.cannon_height, angle, 1)
            arrow.attacker = 1  # the towers are attacking
            arrow.target = enemy
            # add arrow into dispatched units lists
            add_to_barracks(arrow, 1)
            barrack_p1.active_arrow.append(arrow)

        if player == 2:
            x_dist = self.rect.centerx - enemy.rect.center[0]
            y_dist = enemy.rect.center[1] - self.cannon_height
            angle = math.atan2(y_dist, x_dist)
            # create an arrow that point to the enemy:
            arrow = Arrow(ARROW_SPEED, units_animations_player2[3], self.rect.centerx, self.cannon_height, angle, 2)
            arrow.attacker = 1
            arrow.target = enemy
            # arrow.image = pg.transform.rotate(arrow.image, 90)
            add_to_barracks(arrow, 2)
            barrack_p2.active_arrow.append(arrow)


# define wall's class
class Wall(pg.sprite.Sprite):
    def __init__(self, health, x, y, player):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.health = health
        self.player = player
        self.image = pg.image.load(f'sprites/player{player}/building/wall.png')  # tower's image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    # health cannot go below 0:
    def update(self):
        if self.health < 0:
            self.health = 0
        self.visualize_hp()
        self.wall_health_bar(WALL_HEALTH)

    # visualize walls health
    def visualize_hp(self):
        if self.player == 1:
            write_on_screen('HP:', str(self.health), 20, 50, (255, 255, 255), FONT)
        elif self.player == 2:
            write_on_screen('HP:', str(self.health), SCREEN_WIDTH - 100, 50, (255, 255, 255), FONT)

    # create health bar for walls
    def wall_health_bar(self, max_health):
        pg.draw.rect(SCREEN, (255, 0, 0), (self.rect.topleft[0] - 20, self.rect.topleft[1] - 100, max_health / 10, 7))
        # if health reduce it reduce size of rectangle:
        if self.health > 0:
            pg.draw.rect(SCREEN, (0, 255, 0), (self.rect.topleft[0] - 20, self.rect.topleft[1] - 100, self.health / 10, 7))


# define Unit's class (of type sprite)
class Units(pg.sprite.Sprite):
    def __init__(self, health, cost, train, speed, animation_list, x, y, player):
        # units are sprite
        pg.sprite.Sprite.__init__(self)
        # general units feature
        self.health = health
        self.cost = cost
        self.train = train
        self.speed = speed
        self.hit = None
        self.animation_list = animation_list
        # initialize first action and frame:
        self.frame_index = 0
        self.action = 0
        # different time control variable (for attack and death animation)
        self.update_time = pg.time.get_ticks()
        self.update_attack = pg.time.get_ticks()
        self.update_death = pg.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.delay = 2.5*TURN_DURATION  # delay of frame
        # position of sprite
        self.x = x
        self.y = y
        # sprite rectangle
        self.rect = pg.Rect(self.x, self.y, 20, 20)
        self.rect.bottomleft = (self.x, self.y)
        self.player = player     # type of player (1 or 2)
        self.delay_attack = 200
        self.death_time = 1000    # time duration of death
        self.alive = True         # check if alive or death
        self.death_count = False

    # visualize the animation on the screen:
    def visualize_animation(self):
        # move unit (at self.speed velocity)
        if self.player == 1:
            self.rect.x += self.speed
        elif self.player == 2:
            self.rect.x -= self.speed
        # check for different type of animation and visualize on screen
        self.type_of_animation()
        SCREEN.blit(self.image, self.rect)

    # handle animations
    def type_of_animation(self):
        # time between two frames:
        delay_frame = self.delay
        # handle delay between frame:
        self.image = self.animation_list[self.action][self.frame_index]
        if pg.time.get_ticks() - self.update_time > delay_frame:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        # if it arrives at the last frame restart the animation from the beginning:
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the unit is dead stay in the last frame
            if self.action == 2 and type(self) != Worker:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                # if it is not dead restart frame from the beginning
                self.frame_index = 0

    # change action and restart frame from 0
    def restore_frame(self, type_action):
        if type_action != self.action:
            self.action = type_action
            self.frame_index = 0

    # inflict damage to an enemy
    def attack(self, object_attacked):
        # if enemy is alive inflict a damage
        if object_attacked.health > 0:
            object_attacked.health -= self.hit
            self.update_attack = pg.time.get_ticks()

    # handle attack of swordsman
    def swordsman_attack(self, object_attacked):
        # if the swordsman is attacking (frame index = 1) inflict damage to enemy
        if self.frame_index == 1 and object_attacked.health > 0:
            if pg.time.get_ticks() - self.update_attack > self.delay_attack/2:
                self.attack(object_attacked)

    # handle attack of archer
    def archer_attack(self, object_attacked):
        # check if enough time since last arrow has passed and attack
        if pg.time.get_ticks() - self.update_attack > self.delay_attack:
            self.attack(object_attacked)

    # handle attack of tower
    def tower_attack(self, object_attacked):
        # apply damage (tower_hit) to an enemy
        temp = self.hit
        self.hit = TOWER_HIT
        self.attack(object_attacked)
        self.hit = temp

    # visualize health bars of units:
    def draw_health_bar(self, max_health):
        # draw 2 overlapping rectangle of different color, one change it's length as health change
        # health bars of units player 1 are switched a little to the left
        if self.player == 1:
            pg.draw.rect(SCREEN, (255, 0, 0), (self.rect.topleft[0] - 10, self.rect.topleft[1] - 15, max_health, 7))
            if self.health > 0:
                pg.draw.rect(SCREEN, (0, 255, 0), (self.rect.topleft[0] - 10, self.rect.topleft[1] - 15, self.health, 7))
        # health bars of units player 2 are switched a little to the right
        elif self.player == 2:
            pg.draw.rect(SCREEN, (255, 0, 0), (self.rect.topleft[0] + 10, self.rect.topleft[1] - 15, max_health, 7))
            if self.health > 0:
                pg.draw.rect(SCREEN, (0, 255, 0), (self.rect.topleft[0] + 10, self.rect.topleft[1] - 15, self.health, 7))

    # handle death animation
    def units_death_animation(self):
        # remove the unit from the trained_units (so enemies do not collide anymore with it)
        if self in barrack_p1.trained_units:
            barrack_p1.trained_units.remove(self)
        if self in barrack_p2.trained_units:
            barrack_p2.trained_units.remove(self)

        # update the death timer for every unit
        if self.death_count is False:
            self.update_death = pg.time.get_ticks()
            self.death_count = True

        # change the action of unit (into death action)
        self.delay = 0.5*TURN_DURATION
        self.restore_frame(2)

        # check if unit reached last frame index of death animation
        if self.frame_index == len(self.animation_list[self.action]) - 1:
            self.units_death()

    # wait a certain time and then kill the unit
    def units_death(self):
        if pg.time.get_ticks() - self.update_death > self.death_time:
            self.kill()

    # check if unit is dead and remove it from screen
    def kill(self):
        self.alive = False
        if self.player == 1:
            delete_from_barrack(self)
        elif self.player == 2:
            delete_from_barrack(self)


# define worker's class
class Worker(Units):
    def __init__(self, health, cost, train, speed, animation_list, x, y, player):
        super().__init__(health, cost, train, speed, animation_list, x, y, player)
        self.produce_res = WORKER_PROD
        self.repair = WORKER_REPAIR
        self.type_action = 0  # 0 = repair wall ; 1 = generate resources
        self.update_attack = pg.time.get_ticks()
        self.delay_prod = 40*TURN_DURATION
        self.delay_repair = 40*TURN_DURATION
        self.delay = 3*TURN_DURATION
        self.update_attack2 = pg.time.get_ticks()

    # decide which action a worker have to make (repair wall or produce resources)
    def update(self):
        if self.alive:
            if self.type_action == 0:
                self.repair_wall()
            elif self.type_action == 1:
                self.generate_resource()

    # handle behaviour of worker in mine
    def action_on_mine(self, mine, mine_pos):
        # stop the worker
        self.speed = 0
        # change action (from run to dig)
        self.restore_frame(2)
        self.action = 2
        # restore position since image change
        self.rect.bottomleft = (mine_pos - 8, SCREEN_HEIGHT - GROUND_HEIGHT - 6)
        # check if enough tima has passed to produce other resources:
        if pg.time.get_ticks() - self.update_attack > self.delay_prod:
            mine.resources += self.produce_res
            self.update_attack = pg.time.get_ticks()

    # generate new resources
    def generate_resource(self):
        if self.player == 1:
            # move towards the mine
            self.rect.x -= self.speed
            self.type_of_animation()
            SCREEN.blit(self.image, self.rect)
            # check if reached the mine
            if self.rect.left <= MINE_POS:
                # handle behaviour of worker in mine
                self.action_on_mine(mine_p1, MINE_POS)

        # for player 2
        elif self.player == 2:
            self.rect.x += self.speed
            self.type_of_animation()
            SCREEN.blit(self.image, self.rect)
            # print(mine_p2.rect.x, 'rect', MINE2_POS, 'POS')
            if self.rect.right >= MINE2_POS:
                self.action_on_mine(mine_p2, MINE2_POS)

    # handle action of worker in the wall
    def action_on_wall(self, wall, type_of_action):
        # stop worker action
        if type_of_action == 0:
            self.speed = 0
            self.restore_frame(3)
            self.frame_index = 1
        # worker restore HP of the wall
        elif type_of_action == 1:
            # stop worker run
            self.speed = 0
            self.restore_frame(3)
            # check if enough time has passed from last restored of HP
            if pg.time.get_ticks() - self.update_attack > self.delay_repair:
                wall.health += self.repair
                self.update_attack = pg.time.get_ticks()

    # repair wall
    def repair_wall(self):
        if self.player == 1:
            self.visualize_animation()
            # check if worker has reached the wall, if it has max health then stay still
            if self.rect.right >= wall_p1.rect.centerx and wall_p1.health >= 1000:
                # handle action on wall
                self.action_on_wall(wall_p1, 0)
            elif self.rect.right >= wall_p1.rect.centerx and wall_p1.health <= 1000:
                # repair wall
                self.action_on_wall(wall_p1, 1)

        elif self.player == 2:
            self.visualize_animation()
            if self.rect.left <= wall_p2.rect.centerx and wall_p2.health >= 1000:
                self.action_on_wall(wall_p2, 0)
            elif self.rect.left <= wall_p2.rect.centerx and wall_p2.health <= 1000:
                self.action_on_wall(wall_p2, 1)


# define swordsman class
class Swordsman(Units, pg.sprite.Sprite):
    def __init__(self, health, cost, train, speed, animation_list, x, y, player):
        super().__init__(health, cost, train, speed, animation_list, x, y, player)
        pg.sprite.Sprite.__init__(self)
        # self.ranges = SWORD_RANGE  # range of attack
        self.hit = SWORD_HIT
        self.rest = SWORD_REST     # rest turns between attack
        self.max_health = SWORD_HEALTH
        self.update_attack = pg.time.get_ticks()
        self.delay_attack = self.rest*TURN_DURATION   # rest duration between attack
        self.update_time = pg.time.get_ticks()
        self.alive = True
        self.target = None  # enemy attacked

    # action made when reached wall
    def attack_wall(self, wall):
        self.target = wall
        self.restore_frame(1)
        self.swordsman_attack(self.target)

    # handle swordsman action
    def update(self):
        # check if is alive
        if self.alive:
            # draw the health bar:
            self.draw_health_bar(self.max_health)

            # check if health reached 0
            if self.health <= 0:
                self.units_death_animation()

            # action made as long as it's alive
            if self.health > 0:
                if self.player == 1:
                    # check collision with enemies
                    gets_hit = pg.sprite.spritecollideany(self, barrack_p2.trained_units)
                    # check if reached the wall
                    if self.rect.right >= wall_p2.rect.left:
                        self.attack_wall(wall_p2)
                    # if does not collide with a troop keep running:
                    elif gets_hit is None:
                        self.restore_frame(0)
                        self.speed = SWORD_SPEED

                # for player 2
                elif self.player == 2:
                    gets_hit = pg.sprite.spritecollideany(self, barrack_p1.trained_units)
                    if self.rect.left <= wall_p1.rect.right:
                        self.attack_wall(wall_p1)
                    # if does not collide with a troop keep running:
                    elif gets_hit is None:
                        self.restore_frame(0)
                        self.speed = SWORD_SPEED

            # run until reaches target:
            if self.action == 0:
                if self.player == 1:
                    self.rect.x += self.speed
                elif self.player == 2:
                    self.rect.x -= self.speed

            # visualize on screen:
            self.type_of_animation()
            SCREEN.blit(self.image, self.rect)


# define Arrows class
class Arrow(Units):
    def __init__(self, speed, animation_list, x, y, angle, player):
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.attacker = 0  # 0 = attacker is an archer, 1 = it's a Tower
        self.speed = speed
        self.hit = ARCHER_HIT
        self.action = 1   # type of action
        self.update_time = pg.time.get_ticks()
        self.update_attack = pg.time.get_ticks()
        self.delay = 15*TURN_DURATION
        self.animation_list = animation_list
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pg.Rect(0, 0, 10, 15)   # arrow's rectangle
        self.x = x
        self.y = y
        self.archer_y = 234  # height of the bow
        self.rect.bottomleft = (self.x, self.y)    # position of rectangle
        self.angle = angle   # angle of attacking arrow
        self.dx = math.cos(self.angle) * self.speed  # displacement in x direction
        self.dy = math.sin(self.angle) * self.speed  # displacement in y direction
        self.target = None    # target of the attack

    # handle arrows behaviour
    def update(self):
        # move the arrow:
        if self.player == 1:
            # if it's a archer's arrow it moves only the x coordinate
            if self.attacker == 0:
                self.rect.x += self.speed
            # if it's a tower's arrow both x and y coordinate have to change
            elif self.attacker == 1:
                self.rect.x += self.dx
                self.rect.y += self.dy
        # for player 2
        if self.player == 2:
            if self.attacker == 0:
                self.rect.x -= self.speed
            elif self.attacker == 1:
                self.rect.x -= self.dx
                self.rect.y += self.dy

        # handle animation:
        self.type_of_animation()
        # gave an angle to the arrow
        if self.player == 1 and self.attacker == 1:
            self.image = pg.transform.rotate(self.image, -(math.degrees(self.angle)))
        # for player 2:
        if self.player == 2 and self.attacker == 1:
            self.image = pg.transform.rotate(self.image, math.degrees(self.angle))

        # visualize arrow
        SCREEN.blit(self.image, self.rect)

    # handle archer's arrow attack
    def throw_arrow(self, attacker, player, enemy_target):
        if player == 1:
            arrow = Arrow(ARCHER_ARROW_SPEED, units_animations_player1[3], attacker.rect.x, self.archer_y, 0, player)
            arrow.target = enemy_target
            add_to_barracks(arrow, 1)
            barrack_p1.active_arrow.append(arrow)
        # for player 2
        elif player == 2:
            arrow = Arrow(ARCHER_ARROW_SPEED, units_animations_player2[3], attacker.rect.x, self.archer_y, 0, player)
            arrow.target = enemy_target
            add_to_barracks(arrow, 2)
            barrack_p2.active_arrow.append(arrow)


# define Archer's class
class Archer(Units):
    def __init__(self, health, cost, train, speed, animation_list, x, y, player):
        super().__init__(health, cost, train, speed, animation_list, x, y, player)
        self.ranges = ARCHER_RANGE
        self.rest = ARCHER_REST
        self.max_heath = ARCHER_HEALTH
        self.current_time = pg.time.get_ticks()  # keep track of time
        self.alive = True
        self.shoot = False  # check if archer has shoots
        self.delay_attack = self.rest*TURN_DURATION  # time between attack

    # handle archer behaviour
    def update(self):
        # check if alive
        if self.alive:
            # draw health bar:
            self.draw_health_bar(self.max_heath)

            # che if health has reached 0:
            if self.health <= 0:
                if self.player == 1:
                    # if archer die put the body on the ground
                    self.rect.bottomleft = (self.rect.x, SCREEN_HEIGHT - GROUND_HEIGHT)
                self.units_death_animation()

            # handle action if it is alive
            if self.health > 0:
                if self.player == 1:
                    # find the target of the attack checking if enemy in ranges
                    enemy_target = find_distance(self, barrack_p2.unit_group)
                    # check if reached the wall (with the range)
                    if self.rect.right > wall_p2.rect.left - self.ranges:
                        self.delay = self.delay_attack
                        # change action from running to attack
                        self.restore_frame(1)
                        # restore position (it changes switching type of animation)
                        self.rect.bottomleft = (wall_p2.rect.left - ARCHER_RANGE, SCREEN_HEIGHT - GROUND_HEIGHT - 4)
                    # if no target keep running
                    elif enemy_target is None:
                        self.archer_target_action(0)
                    # if target is an enemy stop moving and attack it
                    elif enemy_target is not None and enemy_target != wall_p2:
                        self.archer_target_action(1)
                    # handle archer action
                    self.archer_action(arrow_p1, enemy_target)

                # for player 2
                elif self.player == 2:
                    enemy_target = find_distance(self, barrack_p1.unit_group)
                    if self.rect.left <= wall_p1.rect.right + self.ranges:
                        self.delay = self.delay_attack
                        self.restore_frame(1)
                        self.rect.bottomleft = (wall_p1.rect.right + ARCHER_RANGE, SCREEN_HEIGHT - GROUND_HEIGHT - 4)
                    elif enemy_target is None:
                        self.archer_target_action(0)
                    elif enemy_target is not None and enemy_target != wall_p1:
                        self.archer_target_action(1)
                    self.archer_action(arrow_p2, enemy_target)

            # move archer
            if self.action == 0:
                if self.player == 1:
                    self.rect.x += self.speed
                elif self.player == 2:
                    self.rect.x -= self.speed

            # visualize animation
            self.type_of_animation()
            SCREEN.blit(self.image, self.rect)

    # handle action for different target
    def archer_target_action(self, type_of_action):
        # if there are no enemy, keep running
        if type_of_action == 0:
            self.speed = ARCHER_SPEED
            self.restore_frame(0)
            # delay from animation whn running
            self.delay = 2.5*TURN_DURATION
        # if there are units enemies stop moving and attack them
        elif type_of_action == 1:
            self.speed = 0
            # change action from running into attack
            self.restore_frame(1)
            self.action = 1
            # restore the position
            self.rect.y = SCREEN_HEIGHT - (GROUND_HEIGHT + self.image.get_height())
            # delay animation when attacking
            self.delay = self.delay_attack

    # handle archer behaviour based on action
    def archer_action(self, arrow_player, enemy_target):
        # check if archer has to attack
        if self.action == 1 and self.frame_index == 1:
            # handle rest between attack
            if pg.time.get_ticks() - self.current_time > self.delay_attack:
                arrow_player.throw_arrow(self, self.player, enemy_target)
                # restore current time
                self.current_time = pg.time.get_ticks()


# create  a list of initial position of units (in order: swordsman, worker, archer):
dimension_units_swordsman = (units_animations_player1[0][0][0].get_width(), units_animations_player1[0][0][0].get_height())
dimension_units_worker = (units_animations_player1[1][2][0].get_width(), units_animations_player1[1][2][0].get_height())
dimension_units_archer = (units_animations_player1[2][0][0].get_width(), units_animations_player1[2][0][0].get_height())

# initial position of units (barrack position)
initial_position_p1 = (BARRACKS_POS, (SCREEN_HEIGHT - GROUND_HEIGHT))
initial_position_p2 = (SCREEN_WIDTH - (BARRACKS_POS + 10), (SCREEN_HEIGHT - GROUND_HEIGHT))

# create instance of wall:
wall_p1 = Wall(WALL_HEALTH, WALL_POS - WALL_WIDTH / 2, SCREEN_HEIGHT - (GROUND_HEIGHT + WALL_HEIGHT), 1)
wall_p2 = Wall(WALL_HEALTH, SCREEN_WIDTH - (WALL_POS + WALL_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + WALL_HEIGHT), 2)

# create instance of tower:
tower_p1 = Tower(WALL_POS - (TOWER_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT), 1)
tower_p2 = Tower(SCREEN_WIDTH - (WALL_POS + TOWER_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT), 2)

# create a barrack:
barrack_p1 = Barrack(1, 1, 1, 1)
barrack_p2 = Barrack(2, 1, 1, 1)

# initialize barraks:
barrack_p1.initialize_unit()
barrack_p2.initialize_unit()

# create instance of mine:
mine_p1 = Mine(1)
mine_p2 = Mine(2)

# create instance of arrow:
arrow_p1 = Arrow(ARROW_SPEED, units_animations_player1[3], (WALL_POS - TOWER_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT), 0, 1)
arrow_p2 = Arrow(ARROW_SPEED, units_animations_player2[3], (SCREEN_WIDTH - (WALL_POS + TOWER_WIDTH)), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT), 0, 2)

# create a sprite group for walls:
wall_group = pg.sprite.Group()
wall_group.add(wall_p1)
wall_group.add(wall_p2)

# units that will be dispatched all together (using 'z' or 'm' key):
dispatch_all_list = []

# define queue for units target (order of attacking enemies)
q1 = collections.deque()
q2 = collections.deque()

# define font for writing into the screen:
FONT = pg.font.SysFont('Lucida Sans', 18)

# define bigger font
BIGGER_FONT = pg.font.SysFont('arialblack', 35)

# list of tuple with information that have to be visualized on screen (using function below)
written = [('', barrack_p1.worker_mine, MINE_POS-4, 170), ('', barrack_p2.worker_mine, MINE2_POS-4, 170),
           ('', barrack_p1.train_worker, 80, 160), ('', barrack_p2.train_worker, 910, 160),
           ('', barrack_p1.train_swordsman, 100, 160), ('', barrack_p2.train_swordsman, 890, 160),
           ('', barrack_p1.train_archer, 120, 160), ('', barrack_p2.train_archer, 870, 160),
           ('', barrack_p1.worker_tower, 175, 160), ('', barrack_p2.worker_tower, 815, 160)]

# FUNCTIONS:


# write message on screen:
def write_on_screen(message, data, x, y, color=(255, 255, 255), font=pg.font.SysFont('Lucida Sans', 18)):
    # if data are of type list we visualize the length
    if type(data) == list:
        write = font.render(f'{message}' + str(len(data)), True, color)
    # visualize message on screen
    else:
        write = font.render(f'{message}' + str(data), True, color)
    # print on screen the message
    SCREEN.blit(write, (x, y))


# handle units that have to be unleashed all together
def unleash_all_units():
    # # check if there are element to be unleashed all together
    if len(dispatch_all_list) > 0:
        # handle time between dispatching time between two units
        if pg.time.get_ticks() - barrack_p1.up_time > barrack_p1.delay_time:
            unit = dispatch_all_list.pop()
            # add unit to barracks lists of playing units
            if unit in barrack_p1.trained_units:
                barrack_p1.unit_group.add(unit)
                if type(unit) == Swordsman:
                    barrack_p1.swordsman_active.append(unit)
                if type(unit) == Archer:
                    barrack_p1.archer_active.append(unit)
            # check for unit in barrack 2
            elif unit in barrack_p2.trained_units:
                barrack_p2.unit_group.add(unit)
                if type(unit) == Swordsman:
                    barrack_p2.swordsman_active.append(unit)
                if type(unit) == Archer:
                    barrack_p2.archer_active.append(unit)
            # update time
            barrack_p1.up_time = pg.time.get_ticks()


# delete units/arrows from the barrack
def delete_from_barrack(element):
    # check if units/arrows is in barrack 1 and delete:
    if element in barrack_p1.unit_group:
        barrack_p1.unit_group.remove(element)
    if element in barrack_p1.trained_units:
        barrack_p1.trained_units.remove(element)

    # check for barrack 2:
    if element in barrack_p2.unit_group:
        barrack_p2.unit_group.remove(element)
    if element in barrack_p2.trained_units:
        barrack_p2.trained_units.remove(element)

    # check for arrow:
    if element in barrack_p1.active_arrow:
        barrack_p1.active_arrow.remove(element)
    elif element in barrack_p2.active_arrow:
        barrack_p2.active_arrow.remove(element)


# add element to barrack's lists
def add_to_barracks(elem, player):
    if player == 1:
        barrack_p1.unit_group.add(elem)
        barrack_p1.trained_units.append(elem)
    if player == 2:
        barrack_p2.unit_group.add(elem)
        barrack_p2.trained_units.append(elem)


# check if enemy in archer range and return that enemy as attack target
def find_distance(unit, group):
    temp = None
    # check for every enemy the distance with the archer
    for enemy in group:
        if abs(unit.rect.x - enemy.rect.x) <= ARCHER_RANGE and type(enemy) != Arrow:
            temp = enemy
    # if an enemy is in the attack range it becomes the target
    enemy_target = temp
    return enemy_target


# check if two units of same player are in the same point and visualize their total health
def units_same_position(unit, units, player):
    # check if unit is dispatched
    if unit.rect.x in range(150, 850):
        # check if different unit of same player are in the same point
        collide_object = pg.sprite.spritecollide(unit, units, False)
        total_health = 0
        collide_unit = []
        # iterate for every unit that is in same point of another of same player
        for elem in collide_object:
            if type(elem) != Arrow:
                collide_unit.append(elem)
                # add all health of units together
                total_health += elem.health
        # if there are multiple units in same point visualize on screen the total health
        if len(collide_unit) > 1 and unit != Arrow:
            if player == 1:
                write_on_screen('', total_health, collide_unit[0].rect.x, collide_unit[0].rect.y - 40, (255, 0, 0))
            elif player == 2:
                write_on_screen('', total_health, collide_unit[0].rect.x, collide_unit[0].rect.y - 40, (0, 0, 255))


# handle collision between arrows and ground
def ground_collision(unit):
    # check if arrow touch the ground
    if unit.rect.bottomleft[1] >= SCREEN_HEIGHT - GROUND_HEIGHT + unit.image.get_height() / 2 - 3:
        # delete it
        delete_from_barrack(unit)
        if unit in barrack_p1.active_arrow:
            barrack_p1.active_arrow.remove(unit)
        elif unit in barrack_p2.active_arrow:
            barrack_p2.active_arrow.remove(unit)


# handle swordsman collision:
def swordsman_collision(unit, enemy):
    # check if there is an enemy different from thw wall
    if abs(unit.rect.x - enemy.rect.x) <= 20 and unit.target != wall_p2 and unit.target != wall_p1:
        # stop moving swordsman and attack enemy
        unit.speed = 0
        unit.restore_frame(1)
        unit.action = 1
        unit.target = enemy
        unit.swordsman_attack(enemy)


# handle arrows collision with ground and wall
def arrow_collision(unit, player):
    if type(unit) == Arrow:
        # if an arrow hits the ground delete it:
        ground_collision(unit)
        # if arrow hits the tower we delete the arrow and apply damage to the tower:
        if player == 1:
            if unit.rect.right >= wall_p2.rect.left:
                unit.attack(wall_p2)   # apply damage to the tower
                delete_from_barrack(unit)  # delete unit
        # for player 2:
        elif player == 2:
            if unit.rect.left <= wall_p1.rect.right:
                unit.attack(wall_p1)
                delete_from_barrack(unit)


# handle arrows collision with units
def arrow_units_collision(unit, enemy, queue):
    # check if the arrow hits an enemy's unit
    if unit.rect.colliderect(enemy.rect) and type(enemy) != Arrow:
        queue.append(enemy)  # append enemy to queue (enemy to be attacked)
        # if arrows has no specific target take it from the queue
        if unit.target is None:
            unit.target = queue.pop()
        # check if the arrow come from an archer
        if unit.attacker == 0:
            # if it has a target apply damage to it
            if unit.target == enemy:
                unit.attack(enemy)
            # if the enemy attacked is died choose other target
            elif unit.target.action == 2:
                unit.target = queue.pop()
            # check if arrow hit a distance enemy different from the target
            elif abs(unit.target.rect.x - enemy.rect.x) >= 25:
                unit.attack(enemy)
            delete_from_barrack(unit)
        # check is the arrows come from the tower
        if unit.attacker == 1:
            #  check if it has an enemy target or it hits a distant enemy different from the target
            if unit.target == enemy or (unit.target != enemy and abs(enemy.rect.x - unit.target.rect.x) >= 20):
                unit.tower_attack(enemy)  # apply damage to enemy
        delete_from_barrack(unit)  # delete arrow


# handle collision of units and arrows
def handle_collision(units, enemies, player):
    for unit in units:
        # check if two units of same player are in the same point and visualize their total health
        units_same_position(unit, units, player)
        # handle arrows collision with ground and wall
        arrow_collision(unit, player)
        # handle collision between units of a player and enemies (units of other player)
        for enemy in enemies:
            # handle swordsman collision
            if type(unit) == Swordsman and type(enemy) != Arrow:
                swordsman_collision(unit, enemy)
            # handle arrow's collision with enemies:
            if type(unit) == Arrow:
                if player == 1:
                    arrow_units_collision(unit, enemy, q2)
                # for player 2:
                elif player == 2:
                    arrow_units_collision(unit, enemy, q1)


# if an enemy is in the tower's range the tower attacks:
def handle_tower(tower, enemies, player):
    # check for all enemies (units of other player)
    for enemy in enemies:
        # check for enemies that are not arrows
        if type(enemy) != Arrow:
            if player == 1:
                # check if enemy enter the tower's range
                if enemy.rect.left < tower.rect.right + tower.tower_range:
                    # handle time between attack
                    if pg.time.get_ticks() - tower.current_time > tower.delay_arrow:
                        # tower attack enemy
                        tower.attack(enemy, player)
                        tower.current_time = pg.time.get_ticks()
            # for player 2
            elif player == 2:
                if enemy.rect.right > tower.rect.right - tower.tower_range:
                    if pg.time.get_ticks() - tower.current_time > tower.delay_arrow:
                        tower.attack(enemy, player)
                        tower.current_time = pg.time.get_ticks()


# visualize static image (background and buildings):
def draw_static():
    # visualize the background (sky):
    pg.draw.rect(SCREEN, (0, 150, 255), BACKGROUND)
    # visualize the ground:
    pg.draw.rect(SCREEN, (0, 255, 100), GROUND)
    # visualize mines:
    SCREEN.blit(MINE_IMAGE_P1, ((MINE_POS - MINE_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + MINE_HEIGHT)))
    SCREEN.blit(MINE_IMAGE_P2, (SCREEN_WIDTH - (MINE_POS + MINE_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + MINE_HEIGHT)))
    # visualize barracks
    SCREEN.blit(BARRACKS_IMAGE_P1, ((BARRACKS_POS - BARRACKS_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + BARRACKS_HEIGHT)))
    SCREEN.blit(BARRACKS_IMAGE_P2, (SCREEN_WIDTH - (BARRACKS_POS + BARRACKS_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + BARRACKS_HEIGHT)))
    # visualize towers
    SCREEN.blit(TOWER_IMAGE_P1, ((WALL_POS - TOWER_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT)))
    SCREEN.blit(TOWER_IMAGE_P2, (SCREEN_WIDTH - (WALL_POS + TOWER_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + TOWER_HEIGHT)))
    # visualize walls
    SCREEN.blit(WALL_IMAGE_P1, ((WALL_POS - WALL_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + WALL_HEIGHT)))
    SCREEN.blit(WALL_IMAGE_P2, (SCREEN_WIDTH - (WALL_POS + WALL_WIDTH / 2), SCREEN_HEIGHT - (GROUND_HEIGHT + WALL_HEIGHT)))


# initialize game:
# can be initialized by playing new game (type_of_init = True) or load past game (type_of_unit = False)
def initialize_game(type_of_init):
    # initialize elements in game:
    barracks = [barrack_p1, barrack_p2]
    for elem in barracks:
        elem.unit_group.empty()
        elem.trained_units.clear()
        elem.train_archer.clear()
        elem.train_worker.clear()
        elem.worker_mine.clear()
        elem.worker_tower.clear()
        elem.train_swordsman.clear()

    # if playing new game we initialize element in barracks (if loading past game we do not)
    if type_of_init is True:
        # initialize unit in  barracks
        barrack_p1.initialize_unit()
        barrack_p2.initialize_unit()
    # initialize wall's health:
    wall_p1.health = 1000
    wall_p2.health = 1000
    # initialize mine's resources
    mine_p1.resources = 10
    mine_p2.resources = 10


# save game
def save_game():
    # create list for save dispatched units currently playing
    active_swordsman_1 = []
    active_archer_1 = []
    active_worker_mine_1 = []
    active_worker_tower_1 = []
    active_arrow_1 = []
    # crate a file:
    f = open('Save_spec.py', 'w')
    # write relevant data to save on file:
    f.write('# START =' + 'Player1' + '\n')
    f.write('RESOURCES_P1 =' + str(mine_p1.resources) + '\n')   # save resources
    f.write('WALL_HEALTH_P1 =' + str(wall_p1.health) + '\n')     # save health
    # save units in barrack
    f.write('SWORDSMAN_BARRACK_P1 =' + str(len(barrack_p1.train_swordsman)) + '\n')
    f.write('ARCHER_BARRACK_P1 =' + str(len(barrack_p1.train_archer)) + '\n')
    f.write('WORKER_BARRACK_P1 =' + str(len(barrack_p1.train_worker)) + '\n')
    # save units currently plying using a list that contain those elements
    for elem in barrack_p1.active_arrow:
        # for every arrow save position, angle, attacker and speed
        active_arrow_1.append((elem.rect.x, elem.rect.y, elem.angle, elem.attacker, elem.speed))
    f.write('active_arrow_1 = ' + str(active_arrow_1) + '\n')
    for elem in barrack_p1.swordsman_active:
        # for every swordsman save position and health
        active_swordsman_1.append((elem.rect.x, elem.health))
    f.write('active_swordsman_1 = ' + str(active_swordsman_1) + '\n')
    for elem in barrack_p1.archer_active:
        # for every archer save position and health
        active_archer_1.append((elem.rect.x, elem.health))
    f.write('active_archer_1 = ' + str(active_archer_1) + '\n')
    for elem in barrack_p1.worker_mine:
        # for every worker save position and type of action
        active_worker_mine_1.append((elem.rect.x, elem.health, elem.type_action))
    f.write('active_worker_mine_1 = ' + str(active_worker_mine_1) + '\n')
    for elem in barrack_p1.worker_tower:
        # for every swordsman save position and type of action
        active_worker_tower_1.append((elem.rect.x, elem.health, elem.type_action))
    f.write('active_worker_tower_1 = ' + str(active_worker_tower_1) + '\n')
    f.write('# END: Player1' + '\n')
    # put space in file between two player data
    f.write('' + '\n')

    # for player 2:
    active_swordsman_2 = []
    active_archer_2 = []
    active_worker_mine_2 = []
    active_worker_tower_2 = []
    active_arrow_2 = []
    f.write('# START_2 =' + 'Player2' + '\n')
    f.write('RESOURCES_P2 =' + str(mine_p2.resources) + '\n')
    f.write('WALL_HEALTH_P2 =' + str(wall_p2.health) + '\n')
    f.write('SWORDSMAN_BARRACK_P2 =' + str(len(barrack_p2.train_swordsman)) + '\n')
    f.write('ARCHER_BARRACK_P2 =' + str(len(barrack_p2.train_archer)) + '\n')
    f.write('WORKER_BARRACK_P2 =' + str(len(barrack_p2.train_worker)) + '\n')
    for elem in barrack_p2.active_arrow:
        active_arrow_2.append((elem.rect.x, elem.rect.y, elem.angle, elem.attacker, elem.speed))
    f.write('active_arrow_2 = ' + str(active_arrow_2) + '\n')
    for elem in barrack_p2.swordsman_active:
        active_swordsman_2.append((elem.rect.x, elem.health))
    f.write('active_swordsman_2 = ' + str(active_swordsman_2) + '\n')
    for elem in barrack_p2.archer_active:
        active_archer_2.append((elem.rect.x, elem.health))
    f.write('active_archer_2 = ' + str(active_archer_2) + '\n')
    for elem in barrack_p2.worker_mine:
        active_worker_mine_2.append((elem.rect.x, elem.health, elem.type_action))
    f.write('active_worker_mine_2 = ' + str(active_worker_mine_2) + '\n')
    for elem in barrack_p2.worker_tower:
        active_worker_tower_2.append((elem.rect.x, elem.health, elem.type_action))
    f.write('active_worker_tower_2 = ' + str(active_worker_tower_2) + '\n')
    f.write('# END_2 =' + 'Player2' + '\n')
    # close file
    f.close()
    # visualize that the game has been saved
    write_on_screen('GAME SAVED', '', 450, 150)
    # visualize key to press to continue playing
    write_on_screen('Press SPACE to continue this game', '', 350, 180)


# load past saved game
def load_game():
    # visualize on screen that it's loading past game
    write_on_screen('GAME LOAD', '', 450, 150)
    write_on_screen('Press SPACE to start playing', '', 380, 170)
    # load units in the barrack (create unit equal to saved units and add it to barracks lists):
    # for every swordsman in barrack saved, load a new one with same features (position and health)
    for i in range(SWORDSMAN_BARRACK_P1):
        swordsman = barrack_p1.new_swordsman()
        barrack_p1.train_swordsman.append(swordsman)
        barrack_p1.trained_units.append(swordsman)
    # for every archer in barrack saved, load a new one with same features
    for i in range(ARCHER_BARRACK_P1):
        archer = barrack_p1.new_archer()
        barrack_p1.train_archer.append(archer)
        barrack_p1.trained_units.append(archer)
    # for every worker in barrack saved load a new one with same features
    for i in range(WORKER_BARRACK_P1):
        worker = barrack_p1.new_worker()
        barrack_p1.train_worker.append(worker)
        barrack_p1.trained_units.append(worker)

    # load arrow (create arrows and add to barrack lists):
    for i in range(len(active_arrow_1)):
        arrow = Arrow(active_arrow_1[i][4], units_animations_player1[3], active_arrow_1[i][0],
                 active_arrow_1[i][1], active_arrow_1[i][2], 1)
        arrow.attacker = active_arrow_1[i][3]
        add_to_barracks(arrow, 1)
        barrack_p1.active_arrow.append(arrow)

    # load units dispatched (create unit and add to barrack lists):
    for i in range(len(active_swordsman_1)):
        swordsman = Swordsman(active_swordsman_1[i][1], units_cost[0], units_train[0], units_speed[0], units_animations_player1[0],
                              active_swordsman_1[i][0], initial_position_p1[1], 1)
        add_to_barracks(swordsman, 1)
    for i in range(len(active_archer_1)):
        archer = Archer(active_archer_1[i][1], units_cost[2], units_train[2], units_speed[2], units_animations_player1[2],
                        active_archer_1[i][0], initial_position_p1[1] - 2, 1)
        add_to_barracks(archer, 1)
    for i in range(len(active_worker_mine_1)):
        worker = Worker(active_worker_mine_1[i][1], units_cost[1], units_train[1], units_speed[1], units_animations_player1[1],
                        active_worker_mine_1[i][0], initial_position_p1[1], 1)
        worker.type_action = active_worker_mine_1[i][2]
        worker.action = active_worker_mine_1[i][2]
        add_to_barracks(worker, 1)
        barrack_p1.worker_mine.append(worker)
    for i in range(len(active_worker_tower_1)):
        worker = Worker(active_worker_tower_1[i][1], units_cost[1], units_train[1], units_speed[1], units_animations_player1[1],
                        active_worker_tower_1[i][0], initial_position_p1[1], 1)
        worker.type_action = active_worker_tower_1[i][2]
        worker.action = active_worker_tower_1[i][2]
        add_to_barracks(worker, 1)
        barrack_p1.worker_tower.append(worker)

    # for player 2:
    for i in range(SWORDSMAN_BARRACK_P2):
        swordsman = barrack_p2.new_swordsman()
        barrack_p2.train_swordsman.append(swordsman)
        barrack_p2.trained_units.append(swordsman)
    for i in range(ARCHER_BARRACK_P2):
        archer = barrack_p2.new_archer()
        barrack_p2.train_archer.append(archer)
        barrack_p2.trained_units.append(archer)
    for i in range(WORKER_BARRACK_P1):
        worker = barrack_p2.new_worker()
        barrack_p2.train_worker.append(worker)
        barrack_p2.trained_units.append(worker)
    # arrows
    for i in range(len(active_arrow_2)):
        arrow = Arrow(active_arrow_2[i][4], units_animations_player2[3], active_arrow_2[i][0],
                 active_arrow_2[i][1], active_arrow_2[i][2], 2)
        arrow.attacker = active_arrow_2[i][3]
        add_to_barracks(arrow, 2)
        barrack_p2.active_arrow.append(arrow)
    # units
    for i in range(len(active_swordsman_2)):
        swordsman = Swordsman(active_swordsman_2[i][1], units_cost[0], units_train[0], units_speed[0], units_animations_player2[0],
                              active_swordsman_2[i][0], initial_position_p2[1], 2)
        add_to_barracks(swordsman, 2)
    for i in range(len(active_archer_2)):
        archer = Archer(active_archer_2[i][1], units_cost[2], units_train[2], units_speed[2], units_animations_player2[2],
                        active_archer_2[i][0], initial_position_p2[1] - 2, 2)
        add_to_barracks(archer, 2)
    for i in range(len(active_worker_mine_2)):
        worker = Worker(active_worker_mine_2[i][1], units_cost[1], units_train[1], units_speed[1], units_animations_player2[1],
                        active_worker_mine_2[i][0], initial_position_p2[1], 2)
        worker.type_action = active_worker_mine_2[i][2]
        worker.action = active_worker_mine_2[i][2]
        add_to_barracks(worker, 2)
        barrack_p2.worker_mine.append(worker)
    for i in range(len(active_worker_tower_2)):
        worker = Worker(active_worker_tower_2[i][1], units_cost[1], units_train[1], units_speed[1], units_animations_player2[1],
                        active_worker_tower_2[i][0], initial_position_p2[1], 2)
        worker.type_action = active_worker_tower_2[i][2]
        worker.action = active_worker_tower_2[i][2]
        add_to_barracks(worker, 2)
        barrack_p2.worker_tower.append(worker)


# main loop
run = True
while run:
    # set clock (iterations per seconds)
    clock.tick(FPS)
    # handle events
    for event in pg.event.get():
        # if any player click to exit it quit game
        if event.type == pg.QUIT:
            run = False
        # handle keyboard events
        if event.type == pg.KEYDOWN:
            # handle keyboard for train units
            barrack_p1.train_units()
            barrack_p2.train_units()
            # handle keyboard for dispatch units
            barrack_p1.dispatch_unit()
            barrack_p2.dispatch_unit()
            # pause game pressing space hey
            if event.key == pg.K_SPACE and pause is False:
                pause = True
            # resume playing
            elif event.key == pg.K_SPACE and pause is True:
                pause = False
            # save and pause game
            elif event.key == pg.K_v:
                pause = True
                save_game()
            # load game
            elif event.key == pg.K_b:
                pause = (not pause)
                initialize_game(False)  # initialize
                load_game()  # load
    # loop of game
    if play is True:
        if pause is False:
            # draw background
            draw_static()
            # draw message (hp, resources, element in barracks)
            for write in written:
                write_on_screen(write[0], write[1], write[2], write[3])
            # handle element to be unleashed all together
            unleash_all_units()
            # update unit's action
            barrack_p1.unit_group.update()
            barrack_p2.unit_group.update()
            # update barrack training time:
            barrack_p1.update()
            barrack_p2.update()
            # check collision between units and units or towers:
            handle_collision(barrack_p1.trained_units, barrack_p2.trained_units, 1)
            handle_collision(barrack_p2.trained_units, barrack_p1.trained_units, 2)
            # handle tower attack:
            handle_tower(tower_p1, barrack_p2.trained_units, 1)
            handle_tower(tower_p2, barrack_p1.trained_units, 2)
            # visualize resources:
            mine_p1.update()
            mine_p2.update()
            # visualize wall health:
            wall_group.update()
            # if wall's health reaches 0 stop the game and visualize winner:
            if wall_p1.health == 0:
                WINNER = ['BLUE', (0, 0, 255)]
                play = False
                # play the winner sound:
                WIN_SOUND.play()
            # for player 2
            if wall_p2.health == 0:
                WINNER = ['RED', (255, 0, 0)]
                play = False
                WIN_SOUND.play()
        # if PAUSE is false warns that the game is paused
        else:

            write_on_screen('PAUSE', '', 450, 100, (255, 255, 255), BIGGER_FONT)
    # stop game and visualize winner
    else:
        write_on_screen('THE WINNER IS:', WINNER[0], 330, 100, WINNER[1], BIGGER_FONT)
        # visualize key to start another game
        write_on_screen('Press 0 to restart', '', 430, 140, WINNER[1], FONT)
        key = pg.key.get_pressed()
        # start new game
        if key[pg.K_0]:
            play = True
            initialize_game(True)  # initialize new game
    # update screen
    pg.display.update()
# quit game
pg.quit()
