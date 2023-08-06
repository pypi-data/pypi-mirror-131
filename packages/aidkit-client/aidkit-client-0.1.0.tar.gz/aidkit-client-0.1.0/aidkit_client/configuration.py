from typing import Optional

from aidkit_client.aidkit_api import AidkitApi, HTTPService
from aidkit_client.exceptions import AidkitClientNotConfiguredError


def configure(base_url: str, auth_token: str) -> None:
    # we allow global setting of the configurations parameters
    global _GLOBAL_API_SERVICE  # pylint: disable=global-statement
    _GLOBAL_API_SERVICE = AidkitApi(base_url=base_url, auth_token=auth_token)


_GLOBAL_API_SERVICE: Optional[HTTPService] = None


def get_api_client() -> HTTPService:
    if _GLOBAL_API_SERVICE is None:
        raise AidkitClientNotConfiguredError(
            """aidkit must be configured first.
        Run `aidkit_client.configure(BASE_URL, AUTH_TOKEN)` before calling any other method."""
        )
    return _GLOBAL_API_SERVICE
