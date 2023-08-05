# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync_my_tasks']

package_data = \
{'': ['*']}

install_requires = \
['asana>=0.10.3,<0.11.0', 'docopt>=0.6.2,<0.7.0', 'msal>=1.16.0,<2.0.0']

entry_points = \
{'console_scripts': ['sync-my-tasks = sync_my_tasks.command:main']}

setup_kwargs = {
    'name': 'sync-my-tasks',
    'version': '0.2.0',
    'description': 'Copy tasks between apps',
    'long_description': '\n<div align="center">\n  sync-my-tasks\n  <br />\n  Copy tasks between apps\n  <br />\n  <br />\n  <a href="https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:bug&template=bug_report.md&title=">Report a Bug</a>\n  ·\n  <a href="https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:enhancement&template=feature_request.md&title=">Request a Feature</a>\n  .\n  <a href="https://github.com/wilrnh/sync-my-tasks/discussions/categories/q-a">Ask a Question</a>\n</div>\n\n# Table of Contents\n<details open="open">\n<summary>Table of Contents</summary>\n\n- [Getting Started](#getting-started)\n- [Development](#development)\n- [Deployment](#deployment)\n- [Contribute](#contribute)\n- [License](#license)\n\n</details>\n\n# Getting Started\n[(Back to top)](#table-of-contents)\n\n## Installation\n\nInstall the app from Pypi:\n\n```sh\n# Install using pip\npip install sync-my-tasks\n\n# Run it\nsync-my-tasks -h\n\nsync-my-tasks.\n\nUsage:\n    sync-my-tasks (--from-asana --asana-workspace=<name> [--asana-token-file PATH])  (--to-mstodo)\n    sync-my-tasks (-h | --help)\n    sync-my-tasks --version\n\nOptions:\n  -h --help                   Show this screen.\n  --version                   Show version.\n  --from-asana                Pull tasks from Asana.\n  --asana-workspace=<name>    Name of workspace\n  --asana-token-file PATH     Path to file containing the Asana Personal token. [default: ./asana-token]\n  --to-mstodo                 Push tasks to Microsoft To-Do.\n```\n\n### Manual Installation:\n\n1. Clone the repo: `git clone https://github.com/wilrnh/sync-my-tasks.git`\n1. Install dependencies: `poetry install`\n1. Start the app: `python sync-my-tasks/command.py`\n\n## Usage\n\n### Asana\n\n### Microsoft To-Do\n\n# Development\n[(Back to top)](#table-of-contents)\n\n## Architecture\n\nsync-my-tasks is a CLI tool that copies tasks between apps. Since different apps provide varying APIs for the import and export of tasks, sync-my-tasks abstracts their functionality into _providers_ which are in charge of interfacing with their respective APIs and handling import and export.\n\nEach provider is responsible for either importing or exporting a well defined `list` of `TaskList`s, or both.\n\n`TaskList`: a named `list` of `Task`s\n`Task`: an object representing a task, that is generic enough to be imported/exported between any provider.\n\n# Deployment\n[(Back to top)](#table-of-contents)\n\nGithub Actions will automcatically build and deploy releases to [Pypi](https://pypi.org/project/sync-my-tasks/).\n\n# Contribute\n[(Back to top)](#table-of-contents)\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply [open an issue](https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:enhancement&template=feature_request.md&title=). Please feel free to [ask questions](https://github.com/wilrnh/sync-my-tasks/discussions/categories/q-a)!\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n# License\n[(Back to top)](#table-of-contents)\n\nDistributed under the MIT License. See `LICENSE` for more information.',
    'author': 'wilrnh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wilrnh/sync-my-tasks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
