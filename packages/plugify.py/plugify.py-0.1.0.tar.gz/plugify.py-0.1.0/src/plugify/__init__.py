"""
plugify.py
~~~~~~~~~~
Pythonic API Wrapper For https://plugify.cf

:copyright: 2021 RPS
:license: Apache-2.0
"""

__title__ = "plugify"
__author__ = "RPS"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021 RPS"
__version__ = "0.1.0"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import logging
from typing import Literal, NamedTuple

from .client import *
from .dispatch import *
from .enums import *
from .gateway import *
from .group import *
from .http import *
from .member import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=1, micro=0, releaselevel="candidate", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
