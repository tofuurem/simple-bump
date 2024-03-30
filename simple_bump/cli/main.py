import click

from simple_bump.cli.commands.bump import bump
from simple_bump.cli.commands.config import config
from simple_bump.cli.commands.push import push


@click.group()
def cli():
    """Simple Program (sp) CLI tool."""
    pass


cli.add_command(bump)
cli.add_command(push)
cli.add_command(config)
