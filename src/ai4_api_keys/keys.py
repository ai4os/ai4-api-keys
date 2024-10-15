"""Module to generate API keys."""

import enum
import json
import pathlib
import secrets
from typing_extensions import Annotated
from typing import Optional

import typer

from ai4_api_keys import fernet


app = typer.Typer(help="AI4 API Keys management CLI.")


class APILevels(str, enum.Enum):
    """Levels of API keys."""

    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    PLATINUM = "platinum"


@app.command(name="create")
def create_cli(
    key_file: Annotated[
        Optional[pathlib.Path],
        typer.Option("--key-file", "-k", help="Read fernet key from a file."),
    ] = None,
    key: Annotated[
        Optional[str], typer.Option("--key", "-K", help="Use a specific fernet key.")
    ] = None,
    level: Annotated[
        APILevels,
        typer.Option("--level", "-l", help="The level of the API key."),
    ] = APILevels.BRONZE,
    scope: Annotated[
        str, typer.Option("--scope", "-s", help="The scope of the API key.")
    ] = "ai4eosc",
) -> None:
    """Create a new API key (CLI)."""
    if key_file and key:
        raise typer.BadParameter("Cannot use both --key-file and --key.")

    if key_file is not None:
        with open(key_file, "r") as f:
            key = f.read().strip()

    if key is None:
        raise typer.BadParameter("Either --key-file or --key must be provided.")

    typer.echo(create(key, scope, level))


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


@app.command(name="validate")
def validate_cli(
    key_file: Annotated[
        Optional[pathlib.Path],
        typer.Option("--key-file", "-k", help="Read fernet key from a file."),
    ] = None,
    key: Annotated[
        Optional[str], typer.Option("--key", "-K", help="Use a specific fernet key.")
    ] = None,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Do not print the result.")
    ] = False,
    scope: str = typer.Argument("ai4eosc", help="The scope of the API key."),
    api_key: str = typer.Argument(..., help="The API key to validate."),
) -> None:
    """Validate an API key (CLI)."""
    if key_file and key:
        raise typer.BadParameter("Cannot use both --key-file and --key.")

    if key_file is not None:
        with open(key_file, "r") as f:
            key = f.read().strip()

    if key is None:
        raise typer.BadParameter("Either --key-file or --key must be provided.")

    valid = validate(key, api_key, scope)

    if valid:
        if not quiet:
            typer.echo("API key is valid.")
    else:
        if not quiet:
            typer.echo("API key is invalid.")
        raise typer.Exit(code=1)


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
