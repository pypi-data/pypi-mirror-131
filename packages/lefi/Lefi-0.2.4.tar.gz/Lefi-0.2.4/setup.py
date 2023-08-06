# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lefi',
 'lefi.exts',
 'lefi.exts.commands',
 'lefi.exts.commands.core',
 'lefi.exts.interactions',
 'lefi.objects',
 'lefi.objects.interactions',
 'lefi.utils',
 'lefi.voice',
 'lefi.ws']

package_data = \
{'': ['*'], 'lefi.voice': ['bin/*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0', 'aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'lefi',
    'version': '0.2.4',
    'description': 'A discord API wrapper focused on clean code, and usability',
    'long_description': '<div align="center">\n    <img src="https://github.com/an-dyy/Lefi/raw/master/docs/logo.png"</img>\n    <p>\n        <a href="https://lefi.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/lefi"</img></a>\n        <a href="https://pypi.org/project/lefi/"><img src="https://img.shields.io/pypi/dm/lefi?color=gre"</img></a>\n        <a href="https://discord.com/invite/QPFXzFbqrK"><img src="https://img.shields.io/discord/907106240537169980?label=discord"</img></a>\n        <a href="https://github.com/an-dyy/Lefi/releases"><img src="https://img.shields.io/github/v/release/an-dyy/lefi?include_prereleases&sort=semver"</img></a>\n    </p>\n    A discord API wrapper focused on clean code, and usability\n</div>\n\n\n## Installation\n\n1. Poetry\n\n   ```\n   poetry add lefi\n   ```\n\n2. Pip\n   ```\n   pip install lefi\n   ```\n\n## Example(s)\n[Here!](examples/)\n\n## Documentation\n[Here!](https://lefi.readthedocs.io/en/latest/)\n\n## Contributing\n1. If you plan on contributing please open an issue beforehand\n2. Fork the repo, and setup the poetry env (with dev dependencies)\n3. Install pre-commit hooks (*makes it a lot easier for me*)\n    ```\n    pre-commit install\n    ```\n\n## Join the discord!\n- [Discord](https://discord.gg/ZcAqDBaxRf)\n\n## Notable contributors\n\n- [blanketsucks](https://github.com/blanketsucks) - collaborator\n- [an-dyy](https://github.com/an-dyy) - creator and maintainer\n\n',
    'author': 'an-dyy',
    'author_email': 'andy.development@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/Lefi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
