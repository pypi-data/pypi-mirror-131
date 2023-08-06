# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oryx',
 'oryx.bijectors',
 'oryx.core',
 'oryx.core.interpreters',
 'oryx.core.interpreters.inverse',
 'oryx.core.ppl',
 'oryx.core.state',
 'oryx.distributions',
 'oryx.experimental',
 'oryx.experimental.autoconj',
 'oryx.experimental.matching',
 'oryx.experimental.mcmc',
 'oryx.experimental.nn',
 'oryx.experimental.optimizers',
 'oryx.internal',
 'oryx.tools',
 'oryx.util']

package_data = \
{'': ['*']}

install_requires = \
['jax==0.2.26', 'jaxlib==0.1.75', 'tfp-nightly[jax]==0.16.0.dev20211216']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

setup_kwargs = {
    'name': 'oryx',
    'version': '0.2.2',
    'description': 'Probabilistic programming and deep learning in JAX',
    'long_description': None,
    'author': 'Google LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
