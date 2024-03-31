import click

from simple_bump.core.handler import Handler


@click.command()
def push() -> None:
    """Pushes changes to the repository."""
    Handler().push()
