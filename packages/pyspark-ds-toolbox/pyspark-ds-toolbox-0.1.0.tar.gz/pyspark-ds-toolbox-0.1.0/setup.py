# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspark_ds_toolbox',
 'pyspark_ds_toolbox.causal_inference',
 'pyspark_ds_toolbox.ml',
 'pyspark_ds_toolbox.stats']

package_data = \
{'': ['*']}

install_requires = \
['databricks>=0.2,<0.3',
 'koalas>=1.8.2,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy==1.21.0',
 'pandas>=1.3.4,<2.0.0',
 'pyspark>=3.1.1,<4.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'typeguard>=2.13.2,<3.0.0']

setup_kwargs = {
    'name': 'pyspark-ds-toolbox',
    'version': '0.1.0',
    'description': 'A Pyspark companion for data science tasks.',
    'long_description': '# Pyspark DS Toolbox\n\n<!-- badges: start -->\n[![Lifecycle:\nexperimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyspark-ds-toolbox.svg)](https://pypi.org/project/pyspark-ds-toolbox/)\n[![Package Tests](https://github.com/viniciusmsousa/pyspark-ds-toolbox/actions/workflows/package-tests.yml/badge.svg)](https://github.com/viniciusmsousa/pyspark-ds-toolbox/actions)\n[![Codecov test coverage](https://codecov.io/gh/viniciusmsousa/pyspark-ds-toolbox/branch/main/graph/badge.svg)](https://codecov.io/gh/viniciusmsousa/pyspark-ds-toolbox?branch=main)\n<!-- badges: end -->\n\n\nThe objective of the package is to provide a set of tools that helps the daily work of data science with spark. The documentation can be found [here](https://viniciusmsousa.github.io/pyspark-ds-toolbox/index.html).\n\n\n## Installation\n\nDirectly from PyPi:\n```\npip install pyspark-ds-toolbox\n```\n\nor from github:\n```\npip install git+https://github.com/viniciusmsousa/pyspark-ds-toolbox.git\n```\n\n## Organization\n\nThe package is currently organized in a structure based on the nature of the task, such as data wrangling, model/prediction evaluation, and so on.\n\n```\npyspark_ds_toolbox     # Main Package\n├─ causal_inference    # Sub-package dedicated to Causal Inferece\n│  ├─ diff_in_diff.py   # Module Diff in Diff\n│  └─ ps_matching.py    # Module Propensity Score Matching\n├─ ml                  # Sub-package dedicated to ML\n│  ├─ data_prep.py      # Module for Data Preparation\n│  └─ eval.py           # Module for model/prediction evaluation\n├─ wrangling.py        # Module for general Data Wrangling\n└─ stats               # Sub-package dedicated to basic statistic functionalities\n   └─ association.py    # Association metrics module\n```\n\n',
    'author': 'vinicius.sousa',
    'author_email': 'vinisousa04@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viniciusmsousa/pyspark-ds-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
