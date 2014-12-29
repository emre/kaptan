"""
    kaptan
    ~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from setuptools import find_packages, setup

setup(
    name='kaptan',
    version='0.5.8',
    packages=find_packages(),
    url='https://github.com/emre/kaptan',
    license='BSD',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Configuration Manager',
    install_requires=['PyYAML'],
    entry_points=dict(
        console_scripts=[
            'kaptan = kaptan:main',
        ],
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)

