import os
import sys
from pathlib import Path

import click

from simple_bump.core.files_operation import FilesOperation
from simple_bump.core.git_operation import GitOperations
from simple_bump.core.main import Core
from simple_bump.core.types import VerVal


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
    core = Core()
    if major:
        click.echo("Major version bumped.")
        new_version = VerVal.major
    elif minor:
        click.echo("Minor version bumped.")
        new_version = VerVal.minor
    elif patch:
        click.echo("Patch version bumped.")
        new_version = VerVal.patch
    else:
        new_version = core.go.determine_version_bump
    if new_version is None:
        click.echo('No changes to bump')
        return
    old, new = core.fo.update_version_in_files(new_version)
    core.go.commit_and_tag(old, new, [core.fo.project_toml])
    if push:
        core.go.push_changes()
