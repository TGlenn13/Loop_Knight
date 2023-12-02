from designer import *
from dataclasses import dataclass
from random import randint

background_image("images/grass.jpg")

KNIGHT_SPEED = 15
PLAYER_HEALTH = 5
SWORD = emoji("🔪")
MONSTER_HEALTH = 1
ATTACKING = False
SKULL = emoji("💀")
@dataclass
class World:
    sword_timer: int
    score: int
    knight: DesignerObject
    knight_speed: int
    monster: list[DesignerObject]
    monster_health: int
    # tier_2_monster: list[DesignerObject]
    # boss: list[DesignerObject]
    sword: DesignerObject
    weapons: list[DesignerObject]
    player_health: int
    counter: DesignerObject
    attacking: bool
    #skull: DesignerObject
    # weapons: list[DesignerObject]
    # wave_number: int


def create_world() -> World:
    return World(0, 0, create_knight(), KNIGHT_SPEED, [], MONSTER_HEALTH, SWORD, [], PLAYER_HEALTH,
                 text("black", "Health: " + str(PLAYER_HEALTH),  40, get_width() // 2, 30), ATTACKING)
when('starting', create_world)

def create_knight() -> DesignerObject:
    """ Create the knight """
    knight = emoji("🥷")
    knight.y = get_height() / 2
    knight.x = get_width() / 2
    return knight


def move_knight_horizontal(world: World, key: str):
    """ Move the knight and sword horizontally"""
    if key == "d":
        world.knight.x += world.knight_speed
        world.sword.x += world.knight_speed
    elif key == "a":
        world.knight.x -= world.knight_speed
        world.sword.x -= world.knight_speed
when("typing", move_knight_horizontal)

def move_knight_vertical(world: World, key: str):
    """ Move the knight and sword vertically"""
    if key == "w":
        world.knight.y -= world.knight_speed
        world.sword.y -= world.knight_speed
    elif key == "s":
        world.knight.y += world.knight_speed
        world.sword.y += world.knight_speed
when("typing", move_knight_vertical)

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
when("updating", boundaries)

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
when("typing", direct_knight)

def create_weapon() -> DesignerObject:
    """ Create a weapon. For now swords only"""
    return SWORD


def move_below(bottom: DesignerObject, top: DesignerObject):
    """ Move the bottom object to be below the top object """
    bottom.y = top.y + top.height/2 + 10
    bottom.x = top.x

def attack_weapon(world: World, key: str):
    """ Moves the sword downwards when the player hits space,
     and back up after hitting space again"""
    if key == 'space':
        if world.sword.y == world.knight.y:
            new_weapon = create_weapon()
            move_below(new_weapon, world.knight)
            world.weapons.append(new_weapon)
            world.attacking = True
            world.sword_timer = 15
when('typing', attack_weapon)

def update_timer(world: World):
    """"Updates the timer after the,
    player has attacked. When the timer,
    reaches 0 the sword resets"""
    if world.sword_timer > 0:
        world.sword_timer -= 1
    else:
        world.attacking = False
        world.sword.y = world.knight.y
when("updating", update_timer)

def create_monster() -> DesignerObject:
    """ Create a monster randomly on the screen """
    monster = emoji('🧟')
    monster.scale_x = 3
    monster.scale_y = 3
    monster.anchor = 'midbottom'
    monster.x = randint(0, get_width())
    monster.y = get_height()
    return monster


def make_monster(world: World):
    """ Create a new monster at random times, if the monster cap has not been met """
    #not_too_many_monsters = len(world.monster) < 15
    random_chance = randint(1, 30) == 15
    if random_chance:
        world.monster.append(create_monster())
when("updating", make_monster)

def monster_movement(world: World):
    """Moves the monster upwards and horizontally slowly.
    If the monster reaches the top they spawn back in
    at the bottom"""
    for monster in world.monster:
        monster.x += randint(-20,20)
        monster.y -= 2
        if monster.y <= 0:
            monster.y = get_height()
when("updating", monster_movement)

def monster_boundaries(world: World):
    """keeps the monster within the screen"""
    for monster in world.monster:
        if monster.x > get_width():
            monster.x = get_width() - 3
        if monster.x <= 0:
            monster.x = 3
when("updating", monster_boundaries)

def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    """Filters unwanted data from a list"""
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

def damage_monster(world: World):
    """Damages monsters when weapon collides with them. Removes dead monsters"""
    killed_monsters = []
    for monster in world.monster:
        if world.attacking:
            if colliding(world.sword, monster):
                killed_monsters.append(monster)
                world.score += 1
    world.monster = filter_from(world.monster, killed_monsters)
when("updating", damage_monster)

'''
def flash_skull(world: World):
    timer = 10
    for time in timer:
        timer -= 1
'''
def update_health(world):
    """Updates the health displayed"""
    world.counter.text = "Health: " + str(world.player_health)
when("updating", update_health)

def damage_player(world: World):
    """Damages the player when they run into a monster,
    This kills the monster too"""
    dead_monster = []
    for monster in world.monster:
        if colliding(world.knight, monster):
            world.player_health -= 1
            dead_monster.append(monster)
            world.monster = filter_from(world.monster, dead_monster)
when("updating", damage_player)

def player_has_no_health(world: World) -> bool:
    """checks players health and returns a bool of if the player has health or not"""
    no_health = False
    if world.player_health <= 0:
        no_health = True
    return no_health

def game_over(world: World):
    world.counter.text = "GAME OVER! YOU HAVE SLAIN " + str(world.score) + " MONSTERS!"
    for monster in world.monster:
        destroy(monster)
when(player_has_no_health, game_over, pause)

start()