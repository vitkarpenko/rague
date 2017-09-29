import pyautogui

from rague.config import blt


def test_movement_system_on_dummy_entity_one_turn(world, dummy_entity):
    world.entities.add(dummy_entity)
    world.make_iteration()
    assert (
        dummy_entity.position.x
        == dummy_entity.position.y
        == 1
    )



def test_movement_system_on_paralyzed_dummy(world, dummy_entity):
    world.entities.add(dummy_entity)
    del dummy_entity.velocity
    while blt.has_input():
        world.make_iteration()
    assert (
        dummy_entity.position.x
        == dummy_entity.position.y
        == 0
    )


def test_player_up_movement(world, player):
    world.entities.add(player)
    pyautogui.typewrite(['up'])
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 0
        and player.position.y == -1
    )


def test_player_right_movement(world, player):
    world.entities.add(player)
    pyautogui.typewrite(['right'])
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 1
        and player.position.y == 0
    )


def test_player_circular_movement(world, player):
    world.entities.add(player)
    keys = ['up', 'right', 'down', 'left']
    pyautogui.typewrite(keys)
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 0
        and player.position.y == 0
    )
