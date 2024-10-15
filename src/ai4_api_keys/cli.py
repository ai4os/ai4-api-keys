"""Command line interface for the ai4-api-keys package."""

import typer

import ai4_api_keys
import ai4_api_keys.keys
import ai4_api_keys.fernet

app = typer.Typer(help="AI4 API Keys management CLI.")
app.add_typer(ai4_api_keys.fernet.app, name="fernet")
app.add_typer(ai4_api_keys.keys.app, name="keys")


def version_callback(value: bool):
    """Return the version for the --version option."""
    if value:
        typer.echo(ai4_api_keys.extract_version())
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    )
):
    """Show version and exit."""
    pass
