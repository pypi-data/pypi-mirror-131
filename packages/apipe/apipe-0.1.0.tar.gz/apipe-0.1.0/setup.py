# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apipe']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.0.0,<3.0.0',
 'dask[delayed]>=2021.12.0,<2022.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'xxhash>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'apipe',
    'version': '0.1.0',
    'description': 'Data pipelines with lazy computation and caching',
    'long_description': "# dpipe\n\nData pipelines feat. lazy computation and caching\n\n## Installation\n\n```shell\npip install dpipe\n```\n\n## Example\n\n```python\nimport dpipe\nimport pandas as pd\nimport numpy as np\nfrom loguru import logger\n\n# --- Define data transformations via step functions (similar to dask.delayed)\n\n@dpipe.delayed_cached()  # lazy computation + caching on disk\ndef load_1():\n    df = pd.DataFrame({'a': [1., 2.], 'b': [0.1, np.nan]})\n    logger.info('Loaded {} records'.format(len(df)))\n    return df\n\n@dpipe.delayed_cached()  # lazy computation + caching on disk\ndef load_2(timestamp):\n    df = pd.DataFrame({'a': [0.9, 3.], 'b': [0.001, 1.]})\n    logger.info('Loaded {} records'.format(len(df)))\n    return df\n\n@dpipe.delayed_cached()  # lazy computation + caching on disk\ndef compute(x, y, eps):\n    assert x.shape == y.shape\n    diff = ((x - y).abs() / (y.abs()+eps)).mean().mean()\n    logger.info('Difference is computed')\n    return diff\n\n# --- Define pipeline dependencies\nts = pd.Timestamp(2019, 1, 1)\neps = 0.01\ns1 = load_1()\ns2 = load_2(ts)\ndiff = compute(s1, s2, eps)\n\n# --- Trigger pipeline execution\nprint('diff: {:.3f}'.format(dpipe.delayed_compute((diff, ))[0]))\n```\n",
    'author': 'Mysterious Ben',
    'author_email': 'datascience@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mysterious-ben/dpipe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
