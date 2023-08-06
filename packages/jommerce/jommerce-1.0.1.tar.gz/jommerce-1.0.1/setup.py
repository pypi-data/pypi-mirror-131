# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jommerce',
 'jommerce.auth',
 'jommerce.auth.migrations',
 'jommerce.project_template',
 'jommerce.project_template.project_name',
 'jommerce.settings']

package_data = \
{'': ['*'],
 'jommerce': ['static/css/*',
              'static/js/*',
              'templates/*',
              'templates/pages/*']}

install_requires = \
['Django==4']

extras_require = \
{'PostgreSQL': ['psycopg2>=2.5.4,<3.0.0']}

entry_points = \
{'console_scripts': ['jommerce = jommerce.__main__:main']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '1.0.1',
    'description': 'Jommerce',
    'long_description': '![Jommerce Version]\n![Python Version]\n![Django Version]\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n\n![Alt](https://repobeats.axiom.co/api/embed/7e78770ff262c113efb65f7b81e32e07941a2879.svg "Repobeats analytics image")\n\n\n<!-- MarkDown References -->\n[Django Version]: https://img.shields.io/pypi/djversions/jommerce\n[Python Version]: https://img.shields.io/pypi/pyversions/jommerce\n[Jommerce Version]: https://img.shields.io/pypi/v/jommerce\n',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jommerce/jommerce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
