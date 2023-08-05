# Copyright (c) 2021 Mindey.
# All Rights Reserved.

from setuptools import find_packages, setup

setup(
    name='mdrive',
    version='0.0.1',
    description='Metadrive as a service.',
    long_description='Data and Actions as a Service',
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/mindey/mdrive',
    author='Mindey',
    author_email='mindey@mindey.com',
    license='PROPRIETARY',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        # "fastapi==",
    ],
    extras_require={
        'develop': [
        ],
    },
    entry_points={
        'console_scripts': [
            'mdrive=mdrive.cli:hello',
        ],
    },
    zip_safe=False
)
