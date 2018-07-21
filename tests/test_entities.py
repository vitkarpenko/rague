def test_dummy_entity_has_position(dummy_entity):
    assert hasattr(dummy_entity, 'position')


def test_dummy_entity_has_velocity(dummy_entity):
    assert hasattr(dummy_entity, 'velocity')
