import pytest

from b_aws_cf.credentials import Credentials
from b_aws_cf.exceptions.stack_does_not_exist import StackDoesNotExist
from b_aws_cf.stack import Stack


def test_FUNC_delete_WITH_existing_stack_EXPECT_stack_deleted(stack_fixture):
    stack_name, stack_id = stack_fixture
    Stack.from_name(stack_name).delete()


def test_FUNC_get_outputs_WITH_existing_stack_EXPECT_outputs_returned(stack_fixture):
    stack_name, stack_id = stack_fixture

    outputs = Stack.from_name(stack_name).get_outputs()
    assert outputs == {}


def test_FUNC_from_name_WITH_non_existing_stack_EXPECT_stack_returned():
    with pytest.raises(StackDoesNotExist):
        Stack.from_name('Some-Name-That-Does-Not-Exist-123abc')


def test_FUNC_from_name_WITH_existing_stack_EXPECT_stack_returned(stack_fixture):
    stack_name, stack_id = stack_fixture

    stack = Stack.from_name(stack_name)

    assert stack.stack_name == stack_name
    assert stack.stack_id == stack_id


def test_FUNC_deserialize_WITH_existing_stack_EXPECT_stack_deserialized(stack_fixture):
    stack_name, stack_id = stack_fixture

    description = (
        Credentials()
            .boto_session
            .client('cloudformation')
            .describe_stacks(StackName=stack_name)['Stacks'][0]
    )

    stack = Stack.deserialize(description)

    assert stack.stack_name == stack_name
    assert stack.stack_id == stack_id
