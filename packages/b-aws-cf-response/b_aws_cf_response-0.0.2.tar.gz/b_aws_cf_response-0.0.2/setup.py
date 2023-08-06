from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_aws_cf_response',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        '.venv',
        'b_aws_cf_response_tests',
    ]),
    description=(
        f'Package makes a response message from a custom resource provider event and sends a callback to '
        f'AWS CloudFormation service.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'urllib3>=1.26.6,<2.0.0',
        'pytest>=6.2.5,<7.0.0'
    ],
    author='Gediminas Kazlauskas',
    author_email='gediminas.kazlauskas@biomapas.com',
    keywords='AWS CloudFormation Response Custom Resource',
    url='https://github.com/Biomapas/B.AwsCfResponse.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
