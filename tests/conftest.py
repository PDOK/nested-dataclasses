import pytest
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

from nested_dataclasses import nested


TEST_STRING = "a string"
TEST_FLOAT = 1.1
TEST_INT = 1


@nested
@dataclass
class NestedChild:
    text: str


@nested
@dataclass
class NestedWithDefault:
    a_text: str
    text: str = TEST_STRING

    @property
    def a_string(self):
        return self.parent.text


@nested
@dataclass
class NestedWithOptional:
    text: Optional[str]


@nested
@dataclass
class NestedWithDefaultParent:
    text: str
    child: NestedWithDefault


@nested
@dataclass
class NestedParent:
    child_instances: List[NestedChild]
    a_string: str
    a_list: List[str]
    a_dict: Dict[str, str]


@nested
@dataclass
class NestedStack:
    child_instances: List[NestedParent]


@nested(validator=False)
@dataclass
class NestedNoValidation:
    text: str


@nested
@dataclass
class NestedTypedClass:
    integer: int
    string: str
    floating_point: float
    string_list: List[str]
    string_dict: Dict[str, str]


@nested
@dataclass
class TypedClassParent:
    nested_list: List[NestedTypedClass]
    nested_tuple: Tuple[NestedTypedClass]
    nested_dict: Dict[str, NestedTypedClass]


@pytest.fixture
def nested_child():
    return NestedChild(TEST_STRING)


@pytest.fixture
def nested_with_default():
    return NestedWithDefault(TEST_STRING)


@pytest.fixture
def nested_with_optional():
    return NestedWithOptional(None)


@pytest.fixture
def nested_parent_with_default(nested_with_default):
    return NestedWithDefaultParent(TEST_STRING, nested_with_default)


@pytest.fixture
def nested_parent(nested_child):
    nested_object = NestedParent(
        child_instances=[nested_child, nested_child],
        a_string=TEST_STRING,
        a_list=[TEST_STRING, TEST_STRING],
        a_dict={TEST_STRING: TEST_STRING},
    )
    return nested_object


@pytest.fixture
def nested_stack(nested_parent):
    nested_object = NestedStack([nested_parent, nested_parent])
    return nested_object


@pytest.fixture
def nested_no_validation():
    return NestedNoValidation(TEST_STRING)


@pytest.fixture
def valid_nested_typed_child():
    return NestedTypedClass(
        integer=TEST_INT,
        string=TEST_STRING,
        floating_point=1.1,
        string_list=[TEST_STRING, TEST_STRING],
        string_dict={TEST_STRING: TEST_STRING},
    )


@pytest.fixture
def invalid_nested_typed_child():
    return NestedTypedClass(
        integer=TEST_STRING,
        string=TEST_INT,
        floating_point=TEST_STRING,
        string_list=[
            TEST_INT,
        ],
        string_dict={TEST_STRING: TEST_INT},
    )


@pytest.fixture
def invalid_typed_parent(invalid_nested_typed_child):
    return TypedClassParent(
        nested_list=[
            invalid_nested_typed_child,
        ],
        nested_tuple=(invalid_nested_typed_child,),
        nested_dict={TEST_STRING: invalid_nested_typed_child},
    )


@pytest.fixture
def valid_typed_parent(valid_nested_typed_child):
    return TypedClassParent(
        nested_list=[
            valid_nested_typed_child,
        ],
        nested_tuple=(valid_nested_typed_child,),
        nested_dict={TEST_STRING: valid_nested_typed_child},
    )
