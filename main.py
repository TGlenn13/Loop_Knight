from designer import *
from dataclasses import dataclass
from random import randint

KNIGHT_SPEED = 5
PLAYER_HEALTH = 5
SWORD = "🗡️"

@dataclass
class World:
    knight: DesignerObject
    knight_speed: int
    monster: list[DesignerObject]
    # tier_2_monster: list[DesignerObject]
    # boss: list[DesignerObject]
    sword: DesignerObject
    player_health: int
    # weapons: list[DesignerObject]
    # wave_number: int


def create_world() -> World:
    return World(create_knight(), KNIGHT_SPEED, [], SWORD,
                 text("black", "Health: " + str(PLAYER_HEALTH),  20, 40, 10))


def create_knight() -> DesignerObject:
    """ Create the knight """
    knight = emoji("🥷")
    knight.y = get_height() / 2
    knight.x = get_width() / 2
    return knight


def move_knight_horizontal(world: World, key: str):
    """ Move the knight horizontally"""
    if key == "d":
        world.knight.x += world.knight_speed
    elif key == "a":
        world.knight.x -= world.knight_speed


def move_knight_vertical(world: World, key: str):
    """ Move the knight vertically"""
    if key == "w":
        world.knight.y -= world.knight_speed
    elif key == "s":
        world.knight.y += world.knight_speed


def boundaries(world: World):
    """ Handle the knight running into the wall"""
    if world.knight.x > get_width():
        world.knight.x = get_width() - 1
    elif world.knight.x < 0:
        world.knight.x = 1
    if world.knight.y > get_height():
        world.knight.y = get_height() - 1
    elif world.knight.y < 0:
        world.knight.y = 1


def head_left(world: World):
    """ Make the knight move left """
    # world.knight_speed = -KNIGHT_SPEED
    world.knight.flip_x = False


def head_right(world: World):
    """ Make the knight move right """
    # world.knight_speed = KNIGHT_SPEED
    world.knight.flip_x = True


def direct_knight(world: World, key: str):
    """ Change the direction that the knight is moving """
    if key == "a":
        head_left(world)
    elif key == "d":
        head_right(world)
'''
def create_weapon() -> DesignerObject:
    """ Create a weapon. For now swords only"""
    return World.sword

def move_below(bottom: DesignerObject, top: DesignerObject):
    """ Move the bottom object to be below the top object """
    bottom.y = top.y + top.height/2
    bottom.x = top.x

def attack_weapon(world: World, key: str):
    """ Moves the sword downwards when the player hits space"""
    if key == 'space':
        new_weapon = create_weapon()
        move_below(new_weapon, world.knight)
'''
def create_monster() -> DesignerObject:
    """ Create a monster randomly on the screen """
    monster = emoji('🧟')
    monster.scale_x = 1
    monster.scale_y = 1
    monster.anchor = 'midbottom'
    monster.x = randint(0, get_width())
    monster.y = get_height()
    return monster


def make_monster(world: World):
    """ Create a new monster at random times, if the monster cap has not been met """
    not_too_many_monsters = len(world.monster) < 15
    random_chance = randint(1, 80) == 40
    if not_too_many_monsters and random_chance:
        world.monster.append(create_monster())


when('starting', create_world)
when("typing", move_knight_horizontal)
when("typing", move_knight_vertical)
# when('typing', attack_weapon)
when("updating", boundaries)
when("updating", make_monster)
when("typing", direct_knight)
start()