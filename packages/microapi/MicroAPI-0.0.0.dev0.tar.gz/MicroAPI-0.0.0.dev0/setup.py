# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['MicroAPI']

package_data = \
{'': ['*']}

install_requires = \
['FastAPI>=0.70.1,<0.71.0', 'SQLModel>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'microapi',
    'version': '0.0.0.dev0',
    'description': 'FastAPI on low-power devices',
    'long_description': '# FastAPI on low-power devices\n',
    'author': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/FastAIAPI/MicroAPI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
