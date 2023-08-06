# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compsyn']

package_data = \
{'': ['*']}

install_requires = \
['IPython==7.13.0',
 'beautifulsoup4>=4.9.0,<5.0.0',
 'black>=19.10b0,<20.0',
 'boto3>=1.14.4,<2.0.0',
 'google-api-core>=1.14.3,<2.0.0',
 'google-auth>=1.6.3,<2.0.0',
 'google-cloud-vision>=0.39.0,<0.40.0',
 'google-cloud>=0.34.0,<0.35.0',
 'googleapis-common-protos>=1.6.0,<2.0.0',
 'grpcio>=1.28.1,<2.0.0',
 'ipykernel>=5.2.0,<6.0.0',
 'kymatio>=0.2.0,<0.3.0',
 'matplotlib>=3.2.1,<4.0.0',
 'memory_profiler>=0.57.0,<0.58.0',
 'nltk>=3.4.5,<4.0.0',
 'notebook>=6.0.3,<7.0.0',
 'numba>=0.48.0,<0.49.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pillow>=8.1.1,<9.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytest-depends>=1.0.1,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'qloader>=8.1.2,<9.0.0',
 'requests>=2.23.0,<3.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'seaborn>=0.10.0,<0.11.0',
 'textblob>=0.15.3,<0.16.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'compsyn',
    'version': '1.0.0',
    'description': 'python package to explore the color of language',
    'long_description': None,
    'author': 'comp-syn',
    'author_email': 'group@comp-syn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
