# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydrinker']

package_data = \
{'': ['*']}

install_requires = \
['pydrinker-loafer>=1.0.1,<2.0.0']

extras_require = \
{'gcp': ['pydrinker-gcp>=1.1.2,<2.0.0']}

setup_kwargs = {
    'name': 'pydrinker',
    'version': '1.0.3',
    'description': 'The most amazing lib to drink (consume) message from your queue provider of preference',
    'long_description': '# pydrinker\n\n![build on github actions](https://github.com/pydrinker/pydrinker/actions/workflows/test.yml/badge.svg?branch=main)\n\nThis is a abstraction layer between [pydrinker-loafer](https://github.com/pydrinker/pydrinker-loafer) and all pydrinker libs, this project makes possible change thinks of original [olist-loafer](https://github.com/olist/olist-loafer) project, the future of this project is switch all core structure to here and remove pydrinker-loafer;\n\nTo understand more about pydrinker see [org page](https://github.com/pydrinker).\n',
    'author': 'Rafael Henrique da Silva Correia',
    'author_email': 'rafael@abraseucodigo.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafaelhenrique/pydrinker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
