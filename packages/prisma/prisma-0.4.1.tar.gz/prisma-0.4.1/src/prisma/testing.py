import contextlib
from typing import Iterator, Optional

from . import client as _client
from .client import RegisteredClient
from .errors import ClientNotRegisteredError


@contextlib.contextmanager
def reset_client(new_client: Optional[RegisteredClient] = None) -> Iterator[None]:
    """Context manager to unregister the current client

    Once the context manager exits, the registered client is set back to it's original state
    """
    # pylint: disable=protected-access
    client = _client._registered_client
    if client is None:
        raise ClientNotRegisteredError()

    try:
        _client._registered_client = new_client
        yield
    finally:
        _client._registered_client = client
