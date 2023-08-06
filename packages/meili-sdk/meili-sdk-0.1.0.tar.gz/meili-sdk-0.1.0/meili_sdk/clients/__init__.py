import json.decoder
import urllib.parse
import typing as t

import requests
from requests.exceptions import RequestException

from .apitoken_client import APITokenClient
from .base import BaseAPIClient
from .persistent_token_client import PersistentTokenClient
from .sdk_client import SDKClient

__all__ = (
    "APITokenClient",
    "PersistentTokenClient",
    "SDKClient",
    "get_client",
)


def get_client(token, host_override=None) -> t.Type[BaseAPIClient]:
    """
    Get client that will work with the token provided

    If an error occurs somewhere a default APITokenClient will be returned
    """
    from meili_sdk.site import get_host

    host = host_override or get_host()
    url = urllib.parse.urljoin(host, "api/token-evaluation/")

    try:
        response = requests.post(url, data={"key": token})
        if not response.ok:
            raise ValueError
        response_data = response.json()
        key_type = response_data["key_type"]
    except (RequestException, ValueError, json.decoder.JSONDecodeError, KeyError):
        return APITokenClient

    return {
        "SDKToken": SDKClient,
        "APIToken": APITokenClient,
        "PersistentToken": PersistentTokenClient,
    }[key_type](token, host)
