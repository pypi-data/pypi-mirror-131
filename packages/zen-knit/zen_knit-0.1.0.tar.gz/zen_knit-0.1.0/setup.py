# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zen_knit',
 'zen_knit.data_types',
 'zen_knit.executor',
 'zen_knit.formattor',
 'zen_knit.formattor.html_support',
 'zen_knit.organizer',
 'zen_knit.parser',
 'zen_knit.reader']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'ipykernel>=6.6.0,<7.0.0',
 'ipython>=7.30.1,<8.0.0',
 'jupyter-client>=7.1.0,<8.0.0',
 'nbconvert>=6.3.0,<7.0.0',
 'nbformat>=5.1.3,<6.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['knit = zen_knit.cli:knit']}

setup_kwargs = {
    'name': 'zen-knit',
    'version': '0.1.0',
    'description': 'Zen-Knit is a formal (PDF), informal (HTML) report generator for data analyst and data scientist who wants to use python. Inspired from Pweave. ',
    'long_description': 'About Zen-Knit:\n---------------\n\nZen-Knit is a formal (PDF), informal (HTML) report generator for data analyst and data scientist who wants to use python. Inspired from Pweave. \nZen-Knit is good for creating reports, tutorials with embedded python\n\nFeatures:\n---------\n\n* Python 3.6+ compatibility\n* Support for IPython magics and rich output.\n* **Execute python code** in the chunks and **capture** input and output to a report.\n* **Use hidden code chunks,** i.e. code is executed, but not printed in the output file.\n* Capture matplotlib graphics.\n* Evaluate inline code in documentation chunks marked using ```{ }`` \n* Publish reports from Python scripts. Similar to R markdown.\n\nInstall\n-----------------------\n\nFrom PyPi::\n\n  pip install --upgrade zen_knit\n\nor download the source and run::\n\n  python setup.py install\n\n\n\nLicense information\n-------------------\n\nSee the file "LICENSE" for information on the history of this\nsoftware, terms & conditions for usage, and a DISCLAIMER OF ALL\nWARRANTIES.',
    'author': 'Zen',
    'author_email': 'zenreportz@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zen-Reportz/zen_knit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
