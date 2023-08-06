# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minimal_pandas_api_for_polars',
 'minimal_pandas_api_for_polars.lib',
 'minimal_pandas_api_for_polars.lib.helpers',
 'minimal_pandas_api_for_polars.lib.interop',
 'minimal_pandas_api_for_polars.lib.pandas_api',
 'minimal_pandas_api_for_polars.lib.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['Bottleneck==1.3.2',
 'numexpr==2.8.1',
 'pandas==1.3.5',
 'polars==0.11.0',
 'pyarrow==6.0.1']

setup_kwargs = {
    'name': 'minimal-pandas-api-for-polars',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Austin Ray',
    'author_email': 'austin@hemmeter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
