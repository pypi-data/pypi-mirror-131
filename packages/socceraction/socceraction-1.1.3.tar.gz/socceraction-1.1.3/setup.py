# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['socceraction',
 'socceraction.atomic',
 'socceraction.atomic.spadl',
 'socceraction.atomic.vaep',
 'socceraction.data',
 'socceraction.data.opta',
 'socceraction.data.opta.parsers',
 'socceraction.data.statsbomb',
 'socceraction.data.wyscout',
 'socceraction.spadl',
 'socceraction.vaep']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.2,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pandera>=0.7.1,<0.9.0',
 'requests>=2.26.0,<3.0.0',
 'scikit-learn>=0.24.2,<1.1.0']

setup_kwargs = {
    'name': 'socceraction',
    'version': '1.1.3',
    'description': 'Convert soccer event stream data to the SPADL format and value on-the-ball player actions',
    'long_description': '<div align="center">\n\t<img src="https://socceraction.readthedocs.io/en/latest/_static/logo_white.png" height="200">\n\t<p>\n\t<b>Convert soccer event stream data to the SPADL format<br/>and value on-the-ball player actions.</b>\n\t</p>\n\t<br/>\n\n[![PyPi](https://img.shields.io/pypi/v/socceraction.svg)](https://pypi.org/project/socceraction)\n[![Python Version: 3.7.1+](https://img.shields.io/badge/Python-3.7.1+-blue.svg)](https://pypi.org/project/socceraction)\n[![Downloads](https://img.shields.io/pypi/dm/socceraction.svg)](https://pypistats.org/packages/socceraction)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n\n[![Build Status](https://img.shields.io/github/workflow/status/ML-KULeuven/socceraction/CI?label=build&logo=github)](https://github.com/ML-KULeuven/socceraction/actions?workflow=CI)\n[![Read the Docs](https://img.shields.io/readthedocs/socceraction/latest.svg?label=Read%20the%20Docs)](https://socceraction.readthedocs.io)\n[![Code coverage](https://codecov.io/gh/ML-KULeuven/socceraction/branch/master/graph/badge.svg)](https://codecov.io/gh/ML-KULeuven/socceraction)\n\n<br/>\n<br/>\n</div>\n\nSocceraction is a Python package for objectively quantifying the impact of the individual actions performed by soccer players using event stream data. The general idea is to assign a value to each on-the-ball action based on the action\'s impact on the game outcome, while accounting for the context in which the action happened. The video below gives a quick two-minute introduction to action values.\n\n<div align="center">\n\nhttps://user-images.githubusercontent.com/2175271/136857714-1d2c8706-7f2f-449d-818f-0e67fbb75400.mp4\n\n</div>\n\n## Features\n\nSocceraction contains the following components:\n\n- Loaders for StatsBomb, Opta, Wyscout, StatsPerform and WhoScored data that enable **loading events and corresponding metadata** as Pandas DataFrames using a unified data model. [Read more »](https://socceraction.readthedocs.io/en/latest/modules/data.html)\n- Converters for event stream data to the **SPADL** and **atomic-SPADL** formats, which are unified and expressive languages for on-the-ball player actions. [Read more »](https://socceraction.readthedocs.io/en/latest/documentation/SPADL.html)\n- An implementation of the **xT** framework to value ball-progressing actions using a possession-based Markov model. [Read more »](https://socceraction.readthedocs.io/en/latest/documentation/xT.html)\n- An implementation of the **VAEP** and **Atomic-VAEP** frameworks to value actions on their expected impact on the score line. [Read more »](https://socceraction.readthedocs.io/en/latest/documentation/VAEP.html)\n\n## Installation / Getting started\n\nThe recommended way to install `socceraction` is to simply use pip. The latest version officially supports Python 3.7.1 - 3.9.\n\n```sh\n$ pip install socceraction\n```\n\nThe folder [`public-notebooks`](https://github.com/ML-KULeuven/socceraction/tree/master/public-notebooks) provides a demo of the full pipeline from raw StatsBomb event stream data to action values and player ratings. More detailed installation/usage instructions can be found in the [Documentation](https://socceraction.readthedocs.io/en/latest/).\n\n## Contributing\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. However, be aware that socceraction is not actively developed. It\'s primary use is to enable reproducibility of our research. If you believe there is a feature missing, feel free to raise a feature request, but please do be aware that the overwhelming likelihood is that your feature request will not be accepted.\nTo learn more on how to contribute, see the [Contributor Guide](https://socceraction.readthedocs.io/en/latest/development/developer_guide.html).\n\n## Research\n\nIf you make use of this package in your research, please consider citing the following papers:\n\n- Decroos, Tom, Lotte Bransen, Jan Van Haaren, and Jesse Davis. **Actions speak louder than goals: Valuing player actions in soccer.** In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1851-1861. 2019. <br/>[ [pdf](http://doi.acm.org/10.1145/3292500.3330758) | [bibtex](https://github.com/ML-KULeuven/socceraction/blob/master/docs/_static/decroos19.bibtex) ]\n\n- Maaike Van Roy, Pieter Robberechts, Tom Decroos, and Jesse Davis. **Valuing on-the-ball actions in soccer: a critical comparison of XT and VAEP.** In Proceedings of the AAAI-20 Workshop on Artifical Intelligence in Team Sports. AI in Team Sports Organising Committee, 2020. <br/>[ [pdf](https://limo.libis.be/primo-explore/fulldisplay?docid=LIRIAS2913207&context=L&vid=KULeuven&search_scope=ALL_CONTENT&tab=all_content_tab&lang=en_US) | [bibtex](https://github.com/ML-KULeuven/socceraction/blob/master/docs/_static/vanroy20.bibtex) ]\n\nThe Expected Threat (xT) framework was originally introduced by Karun Singh on his [blog](https://karun.in/blog/expected-threat.html) in 2019.\n\n## License\n\nDistributed under the terms of the [MIT license](https://opensource.org/licenses/MIT),\nsocceraction is free and open source software. Although not strictly required, we appreciate it if you include a link to this repo or cite our research in your work if you make use of socceraction.\n',
    'author': 'Tom Decroos',
    'author_email': 'tom.decroos.be@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ML-KULeuven/socceraction',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
