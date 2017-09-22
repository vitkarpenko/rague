import pyautogui

from conftest import clear_input


def test_movement_system_on_dummy_entity_one_turn(world, dummy_entity):
    world.entities.add(dummy_entity)
    world.make_iteration()
    clear_input()
    assert (
        dummy_entity.components['Position'].x
        == dummy_entity.components['Position'].y
        == 1
    )



def test_movement_system_on_paralyzed_dummy(world, dummy_entity):
    world.entities.add(dummy_entity)
    del dummy_entity.components['Velocity']
    world.make_iteration()
    clear_input()
    assert (
        dummy_entity.components['Position'].x
        == dummy_entity.components['Position'].y
        == 0
    )


def test_player_up_movement(world, player):
    pyautogui.typewrite(['up'])
    world.make_iteration()
    clear_input()
    assert (
        player.components['Position'].x == 0
        and player.components['Position'].y == 1
    )


def test_player_right_movement(world, player):
    pyautogui.typewrite(['right'])
    world.make_iteration()
    clear_input()
    assert (
        player.components['Position'].x == 1
        and player.components['Position'].y == 0
    )


def test_player_circular_movement(world, player):
    keys = ['up', 'right', 'down', 'left']
    for key in keys:
        pyautogui.typewrite([key])
        world.make_iteration()
        clear_input()
    assert (
        player.components['Position'].x == 0
        and player.components['Position'].y == 0
    )
