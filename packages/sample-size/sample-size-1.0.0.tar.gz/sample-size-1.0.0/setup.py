# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_size', 'sample_size.scripts']

package_data = \
{'': ['*']}

install_requires = \
['statsmodels>=0.13.1,<0.14.0']

entry_points = \
{'console_scripts': ['format = poetry_scripts:format_fix',
                     'format-check = poetry_scripts:format_check',
                     'lint = poetry_scripts:lint',
                     'qa = poetry_scripts:qa',
                     'run-sample-size = '
                     'sample_size.scripts.sample_size_run:main',
                     'test = poetry_scripts:test',
                     'type-check = poetry_scripts:type_check']}

setup_kwargs = {
    'name': 'sample-size',
    'version': '1.0.0',
    'description': 'A python module implementing power analysis to estimate sample size',
    'long_description': '# sample-size\n\nThis python project is a helper package that uses power analysis to calculate required sample size for any experiment.\n\n## Script Usage Guide\n\nSample size script lets you get the sample size estimation easily by providing metric inputs.\n\n### Requirements\n\nPlease make sure you have [Python 3](https://www.python.org/downloads/) installed before using the script.\n\n**Verify Python was installed** \n\n```bash\npython -V # python version should >=3.7.1, <3.11\n```\n\n**Verify pip was installed** \n```bash\npip -V \n```\n\n### Install the package\n\n```bash\npip install sample-size\npip show sample-size # verify package was installed\n```\n\n### Start using the script\n\n`run-sample-size` will promp you questions for you to enter the input it needs\n\n```bash\nrun-sample-size\n```\n\n### Script Constraints\n* This package supports \n  * Single metric per calculator for now\n  * Metric types: Boolean, Numeric, and Ratio\n* Default statistical power (80%) is used in `run-sample-size` all the time\n* Input constraints\n  * alpha: (0, 0.3]\n  * probability (Boolean Metric): (0, 1)\n  * variance (Numeric and Ratio Metrics): [0, <a href="https://www.codecogs.com/eqnedit.php?latex=\\small&space;&plus;\\infty" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\\small&space;&plus;\\infty" title="\\small +\\infty" /></a>)\n\n\n## Contributing\n\nAll contributors and contributions are welcome! Please see the [contributing docs](CONTRIBUTING.md) for more information.',
    'author': None,
    'author_email': None,
    'maintainer': 'GoDaddy',
    'maintainer_email': 'oss@godaddy.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
