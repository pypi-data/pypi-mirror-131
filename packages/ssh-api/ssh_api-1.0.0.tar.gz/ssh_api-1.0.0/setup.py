# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ssh_api']
setup_kwargs = {
    'name': 'ssh-api',
    'version': '1.0.0',
    'description': "ssh api for make a ssh client's or code.... Main platform is windows 10,11.",
    'long_description': None,
    'author': 'OwoNicoo',
    'author_email': '86409467+DiscordBotML@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
