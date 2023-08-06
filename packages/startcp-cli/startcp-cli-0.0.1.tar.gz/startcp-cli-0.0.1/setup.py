import os
import re

from setuptools import setup, find_packages


setup(
    name='startcp-cli',
    author="Team Stark",
    version="0.0.1",
    url="https://github.com/asprazz/startcp-cli",
    description="A CLI boiler plate for current competition.",
    packages=["startcp"],
    install_requires=[
        'requests>=2.23',
        'argparse',
        'colorama',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'startcp=startcp.__main__:main'
        ]
    },
    author_email="ankushpatil6174@gmail.com",
    keywords=["startcp", "codechef", "codeforces", "python"],
    license="MIT"
)
