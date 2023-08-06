# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['colorie']
setup_kwargs = {
    'name': 'colorie',
    'version': '0.1.1',
    'description': 'ANSII Color formatting for output in terminal',
    'long_description': 'I am an upgraded version of [termcolor](https://pypi.org/project/termcolor/) that allows you to store colors as objects\nand use addition/calling to apply them to text. Color objects can also validate whether you use the correct color\nidentifiers upon creation, so all errors can be caught early.\n\n# Example\n```python\nimport sys\nfrom colorie import Color, colored, cprint\n\ntext = colored(\'Hello, World!\', \'red\', attrs=[\'reverse\', \'blink\'])\nprint(text)\ncprint(\'Hello, World!\', \'green\', \'on_red\')\n\nRED_ON_CYAN = Color(\'red\', \'on_cyan\')\nprint(RED_ON_CYAN + \'Hello, World!\')\nprint(RED_ON_CYAN(\'Hello, Universe!\'))\n\nfor i in range(10):\n    cprint(i, \'magenta\', end=\' \')\n\ncprint("Attention!", \'red\', attrs=[\'bold\'], file=sys.stderr)\n\nRED = Color(\'red\')\nON_WHITE = Color(highlight=\'on_white\')\nRED_ON_WHITE = RED + ON_WHITE\nprint(RED + "I am red" + " and I am red!")\nprint(RED + "I am red on white!" + ON_WHITE)\n```\n# Installation\n`pip install colorie`\n# Text Properties\n\n* Text colors\n    * grey\n    * red\n    * green\n    * yellow\n    * blue\n    * magenta\n    * cyan\n    * white\n\n* Text highlights\n    * on\\_grey\n    * on\\_red\n    * on\\_green\n    * on\\_yellow\n    * on\\_blue\n    * on\\_magenta\n    * on\\_cyan\n    * on\\_white\n\n* Attributes\n    * bold\n    * dark\n    * underline\n    * blink\n    * reverse\n    * concealed\n\n# Terminal properties\n\n> \n> \n> | Terminal     | bold    | dark | underline | blink      | reverse | concealed |\n> | ------------ | ------- | ---- | --------- | ---------- | ------- | --------- |\n> | xterm        | yes     | no   | yes       | bold       | yes     | yes       |\n> | linux        | yes     | yes  | bold      | yes        | yes     | no        |\n> | rxvt         | yes     | no   | yes       | bold/black | yes     | no        |\n> | dtterm       | yes     | yes  | yes       | reverse    | yes     | yes       |\n> | teraterm     | reverse | no   | yes       | rev/red    | yes     | no        |\n> | aixterm      | normal  | no   | yes       | no         | yes     | yes       |\n> | PuTTY        | color   | no   | yes       | no         | yes     | no        |\n> | Windows      | no      | no   | no        | no         | yes     | no        |\n> | Cygwin SSH   | yes     | no   | color     | color      | color   | yes       |\n> | Mac Terminal | yes     | no   | yes       | yes        | yes     | yes       |\n>\n',
    'author': 'Ovsyanka83',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/colorie',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
