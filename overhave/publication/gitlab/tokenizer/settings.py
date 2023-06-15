from typing import Any

import httpx
from pydantic import validator

from overhave.transport.http import BaseHttpClientSettings
from overhave.utils import make_url


class TokenizerClientSettings(BaseHttpClientSettings):
    """Important environments and settings for :class:`TokenizerClient`."""

    enabled: bool = False
    url: httpx.URL | None = None  # type: ignore
    initiator: str = "Overhave"
    remote_key: str | None = None
    remote_key_name: str | None = None

    class Config:
        env_prefix = "OVERHAVE_GITLAB_TOKENIZER_"

    @validator("url", pre=True)
    def make_url(cls, v: str | None) -> httpx.URL | None:
        return make_url(v)

    @validator("url", "remote_key", "remote_key_name")
    def validate_remote_key_and_initiator(cls, v: str | None, values: dict[str, Any]) -> str | None:
        if values.get("enabled") and not isinstance(v, str):
            raise ValueError("Please verify that url, remote_key and remote_key_name variables are not nullable!")
        return v
