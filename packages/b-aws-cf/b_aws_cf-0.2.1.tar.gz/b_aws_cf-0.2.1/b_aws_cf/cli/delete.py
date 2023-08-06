from b_aws_cf.credentials import Credentials

from b_aws_cf.stacks import Stacks


def main_delete() -> None:
    """
    Command that deletes all AWS CloudFormation stacks in a specified account.
    :return: No return.
    """
    profile = input('Name of the AWS profile: ')
    region = input('AWS region: ')
    prefix = input('Prefix of the stacks [None]: ') or None
    ans = input('Are you absolutely sure you want to delete all stacks? [y/n]: ')

    if ans == 'y':
        try:
            Stacks(Credentials(profile_name=profile, region_name=region)).delete(name_prefix=prefix)
        except RecursionError:
            stacks = Stacks(Credentials(profile_name=profile, region_name=region)).list(name_prefix=prefix)
            stacks_readable = '\n'.join([stack.stack_name for stack in stacks])

            print(f'Script finished execution. Stacks that were not deleted:\n{stacks_readable}.')
