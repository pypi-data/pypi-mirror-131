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
    'version': '0.1.1',
    'description': 'Runtime profiler for Streamlit, powered by pyinstrument',
    'long_description': '# streamlit-profiler &nbsp;🏄🏼\n\n[![PyPi](https://img.shields.io/pypi/v/streamlit-profiler)](https://pypi.org/project/streamlit-profiler/)\n\n**Runtime profiler for Streamlit, powered by [pyinstrument](https://github.com/joerick/pyinstrument).**\n\nstreamlit-profiler is a Streamlit component that helps you find out which parts of your\ncode are slow. It profiles code via [pyinstrument](https://github.com/joerick/pyinstrument)\nand shows the results right within the Streamlit app.\n\n<sup>Alpha version, use with care.</sup>\n\n<!--\n\n<h3 align="center">\n  🎉 <a href="https://github.com/jrieke/streamlit-profiler">Try it out</a> 🎉\n</h3>\n\n---\n\n<p align="center">\n    <a href="https://github.com/jrieke/readme-template"><img src="demo.gif" width=600></a>\n</p>\n-->\n\n## Installation\n\n```bash\npip install streamlit-profiler\n```\n\n## How to use it\n\n```python\nimport streamlit as st\nfrom streamlit_profiler import Profiler\n\nwith Profiler():\n    st.title("My app")\n    # ... and any other code\n```\n\n## TODOs\n\nPRs are welcome! If you want to work on any of these things, please open an issue to coordinate.\n\n- [ ] TBD\n',
    'author': 'Johannes Rieke',
    'author_email': 'johannes.rieke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jrieke/streamlit-profiler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
