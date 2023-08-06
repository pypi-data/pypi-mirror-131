"""Declares various helper functions."""
import typing

import base64


def urlsafe_b64decode(value: typing.Union[bytes, str]):
    """Decode an URL-encoded Base64 octet sequence."""
    # Some implementations strip the padding.
    if isinstance(value, str):
        value = str.encode(value, 'ascii')
    return base64.urlsafe_b64decode(value + b'=' * (-len(value) % 4))
