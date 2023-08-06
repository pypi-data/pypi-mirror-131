# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imfpy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2,<4.0.0', 'pandas>=1.1.3,<2.0.0', 'requests>=2.19.0,<3.0.0']

setup_kwargs = {
    'name': 'imfpy',
    'version': '0.0.2',
    'description': "A client for interacting with the IMF's JSON RESTful API with Python!",
    'long_description': '# imfpy\n\nA package for interacting with the [IMF\'s JSON RESTful API](https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service) with Python!! In this preliminary phase, the package is a tool for understanding, retrieving and exploring Direction of Trade Statistics (DoTS) data. \n\nThis API client is intended to be useful for economic policymakers, researchers, government officials and more. The package enables the efficient retrieval of trade statistics from any country or country group over the span for which the IMF has data. Functions are designed to be easy-to-understand and adaptive to multiple query types.\n\nMoving forward, I will add more functionality to each module, so that users may retrieve and analyse data from other IMF databases.\n\n## Installation\n\n```python\n!pip install imfpy\n```\n\nDepends on:\n\n- python 3.7 and above\n- pandas 1.1.3 and above\n- requests 2.19.0 and above\n- matplotlib 3.2.2. and above\n\n## Usage\n\nThe package contains three modules:  \n\n* [`searches`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/searches/index.html)\n* [`retrievals`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/retrievals/index.html)\n* [`tools`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/tools/index.html)\n\n`searches` contains many helper functions that assist the user in searching through available IMF databases, dimensions, metadata and variables. \n\n`retrievals` contains functions that retrieve data from important databases. \n\nFor example, `retrievals.dots` pulls data from the DoTS database including imports, exports, two-way trade and trade balances for IMF countries and country-groups. The function handles flexible queries and formats the returned data to the user\'s specifications. \n\n```python\n#Example: retrieve Greece annual trade data\n>>> from imfpy.retrievals import dots\n>>> dots("GR", ["US", "AU", "DE"], 2000, 2005)\n```\n\n![](https://raw.githubusercontent.com/ltk2118/imfpy/main/img/usage5.png)\n\n`tools` contains functions that conduct rudimentary analysis and visualization on the data returned by `retrievals` functions. For example, the `dotsplot` function transforms the result of `dots()` into time series plots.\n\n```python\n#Example: plot Australia trade data\n>>> from imfpy.tools import dotsplot\n>>> d = dots(\'AU\',[\'US\',\'CN\'], 2000, 2020, freq=\'A\', form="long")\n>>> dotsplot(d, subset=[\'Trade Balance\', \'Twoway Trade\'])\n```\n\n<img src="https://raw.githubusercontent.com/ltk2118/imfpy/main/img/usage.png" style="zoom:50%;" />\n\n<img src="https://raw.githubusercontent.com/ltk2118/imfpy/main/img/usage2.png" style="zoom:50%;" />\n\n## Links\n\n**Documentation**\n\n* [User Guide/Vignette](https://imfpy.readthedocs.io/en/latest/example.html#user-guide)\n\n* [Full documentation](https://imfpy.readthedocs.io/en/latest/)\n\n* [API Reference](https://imfpy.readthedocs.io/en/latest/autoapi/index.html)\n\n**Distribution**\n\n* [Github Repo](https://github.com/ltk2118/imfpy)\n* [Github Dist](https://github.com/ltk2118/imfpy/tree/main/dist)\n* [PyPI](https://pypi.org/project/imfpy/)\n* [Test PyPI](https://test.pypi.org/project/imfpy/)\n\n**Testing**\n\n* [Pytests](https://github.com/ltk2118/imfpy/blob/main/tests/test_imfpy.py)\n\n**Extras**\n\n* [IMF DoTS](https://data.imf.org/?sk=9D6028D4-F14A-464C-A2F2-59B2CD424B85)\n* [My website](https://ltk2118.github.io/home/)\n\n## Contributing\n\nInterested in contributing? Want to use this package?  Please get in touch! Check out the contributing guidelines. \n\nPlease note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`imfpy` was created by Liam Tay Kearney. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`imfpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Liam Tay Kearney',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ltk2118/imfpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
