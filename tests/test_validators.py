import pytest

from nested_dataclasses.mixins import ValidationError


def test_nested_no_validation(nested_no_validation):
    assert not hasattr(nested_no_validation, "validate")


def test_nested_is_valid(valid_nested_typed_child):
    result = valid_nested_typed_child.validate()
    assert result is None


def test_parent_is_valid(valid_typed_parent):
    result = valid_typed_parent.validate()
    assert result is None


def test_invalid_nested_raises_error(invalid_nested_typed_child):
    with pytest.raises(ValidationError) as validator:
        invalid_nested_typed_child.validate()
    error_message = str(validator.value)
    number_of_errors = error_message.count("\n - ")
    assert number_of_errors == 5


def test_invalid_parent_raises_error(invalid_typed_parent):
    with pytest.raises(ValidationError) as validator:
        invalid_typed_parent.validate()
    error_message = str(validator.value)
    number_of_errors = error_message.count("\n - ")
    assert number_of_errors == 15


def test_nested_with_optional(nested_with_optional):
    result = nested_with_optional.validate()
    assert result is None
