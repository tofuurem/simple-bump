import click

from simple_bump.cli.dto import BumpParams
from simple_bump.core.handler import Handler


@click.command()
@click.option('--major', is_flag=True, help='Increments the major version.')
@click.option('--minor', is_flag=True, help='Increments the minor version.')
@click.option('--patch', is_flag=True, help='Increments the patch version.')
@click.option('--push', is_flag=True, help='Push changes.')
def bump(
    major: bool,
    minor: bool,
    patch: bool,
    push: bool
) -> None:
    """Bumps the project version."""
    handler = Handler()
    handler.bump(BumpParams(major, minor, patch, push))
