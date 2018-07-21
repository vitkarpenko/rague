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
        player.position.x == 5
        and player.position.y == 4
    )


def test_player_right_movement(world, player):
    world.entities.add(player)
    pyautogui.typewrite(['right'])
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 6
        and player.position.y == 5
    )


def test_player_circular_movement(world, player):
    world.entities.add(player)
    keys = ['up', 'right', 'down', 'left']
    pyautogui.typewrite(keys)
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 5
        and player.position.y == 5
    )


def test_player_not_passing_through_wall(world, player):
    world.entities.add(player)
    keys = ['right'] * 20
    pyautogui.typewrite(keys)
    while blt.has_input():
        world.make_iteration()
    assert (
        player.position.x == 9
        and player.position.y == 5
    )

