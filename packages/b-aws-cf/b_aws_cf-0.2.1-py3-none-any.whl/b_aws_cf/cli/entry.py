import argparse

from b_aws_cf.cli.delete import main_delete


def main():
    arg_parser = argparse.ArgumentParser(description='Cloudformation utilities.')

    choices = [
        'delete'
    ]

    arg_parser.add_argument(
        'action',
        choices=choices,
        help=f'CloudFormation actions. Choices: {choices}.'
    )

    params = arg_parser.parse_args()

    action = params.action

    if action == 'delete':
        main_delete()
