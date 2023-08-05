# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paginator', 'paginator.composers']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.8.1,<14.0.0']

setup_kwargs = {
    'name': 'ptb-menu-pagination',
    'version': '0.2.1',
    'description': 'Creates google-like navigation menu using python-telegram-bot wrapper',
    'long_description': '# python telegram bot menu pagination\n![Actions Status](https://github.com/SergSm/ptb-menu-pagination/workflows/ci/badge.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/9eade003d09d837c852e/maintainability)](https://codeclimate.com/github/SergSm/ptb-menu-pagination/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/9eade003d09d837c852e/test_coverage)](https://codeclimate.com/github/SergSm/ptb-menu-pagination/test_coverage)\n\n# Description\n\nMakes a google style pagination line for a list of items.\n\n![](https://github.com/SergSm/ptb-menu-pagination/blob/main/example/media/example2.png)\n\nIn other words it builds a menu for navigation if you have \na lot of search results or whatever list of anything \n\n![](https://github.com/SergSm/ptb-menu-pagination/blob/main/example/media/example3.png)\n\n\n### Installation\n\n```\npip install ptb-menu-navigation\n```\n\n\nor if you are working with source code and use Poetry tool:\n\n```\nmake install\n```\n\n### Usage\n```python\nfrom paginator import get_menu\n```\n\n\nUse ```get_menu``` function to create a line of pages\n\n#### Example:\n```python\nfrom paginator import get_menu \nfrom dataclasses import dataclass\n\n# Define initial menu settings in the dataclass.\n@dataclass\nclass Menu:\n    items_per_page: int = 10\n    pages_per_line: int = 3\n    navigation_signature: str = \'±\'\n    page_label: str = \' p. \'\n\n# Add the initial call of get_menu\ndef handling_input(update, context):\n    # ...\n    # On first invocation\n    navigation = get_menu(total_items=len(search_results),\n                          current_page=1,\n                          menu_settings=Menu)\n    # ...\n\n# Add a callback to handle a page switching  \ndef navigate(update, context):\n    # ...\n    navigation = get_menu(total_items=len(search_results),\n                          current_page=int(current_page),\n                          menu_settings=Menu)     \n    # ...            \n```\nwhere ```search_results``` is a list of strings and ```current_page```\nis a number extracted from a ```callback_data```.\n\nSee ```examples/search_bot.py```\n\n### Demo bot launch\nCreate a ```.env``` file with a ```TOKEN``` variable\ninside of an ```/examples``` for launching \nthe\n[demo](https://github.com/SergSm/ptb-menu-pagination/blob/main/example/search_bot.py) bot.\\\neg:\\\n```TOKEN=<YOUR_TELEGRAM_BOT_TOKEN_FROM_BOT_FATHER>```\n\nYou may also provide some additional menu values in the same ```.env``` file:\n```\nITEMS_PER_PAGE=1\nPAGES_PER_LINE=1\nNAVIGATION_SIGNATURE="±"\nPAGE_LABEL=" p. "\n```\n',
    'author': 'Smirnov Sergey',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SergSm/ptb-menu-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
