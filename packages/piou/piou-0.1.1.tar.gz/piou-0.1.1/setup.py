# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piou']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.11.0,<11.0.0']

extras_require = \
{'pydantic': ['pydantic>=1.8.2,<2.0.0']}

setup_kwargs = {
    'name': 'piou',
    'version': '0.1.1',
    'description': 'A CLI tool',
    'long_description': "# Piou  \n\n\nA CLI tool to build beautiful command-line interfaces with type validation.\n\nIt is as simple as\n\n```python\nfrom piou import Parser, CmdArg\n\nparser = Parser(description='A CLI tool')\n\nparser.add_argument('-h', '--help', help='Display this help message')\nparser.add_argument('-q', '--quiet', help='Do not output any message')\nparser.add_argument('--verbose', help='Increase verbosity')\n\n\n@parser.command(cmd='foo',\n                help='Run foo command')\ndef foo_main(\n    foo1: int = CmdArg(..., help='Foo arguments'),\n    foo2: str = CmdArg('-f', '--foo2', help='Foo arguments')\n):\n    print('Ran foo main with ', foo1)\n    print('foo2: ', foo2)\n\n\n@parser.command(cmd='bar', help='Run bar command')\ndef bar_main():\n    pass\n\n\nif __name__ == '__main__':\n    parser.print_help()\n    parser.run()\n```\nThe output will look like this: \n\n![example](./docs/example.png)",
    'author': 'Julien Brayere',
    'author_email': 'julien.brayere@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andarius/pioupiou',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
