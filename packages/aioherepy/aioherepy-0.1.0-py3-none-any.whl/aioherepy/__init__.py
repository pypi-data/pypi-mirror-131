"""Asynchronous Python library that provides a simple interface to the HERE APIs."""

__author__ = "Abdullah Selek"
__email__ = "abdullahselek@gmail.com"
__copyright__ = "Copyright (c) 2021 Abdullah Selek"
__license__ = "MIT License"
__version__ = "0.1.0"
__url__ = "https://github.com/abdullahselek/aioherepy"
__download_url__ = "https://pypi.org/pypi/aioherepy"
__description__ = (
    "Asynchronous Python library that provides a simple interface to the HERE APIs."
)

from .here_enum import WeatherProductType

from .aiohere_api import AioHEREApi
from .here_error import (
    HEREError,
    HEREInvalidRequestError,
    HERETimeOutError,
    HEREUnauthorizedError,
)
