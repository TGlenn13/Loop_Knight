from designer import *
from dataclasses import dataclass
from random import randint

background_image("images/grass.jpg")

KNIGHT_SPEED = 20
PLAYER_HEALTH = 5
SWORD = emoji("🔪")
ATTACKING = False
@dataclass
class World:
    sword_timer: int
    score: int
    knight: DesignerObject
    knight_speed: int
    monster: list[DesignerObject]
    boss: list[DesignerObject]
    sword: DesignerObject
    weapons: list[DesignerObject]
    player_health: int
    counter: DesignerObject
    attacking: bool


def create_world() -> World:
    return World(0, 0, create_knight(), KNIGHT_SPEED, [], [], SWORD, [], PLAYER_HEALTH,
                 text("black", "Health: " + str(PLAYER_HEALTH),  40, get_width() // 2, 30), ATTACKING)
when('starting', create_world)

def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    """Filters unwanted data from a list"""
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

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

def create_boss() -> DesignerObject:
    """Creates a boss randomly on the screen"""
    boss = emoji("👹")
    boss.scale_x = 5
    boss.scale_y = 5
    boss.anchor = 'midbottom'
    boss.x = randint(0, get_width())
    boss.y = get_height()
    return boss

def make_boss(world: World):
    """ Create a boss at random times"""
    random_chance = randint(1, 75) == 50
    if random_chance:
        world.boss.append(create_boss())
when("updating", make_boss)

def boss_movement(world: World):
    """Moves the boss upwards and horizontally quickly.
    If the boss reaches the top they spawn back in
    at the bottom"""
    for boss in world.boss:
        boss.x += randint(-60,60)
        boss.y -= 1
        if boss.y <= 0:
            boss.y = get_height()
when("updating", boss_movement)

def boss_boundaries(world: World):
    """keeps the boss within the screen"""
    for boss in world.boss:
        if boss.x > get_width():
            boss.x = get_width() - 3
        if boss.x <= 0:
            boss.x = 3
when("updating", boss_boundaries)

def damage_boss(world: World):
    """Damages boss when a weapon collides with them. Removes dead bosses"""
    killed_bosses = []
    for boss in world.boss:
        if world.attacking:
            if colliding(world.sword, boss):
                killed_bosses.append(boss)
                world.score += 1
    world.boss = filter_from(world.boss, killed_bosses)
when("updating", damage_boss)

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
    """ Create a new monster at random times """
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

def kill_monster(world: World):
    """Damages monsters when a weapon collides with them. Removes dead monsters"""
    killed_monsters = []
    for monster in world.monster:
        if world.attacking:
            if colliding(world.sword, monster):
                killed_monsters.append(monster)
                world.score += 1
    world.monster = filter_from(world.monster, killed_monsters)
when("updating", kill_monster)

def update_health(world):
    """Updates the health displayed"""
   world.counter.text = "Health: " + str(world.player_health)
when("updating", update_health)

def monster_damages_player(world: World):
    """Damages the player when they run into a monster,
    This kills the monster too"""
    dead_monster = []
    for monster in world.monster:
        if colliding(world.knight, monster):
            world.player_health -= 1
            dead_monster.append(monster)
            world.monster = filter_from(world.monster, dead_monster)
when("updating", monster_damages_player)

def boss_damages_player(world: World):
    """Damages the player when they run into a monster,
    This kills the monster too"""
    dead_boss = []
    for boss in world.boss:
        if colliding(world.knight, boss):
            world.player_health -= 1
            dead_boss.append(boss)
            world.boss = filter_from(world.boss, dead_boss)
when("updating", boss_damages_player)

def player_has_no_health(world: World) -> bool:
    """checks players health and returns a bool of if the player has health or not"""
    no_health = False
    if world.player_health <= 0:
        no_health = True
    return no_health

def game_over(world: World):
    """Game over screen when the player dies,
    All monsters are wiped from the screen"""
    if world.score == 1:
        world.counter.text = "GAME OVER! YOU HAVE SLAIN " + str(world.score) + " MONSTER!"
    else:
        world.counter.text = "GAME OVER! YOU HAVE SLAIN " + str(world.score) + " MONSTERS!"
    for monster in world.monster:
        destroy(monster)
    for boss in world.boss:
        destroy(boss)
when(player_has_no_health, game_over, pause)

start()