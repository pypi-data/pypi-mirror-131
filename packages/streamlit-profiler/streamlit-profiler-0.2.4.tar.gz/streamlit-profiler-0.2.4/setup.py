# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_profiler']

package_data = \
{'': ['*']}

install_requires = \
['pyinstrument==4.1.1', 'streamlit>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-profiler',
    'version': '0.2.4',
    'description': 'Runtime profiler for Streamlit, powered by pyinstrument',
    'long_description': '# streamlit-profiler &nbsp;🏄🏼\n\n[![PyPi](https://img.shields.io/pypi/v/streamlit-profiler)](https://pypi.org/project/streamlit-profiler/)\n\n**Runtime profiler for Streamlit, powered by [pyinstrument](https://github.com/joerick/pyinstrument).**\n\nstreamlit-profiler is a [Streamlit component](https://streamlit.io/components) that\nhelps you find out which parts of your app are slow. It profiles the code via\n[pyinstrument](https://github.com/joerick/pyinstrument) and shows the results right\nwithin your Streamlit app.\n\n<sup>Alpha version, use with care.</sup>\n\n---\n\n<h3 align="center">\n  ⏱️ <a href="https://share.streamlit.io/jrieke/streamlit-profiler/main/examples/basic.py">Live demo</a> ⏱️\n</h3>\n\n---\n\n<p align="center">\n    <a href="https://share.streamlit.io/jrieke/streamlit-profiler/main/examples/basic.py"><img src="images/demo.png" width=600></a>\n</p>\n\n## Installation\n\n```bash\npip install streamlit-profiler\n```\n\n## Usage\n\n```python\nimport streamlit as st\nfrom streamlit_profiler import Profiler\n\nwith Profiler():\n    st.title("My app")\n    # ... other code\n\n# Or:\n# p = Profiler()\n# p.start()\n# ...\n# p.stop()\n```\n\nThen start your app as usual: `streamlit run my_app.py`\n\nThe `Profiler` class is an extension of `pyinstrument.Profiler`, so you can use\n[all of its functions](https://pyinstrument.readthedocs.io/en/latest/reference.html#pyinstrument.Profiler).\n',
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
