import click

from simple_bump.core.handler import Handler


@click.command()
@click.option('--tags', is_flag=True, help='Push tags along with changes.')
def push(tags: bool) -> None:
    """Pushes changes to the repository."""
    handler = Handler()
    handler.push(tags)
