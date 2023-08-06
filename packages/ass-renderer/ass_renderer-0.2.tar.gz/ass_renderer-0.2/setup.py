# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ass_renderer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0', 'ass-parser>=1.0,<2.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'ass-renderer',
    'version': '0.2',
    'description': 'Render ASS subtitles as numpy bitmaps.',
    'long_description': 'ass_renderer\n==========\n\nA Python library for rendering ASS subtitle file format using libass.\n\n## Installation\n\n```\npip install --user ass-renderer\n```\n\n## Contributing\n\n```sh\n# Clone the repository:\ngit clone https://github.com/bubblesub/ass_renderer.git\ncd ass_renderer\n\n# Install to a local venv:\npoetry install\n\n# Install pre-commit hooks:\npoetry run pre-commit install\n\n# Enter the venv:\npoetry shell\n```\n\nThis project uses [poetry](https://python-poetry.org/) for packaging,\ninstall instructions at [poetry#installation](https://python-poetry.org/docs/#installation)\n',
    'author': 'Marcin Kurczewski',
    'author_email': 'dash@wind.garden',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bubblesub/ass_renderer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
