"""
Optional setup.py for backward compatibility with pip < 21.0.
This project primarily uses pyproject.toml for configuration.
"""
from setuptools import setup

setup(
    name="svg_generator",
    entry_points={
        'console_scripts': [
            'svg-gen=svg_generator.cli:main',
        ],
    }
)
