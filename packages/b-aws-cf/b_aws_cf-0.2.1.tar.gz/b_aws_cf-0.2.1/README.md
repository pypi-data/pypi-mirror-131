# B.AwsCf

A python based package that enables convenient interaction with
CloudFormation service boto3 library.

### Description

Interacting with AWS CloudFormation service via boto3 is great.
However, boto3 is far too low-level library giving you great
flexibility but too less productivity. This B.AwsCf library makes
interaction with CloudFormation more object-oriented and more
high-level. It eliminates things like pagination with "NextToken"
and so on. 

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

### Related technology

- Python 3
- AWS CloudFormation
- boto3

### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS.
- You have basic-good knowledge in AWS CloudFormation.

### Useful sources

- What is CloudFormation?:<br>
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
  
- CloudFormation with boto3:<br>
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b_aws_cf
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

#### Programmatic usage

Two main constructs of this library is `Stack` and `Stacks`. The
`Stack` class lets you work with a single stack and `Stacks` class
lets you work with lists of stacks.

`Stack` class example.

```python
from b_aws_cf.stack import Stack

# Create stack object just by knowing its name:
stack = Stack.from_name('MyCoolStack')

# Gets this stack's outptus:
outputs = stack.get_outputs()

# Delete this stack:
stack.delete()
```

`Stacks` class example:

```python
from b_aws_cf.stacks import Stacks

# List all of the stacks in your account:
stacks = Stacks().list()

# Delete all of the stacks with some specific prefix:
Stacks().delete('MyPrefix')
```

#### CLI usage

The library exposes CLI commands. Run (to find about more):

```
cf --help
```

### Testing

This project has integration tests based on pytest. To run tests, simply run:

```
pytest
```

### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
