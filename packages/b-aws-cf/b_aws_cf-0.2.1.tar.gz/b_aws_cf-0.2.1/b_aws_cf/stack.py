from datetime import datetime
from typing import Optional, Dict, Any

from botocore.exceptions import ClientError

from b_aws_cf.credentials import Credentials
from b_aws_cf.exceptions.stack_does_not_exist import StackDoesNotExist
from b_aws_cf.stack_status import StackStatus


class Stack:
    def __init__(
            self,
            stack_id: str,
            stack_name: str,
            description: str,
            creation_time: datetime,
            last_updated_time: datetime,
            deletion_time: datetime,
            stack_status: StackStatus,
            stack_status_reason: str,
            parent_id: str,
            root_id: str,
            drift_information: Dict[str, Any],
            credentials: Optional[Credentials] = None
    ):
        self.stack_id = stack_id
        self.stack_name = stack_name
        self.description = description
        self.creation_time = creation_time
        self.last_updated_time = last_updated_time
        self.deletion_time = deletion_time
        self.stack_status = stack_status
        self.stack_status_reason = stack_status_reason
        self.parent_id = parent_id
        self.root_id = root_id
        self.drift_information = drift_information

        self.__credentials = credentials or Credentials()
        self.__client = self.__credentials.boto_session.client('cloudformation')

    def __str__(self) -> str:
        return f'{self.stack_name:25} [{self.stack_status.name}]'

    def delete(self) -> None:
        self.__client.delete_stack(StackName=self.stack_name)

    def get_outputs(self) -> Dict[str, str]:
        stack = self.__client.describe_stacks(StackName=self.stack_name)['Stacks'][0]
        outputs = stack.get('Outputs') or []
        outputs = {out['OutputKey'] or out['ExportName']: out['OutputValue'] for out in outputs}
        return outputs

    @staticmethod
    def from_name(
            stack_name: str,
            credentials: Optional[Credentials] = None
    ) -> 'Stack':
        credentials = credentials or Credentials()
        client = credentials.boto_session.client('cloudformation')
        try:
            description = client.describe_stacks(StackName=stack_name)['Stacks'][0]
        except ClientError as ex:
            is_validation_err = ex.response.get('Error').get('Code') == 'ValidationError'
            is_does_not_exist_err = 'does not exist' in ex.response.get('Error').get('Message')
            if is_validation_err and is_does_not_exist_err:
                raise StackDoesNotExist(f'{stack_name} does not exist.')
            raise
        return Stack.deserialize(description)

    @staticmethod
    def deserialize(stack_summary: Dict[str, Any]) -> 'Stack':
        return Stack(
            stack_id=stack_summary['StackId'],
            stack_name=stack_summary['StackName'],
            description=stack_summary.get('TemplateDescription') or stack_summary.get('Description'),
            creation_time=stack_summary['CreationTime'],
            last_updated_time=stack_summary.get('LastUpdatedTime'),
            deletion_time=stack_summary.get('DeletionTime'),
            stack_status=StackStatus[stack_summary['StackStatus']],
            stack_status_reason=stack_summary.get('StackStatusReason'),
            parent_id=stack_summary.get('ParentId'),
            root_id=stack_summary.get('RootId'),
            drift_information=stack_summary.get('DriftInformation')
        )
