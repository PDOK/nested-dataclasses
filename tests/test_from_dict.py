import pytest

from .conftest import TEST_STRING


def test_child_without_parent_is_none(nested_child):
    assert nested_child.to_dict() == {"text": TEST_STRING}


def test_nested_with_default(nested_with_default):
    with pytest.raises(AttributeError):
        nested_with_default.to_dict()


def test_nested_parent_with_default(nested_parent_with_default):
    assert nested_parent_with_default.to_dict() == {
        "child": {"a_text": TEST_STRING, "text": TEST_STRING, "a_string": TEST_STRING},
        "text": TEST_STRING,
    }


def test_nested_child_has_parent(nested_parent):
    assert nested_parent.to_dict() == {
        "a_dict": {TEST_STRING: TEST_STRING},
        "a_list": [TEST_STRING, TEST_STRING],
        "a_string": TEST_STRING,
        "child_instances": [{"text": TEST_STRING}, {"text": TEST_STRING}],
    }


def test_nested_stack_children_have_parent(nested_stack):
    assert nested_stack.to_dict() == {
        "child_instances": [
            {
                "a_dict": {TEST_STRING: TEST_STRING},
                "a_list": [TEST_STRING, TEST_STRING],
                "a_string": TEST_STRING,
                "child_instances": [{"text": TEST_STRING}, {"text": TEST_STRING}],
            },
            {
                "a_dict": {TEST_STRING: TEST_STRING},
                "a_list": [TEST_STRING, TEST_STRING],
                "a_string": TEST_STRING,
                "child_instances": [{"text": TEST_STRING}, {"text": TEST_STRING}],
            },
        ]
    }
