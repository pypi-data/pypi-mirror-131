from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_aws_cf',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_aws_cf_test'
    ]),
    description=(
        'Various utilities that wrap around boto3 for CloudFormation service.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cf=b_aws_cf.cli.entry:main',
        ],
    },
    install_requires=[
        'pytest',
        'boto3>=1.0.0,<=1.20.23',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='AWS IAC CDK Parallel',
    url='https://github.com/biomapas/B.AwsCf.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
