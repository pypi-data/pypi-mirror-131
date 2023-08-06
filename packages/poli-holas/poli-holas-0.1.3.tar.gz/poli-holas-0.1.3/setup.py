# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poli_holas']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.14.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['poli-holas = poli_holas.__main__:app']}

setup_kwargs = {
    'name': 'poli-holas',
    'version': '0.1.3',
    'description': 'Saludar en múltiples idiomas',
    'long_description': '# poli-holas\n\n<div align="center">\n\n\n[![Python Version](https://img.shields.io/pypi/pyversions/poli-holas.svg)](https://pypi.org/project/poli-holas/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/fraediaz/poli-holas/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/fraediaz/poli-holas/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/fraediaz/poli-holas/releases)\n[![License](https://img.shields.io/github/license/fraediaz/poli-holas)](https://github.com/fraediaz/poli-holas/blob/master/LICENSE)\n\n\nSaludar en múltiples idiomas\n\n</div>\n\n\n## Installation\n\n```bash\npip install -U poli-holas\n```\n\n\nThen you can run\n```bash\npoli-holas --help\n```\n\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/fraediaz/poli-holas/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\n### List of labels and corresponding titles\n\n|               **Label**               |  **Title in Releases**  |\n| :-----------------------------------: | :---------------------: |\n|       `enhancement`, `feature`        |       🚀 Features       |\n| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |\n|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |\n|              `breaking`               |   💥 Breaking Changes   |\n|            `documentation`            |    📝 Documentation     |\n|            `dependencies`             | ⬆️ Dependencies updates |\n\nYou can update it in [`release-drafter.yml`](https://github.com/fraediaz/poli-holas/blob/master/.github/release-drafter.yml).\n\nGitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/fraediaz/poli-holas)](https://github.com/fraediaz/poli-holas/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/fraediaz/poli-holas/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{poli-holas,\n  author = {fraediaz},\n  title = {Saludar en múltiples idiomas},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/fraediaz/poli-holas}}\n}\n```\n',
    'author': 'fraediaz',
    'author_email': 'fraediaz@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fraediaz/poli-holas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
