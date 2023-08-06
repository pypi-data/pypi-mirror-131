import uuid
from os.path import dirname, abspath
from typing import Tuple, Callable, Optional

from pytest import fixture

from b_aws_cf.credentials import Credentials


@fixture(scope='function')
def stack_function_fixture() -> Callable:
    """
    Fixture that returns a function.
    The function creates a dummy CloudFormation stack.

    This fixture does automatic cleanup (deletes created stacks) after test run.

    :return: Callable function to create a stack.
    """

    stack_names = []

    def __create_stack(name_prefix: Optional[str] = None):
        stack_name = str(uuid.uuid4()).replace('-', '')
        stack_name = f'Stack{name_prefix or ""}{stack_name}'
        with open(f'{dirname(abspath(__file__))}/dummy_stack_template.yaml', 'r') as template_file:
            response = Credentials().boto_session.client('cloudformation').create_stack(
                StackName=stack_name,
                TemplateBody=template_file.read()
            )

        stack_names.append(stack_name)
        return stack_name, response['StackId']

    yield __create_stack

    for stack_name in stack_names:
        Credentials().boto_session.client('cloudformation').delete_stack(
            StackName=stack_name
        )


@fixture(scope='function')
def stack_fixture(stack_function_fixture) -> Tuple[str, str]:
    """
    Fixture that creates a dummy stack with dummy resources.

    :return: Tuple, where first element is stack name, and second element is stack id.
    """
    return stack_function_fixture()
