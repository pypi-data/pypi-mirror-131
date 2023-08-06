# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concatenate']

package_data = \
{'': ['*']}

install_requires = \
['registrate>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'concatenate',
    'version': '0.1.1',
    'description': 'Concatenate two objects of the same type',
    'long_description': "# concatenate\nConcatenate two objects of the same type\n\n## Installation\n```sh\npip install concatenate\n```\n\n## Usage\n```python\n>>> from concatenate import concatenate\n>>>\n>>> # int\n>>> assert concatenate(123, 456) == 123456\n>>> assert concatenate(0xdead, 0xbeef, base=16) == 0xdeadbeef\n>>> assert concatenate(0b1010, 0b1100, base=2) == 0b10101100\n>>> assert concatenate(0o137, 0o246, base=8) == 0o137246\n>>>\n>>> # str\n>>> assert concatenate('foo', 'bar') == 'foobar'\n>>>\n>>> # dict\n>>> assert concatenate({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}\n>>>\n>>> # list\n>>> assert concatenate([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]\n>>>\n>>> # tuple\n>>> assert concatenate((1, 2, 3), (4, 5, 6)) == (1, 2, 3, 4, 5, 6)\n>>>\n>>> # set\n>>> assert concatenate({1, 2, 3}, {3, 4, 5}) == {1, 2, 3, 4, 5}\n```",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/concatenate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
