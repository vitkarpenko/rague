def test_dummy_entity(dummy_entity):
    assert hasattr(dummy_entity, 'components')
    assert dummy_entity.components != set()
