# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['keyboard_api']
setup_kwargs = {
    'name': 'keyboard-api',
    'version': '1.0.0',
    'description': 'KeyLog -> if you press a any button on your keyboard, this key was starting auto-save to file....',
    'long_description': None,
    'author': 'FlameNicoo',
    'author_email': '86409467+DiscordBotML@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
