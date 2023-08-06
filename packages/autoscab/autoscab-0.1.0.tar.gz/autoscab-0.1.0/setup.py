# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoscab', 'autoscab.constants']

package_data = \
{'': ['*'], 'autoscab': ['captchaAudio/*']}

install_requires = \
['Faker>=10.0.0,<11.0.0',
 'SpeechRecognition>=3.8.1,<4.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'charset-normalizer>=2.0.9,<3.0.0',
 'fpdf>=1.7.2,<2.0.0',
 'idna>=3.3,<4.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'requests>=2.26.0,<3.0.0',
 'selenium>=3,<4',
 'urllib3>=1.26.7,<2.0.0',
 'webdriver-manager>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'autoscab',
    'version': '0.1.0',
    'description': 'apply for many of the same job',
    'long_description': None,
    'author': 'sneakers-the-rat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
