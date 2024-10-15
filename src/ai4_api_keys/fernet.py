"""Manage AI4 Fernet signing keys."""

from typing_extensions import Annotated
from typing import Optional

import cryptography.fernet
import typer

app = typer.Typer(help="AI4 Fernet keys management CLI.")


@app.command(name="generate")
def generate_cli(
    output: Annotated[
        Optional[str],
        typer.Option("--output", "-o", help="Output file for the generated key."),
    ] = None,
) -> None:
    """Generate a new Fernet key."""
    key = generate()
    if output is None:
        typer.echo(key.decode())
    else:
        with open(output, "wb") as key_file:
            key_file.write(key)


def generate() -> bytes:
    """Generate a new Fernet key."""
    key = cryptography.fernet.Fernet.generate_key()
    return key


@app.command(name="encrypt")
def encrypt_cli(
    key: str = typer.Argument(..., help="The Fernet key to use."),
    data: str = typer.Argument(..., help="The data to encrypt."),
) -> None:
    """Encrypt data using a Fernet key (CLI)."""
    typer.echo(encrypt(key, data))


def encrypt(key: str, data: str) -> str:
    """Encrypt data using a Fernet key."""
    fernet = cryptography.fernet.Fernet(key.encode())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()


@app.command(name="decrypt")
def decrypt_cli(
    key: str = typer.Argument(..., help="The Fernet key to use."),
    data: str = typer.Argument(..., help="The data to decrypt."),
) -> None:
    """Decrypt data using a Fernet key (CLI)."""
    typer.echo(decrypt(key, data))


def decrypt(key: str, data: str) -> str:
    """Decrypt data using a Fernet key."""
    fernet = cryptography.fernet.Fernet(key.encode())
    decrypted_data = fernet.decrypt(data.encode())
    return decrypted_data.decode()
