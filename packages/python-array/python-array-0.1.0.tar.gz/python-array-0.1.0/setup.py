# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_array']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-array',
    'version': '0.1.0',
    'description': 'https://python-utilities.readthedocs.io/en/latest/array.html',
    'long_description': '# python-array\n\nSee https://python-utilities.readthedocs.io/en/latest/array.html\n\n## Install\n\n```\npip3 install -U python-array\n```\n\n## Usage\n\n```py\n>>> from python_array import CTypesView\n>>> text = bytearray(b"Hello, I am a simple ASCII string!")\n>>> ctview = CTypesView(text, itemsize=1)\n>>> ctview.view[0] = 0x61\n>>> print(text)\naello, I am a simple ASCII string!\n>>> ctview.to_uint16()[3] = 0x6554\n>>> print(text)\naello,Te am a simple ASCII string!\n```\n\n## License\n\nMIT\n\n## Contact\n\nMaintained by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!\n\nMy Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It\'s the best way to reach me, and I\'m always happy to hear from you.\n\n- Twitter: [@theshawwn](https://twitter.com/theshawwn)\n- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)\n- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)\n- Website: [shawwn.com](https://www.shawwn.com)\n\n',
    'author': 'Shawn Presser',
    'author_email': 'shawnpresser@gmail.com',
    'url': 'https://github.com/shawwn/python-array',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
