def test_dummy_entity_has_components_set(dummy_entity):
    assert hasattr(dummy_entity, 'components')

def test_dummy_entity_components_set_is_not_empty(dummy_entity):
    assert dummy_entity.components != set()
