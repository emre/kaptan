from setuptools import setup

setup(
    name='kaptan',
    version='0.5.2',
    packages=['kaptan', 'kaptan.handlers'],
    url='http://github.com/emre/kaptan',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Configuration Manager',
    install_requires=['PyYAML', ],
    entry_points=dict(
        console_scripts=[
            'kaptan = kaptan:main',
        ],
    ),
)
