from pathlib import Path

from setuptools import setup

setup(
    name='10dulkar17_s3_aws',
    description='Python library for dashboard',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Shubham Tendulkar',
    author_email='shubham10dulkar17@gmail.com',
    url='https://github.com/10dulkar17/10dulkar17-utils',
    version='0.0.6',
    packages=[
        '10dulkar17_s3_aws',
        '10dulkar17_s3_aws/sdk'
    ],
    install_requires=['colorama', 'colorlog', 'requests']
)
