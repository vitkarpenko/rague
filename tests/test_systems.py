def test_movement_system_on_dummy_entity_one_turn(world, dummy_entity):
    world.entities.add(dummy_entity)
    world.make_iteration()
    assert (
        dummy_entity.components['Position'].x
        == dummy_entity.components['Position'].y
        == 1
    )

def test_movement_system_on_dummy_entity_two_turns(world, dummy_entity):
    world.entities.add(dummy_entity)
    world.make_iteration()
    world.make_iteration()
    assert (
        dummy_entity.components['Position'].x
        == dummy_entity.components['Position'].y
        == 2
    )
