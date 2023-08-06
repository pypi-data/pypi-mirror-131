from pathlib import Path

from setuptools import setup

setup(
    name='tendulkar_s3_aws',
    description='Python library for dashboard',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Shubham Tendulkar',
    author_email='shubhamtendulkar@gmail.com',
    url='https://github.com/tendulkar/tendulkar-utils',
    version='0.0.1',
    packages=[
        'tendulkar_s3_aws',
        'tendulkar_s3_aws/sdk'
    ],
    install_requires=['colorama', 'colorlog', 'requests']
)
