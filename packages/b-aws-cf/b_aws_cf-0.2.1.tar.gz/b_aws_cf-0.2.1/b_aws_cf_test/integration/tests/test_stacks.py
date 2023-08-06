from b_aws_cf.stacks import Stacks


def test_FUNC_list_WITH_multiple_stacks_EXPECT_list_returned(stack_function_fixture):
    names = []
    ids = []

    for i in range(5):
        stack_name, stack_id = stack_function_fixture('MyCoolTest')
        names.append(stack_name)
        ids.append(stack_id)

    for item in Stacks().list(name_prefix='MyCoolTest'):
        assert item.stack_name in names
        assert item.stack_id in ids


def test_FUNC_get_outputs_WITH_multiple_stacks_EXPECT_outputs_returned(stack_fixture):
    stack_name, stack_id = stack_fixture

    outputs = Stacks().get_outputs(stack_name)

    assert outputs == {stack_name: {}}


def test_FUNC_list_WITH_delete_EXPECT_list_returned(stack_function_fixture):
    names = []
    ids = []

    for i in range(5):
        stack_name, stack_id = stack_function_fixture('MyCoolTest')
        names.append(stack_name)
        ids.append(stack_id)

    Stacks().delete(name_prefix='MyCoolTest')
