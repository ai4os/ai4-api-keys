"""Module to generate API keys."""

import enum
import json
import secrets

from ai4_api_keys import fernet


class APILevels(str, enum.Enum):
    """Levels of API keys."""

    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    PLATINUM = "platinum"


def create(key: str, scope: str, level: APILevels) -> str:
    """Create a new API key.

    :param key: The Fernet key to use.
    :param scope: The scope of the API key.
    :param level: The level of the API key.
    :return: The new API key.
    """
    message = {
        "nonce": secrets.token_hex(8),
        "scope": scope,
        "level": level.value,
    }

    return fernet.encrypt(key, json.dumps(message))


def validate(key: str, api_key: str, scope: str) -> bool:
    """Validate an API key.

    :param key: The Fernet key to use.
    :param api_key: The API key to validate.
    :param scope: The scope of the API key.
    :return: Whether the API key is valid.
    """
    try:
        decrypted = fernet.decrypt(key, api_key)
    except Exception:
        return False

    message = json.loads(decrypted)
    if message["scope"] != scope:
        return False
    return True
