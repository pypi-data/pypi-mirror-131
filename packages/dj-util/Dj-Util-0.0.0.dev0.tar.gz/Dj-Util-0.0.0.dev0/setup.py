# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djutil']

package_data = \
{'': ['*']}

install_requires = \
['Django-Autocomplete-Light>=3.9.0rc5,<4.0.0',
 'Django-Model-Utils>=4.2.0,<5.0.0',
 'Django>=4.0,<5.0']

setup_kwargs = {
    'name': 'dj-util',
    'version': '0.0.0.dev0',
    'description': 'Django Utilities',
    'long_description': '# Django Utilities\n',
    'author': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Django-AI/DjUtil',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
