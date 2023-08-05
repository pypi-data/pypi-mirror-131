#  AUTHOR: Roman Bergman <roman.bergman@protonmail.com>
# LICENSE: AGPL3.0
# VERSION: 0.0.2

import setuptools

setuptools.setup(
    entry_points={
        'console_scripts': [
            'my-pwd = pwdgen.soft:main',
        ]
  }
)
