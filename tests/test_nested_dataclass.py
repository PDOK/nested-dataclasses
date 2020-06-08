from .conftest import TEST_STRING


def test_child_without_parent_is_none(nested_child):
    assert nested_child.parent is None


def test_nested_with_default(nested_with_default):
    assert nested_with_default.text == TEST_STRING


def test_nested_parent_with_default(nested_parent_with_default):
    assert nested_parent_with_default.child.a_string == nested_parent_with_default.text


def test_nested_child_has_parent(nested_parent):
    assert nested_parent.parent is None
    assert nested_parent.child_instances[0].parent == nested_parent
    assert nested_parent.child_instances[1].parent == nested_parent


def test_nested_stack_children_have_parent(nested_stack):
    assert nested_stack.parent is None
    first_parent = nested_stack.child_instances[0].parent
    second_parent = nested_stack.child_instances[1].parent
    assert first_parent == nested_stack
    assert second_parent == nested_stack
    assert first_parent.child_instances[0].parent == first_parent
    assert first_parent.child_instances[1].parent == first_parent
    assert second_parent.child_instances[0].parent == second_parent
    assert second_parent.child_instances[1].parent == second_parent
