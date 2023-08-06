# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_profiler']

package_data = \
{'': ['*']}

install_requires = \
['pyinstrument>=4.1.1,<5.0.0', 'streamlit>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-profiler',
    'version': '0.1.0',
    'description': 'Runtime profiler for Streamlit, powered by pyinstrument',
    'long_description': None,
    'author': 'Johannes Rieke',
    'author_email': 'johannes.rieke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
