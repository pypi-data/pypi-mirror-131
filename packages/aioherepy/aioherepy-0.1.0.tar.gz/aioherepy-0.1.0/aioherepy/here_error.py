"""Exceptions for aioHEREpy."""


class HEREError(Exception):
    """Generic aioHEREpy exception."""


class HERETimeOutError(HEREError):
    """Timeout while calling the API."""


class HEREUnauthorizedError(HEREError):
    """Invalid or missing api key."""


class HEREInvalidRequestError(HEREError):
    """Invalid request."""
