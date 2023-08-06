import time
from typing import Optional, Iterator, List, Dict

from b_aws_cf.credentials import Credentials
from b_aws_cf.stack import Stack
from b_aws_cf.stack_status import StackStatus


class Stacks:
    def __init__(
            self,
            credentials: Optional[Credentials] = None
    ) -> None:
        self.__credentials = credentials or Credentials()
        self.__client = self.__credentials.boto_session.client('cloudformation')

    def list(
            self,
            stack_status_filter: Optional[List[StackStatus]] = None,
            name_prefix: Optional[str] = None
    ) -> Iterator[Stack]:
        next_token = None
        name_prefix = name_prefix or ''
        default_filter = StackStatus.to_list()
        # All deleted stacks for some time can be still accessed through API. One
        # AWS account may have hundreds of thousands of such deleted stacks.
        # Hence, simply filter our those stacks, when listing stacks.
        default_filter.remove(StackStatus.DELETE_COMPLETE)
        stack_filter = stack_status_filter or default_filter

        while True:
            kwargs = dict(StackStatusFilter=[s.name for s in stack_filter])
            if next_token: kwargs['NextToken'] = next_token

            response = self.__client.list_stacks(**kwargs)

            next_token = response.get('NextToken')
            stack_summaries = response.get('StackSummaries') or []

            for stack_summary in stack_summaries:
                stack = Stack.deserialize(stack_summary)

                if stack.stack_name.startswith(name_prefix):
                    yield stack

            if not next_token:
                break

    def get_outputs(self, stack_name: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Gets Cloud Formation stack outputs for all stacks or a specific stack.

        :param stack_name: A stack name for which to get its outputs.

        :return: A dictionary of outputs where keys are stack names and values are outputs.
        """
        stack_status_filter = [
            StackStatus.CREATE_COMPLETE,
            StackStatus.ROLLBACK_COMPLETE,
            StackStatus.UPDATE_COMPLETE_CLEANUP_IN_PROGRESS,
            StackStatus.UPDATE_COMPLETE,
            StackStatus.UPDATE_ROLLBACK_FAILED,
            StackStatus.UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS,
            StackStatus.UPDATE_ROLLBACK_COMPLETE,
            StackStatus.IMPORT_COMPLETE,
            StackStatus.IMPORT_ROLLBACK_COMPLETE,
        ]

        all_outputs = {}

        stacks = (
            [Stack.from_name(stack_name, self.__credentials)]
            if stack_name
            else list(self.list(stack_status_filter))
        )

        for stack in stacks:
            stack_outputs = stack.get_outputs()
            all_outputs[stack.stack_name] = stack_outputs

        return all_outputs

    def delete(self, name_prefix: Optional[str] = None):
        """
        Deletes all stacks that have a name which starts with a given prefix.

        :param name_prefix: Prefix to filter stacks.

        :return: No return.
        """
        self.__delete(name_prefix)

    def __delete(
            self,
            name_prefix: Optional[str] = None,
            previous_stacks: Optional[List[Stack]] = None,
            current_same_stacks_iteration: int = 0,
            max_same_stacks_iterations: int = 10,
            deletion_sleep_interval: int = 60
    ) -> None:
        allowed_stack_statuses_to_delete = [
            StackStatus.CREATE_IN_PROGRESS,
            StackStatus.CREATE_FAILED,
            StackStatus.CREATE_COMPLETE,
            StackStatus.ROLLBACK_FAILED,
            StackStatus.ROLLBACK_COMPLETE,
            StackStatus.UPDATE_COMPLETE,
            StackStatus.UPDATE_ROLLBACK_FAILED,
            StackStatus.UPDATE_ROLLBACK_COMPLETE,
            StackStatus.IMPORT_COMPLETE,
            StackStatus.IMPORT_ROLLBACK_FAILED,
            StackStatus.IMPORT_ROLLBACK_COMPLETE,
        ]

        if current_same_stacks_iteration == max_same_stacks_iterations:
            raise RecursionError('Max iterations reached. Existing script...')

        stacks = list(self.list(allowed_stack_statuses_to_delete, name_prefix))
        previous_stacks = previous_stacks or []

        if len(previous_stacks) == len(stacks):
            current_same_stacks_iteration += 1
            print(f'Previous stacks and current stacks are the same. Iteration: {current_same_stacks_iteration}.')
        else:
            current_same_stacks_iteration = 0
            print(f'Previous stacks len and current stacks len are different.')

        if stacks:
            for stack in stacks:
                print(f'Deleting stack: {stack.stack_name}.')
                stack.delete()

            print(f'Sleeping for {deletion_sleep_interval} seconds...')
            time.sleep(deletion_sleep_interval)
            self.__delete(name_prefix, stacks, current_same_stacks_iteration, max_same_stacks_iterations)
        else:
            print('No more stacks to delete.')
