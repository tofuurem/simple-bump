import os
import sys
from pathlib import Path

import click

from simple_bump.core.parser import determine_version_bump
from simple_bump.core.tags import update_version_in_toml, commit_and_tag, push_changes


# Defining the main entry point for the CLI application
@click.group()
def cli():
    """Simple Program (sp) CLI tool."""
    pass


# Defining the bump command with optional flags for version increments
@cli.command()
@click.option('--major', is_flag=True, help='Increments the major version.')
@click.option('--minor', is_flag=True, help='Increments the minor version.')
@click.option('--patch', is_flag=True, help='Increments the patch version.')
def bump(major: bool, minor: bool, patch: bool) -> None:
    """Bumps the project version."""
    rel_path = Path(os.path.dirname(os.path.abspath(sys.argv[1])))
    if major:
        click.echo("Major version bumped.")
        new_version = 'patch'
    elif minor:
        click.echo("Minor version bumped.")
        new_version = 'minor'
    elif patch:
        click.echo("Patch version bumped.")
        new_version = 'patch'
    else:
        new_version = determine_version_bump(rel_path)
        click.echo(f"New version bumped: {new_version}")
    res = update_version_in_toml(rel_path.joinpath('pyproject.toml'), new_version)
    commit_and_tag(rel_path, res, [rel_path.joinpath('pyproject.toml')])
    push_changes(rel_path)


# Defining the push command with optional flags
@cli.command()
@click.option('--tags', is_flag=True, help='Push tags along with changes.')
def push(tags):
    """Pushes changes to the repository."""
    if tags:
        click.echo("Changes and tags pushed.")
    else:
        click.echo("Changes pushed.")


# Defining a command group for config commands
@cli.group()
def config():
    """Configuration commands."""
    pass


# Defining the init subcommand under config
@config.command()
def init():
    """Initializes a new configuration."""
    click.echo("Configuration initialized.")


# Defining the check subcommand under config
@config.command()
def check():
    """Checks the current configuration."""
    click.echo("Configuration checked.")


# if __name__ == '__main__':
#     cli()

# sb bump  -> set new version in files and commit and after tag
# sb bump --minor
# sb bump --major
# sb bump --patch


# вывод хелпы
# sb --help

# sb push -> push to repo result by token to github and gitlab
