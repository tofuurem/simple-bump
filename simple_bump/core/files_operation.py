import sys
from functools import cached_property
from pathlib import Path

import semver
import tomlkit
import click

from simple_bump.core.types import VerVal


class FilesOperation:
    def __init__(self, repo_path: Path) -> None:
        self._rp: Path = repo_path

    @cached_property
    def project_toml(self) -> Path:
        return self._rp.joinpath('pyproject.toml')

    def update_version_in_files(self, version_bump: VerVal) -> tuple[str, str]:
        # todo: add changed files from configuration
        with open(self.project_toml, 'r', encoding='utf-8') as f:
            data = tomlkit.parse(f.read())

        tool = data.get('tool')

        if tool is None or tool.get('sp') is None:
            click.echo(f'Config file is empty: {self.project_toml}', err=True)

        try:
            old = tool['sp']['version']
            new_version = str(semver.VersionInfo.parse(old).next_version(part=version_bump))
        except Exception as ex:
            click.echo(f'No version in config, or bad style: {ex}', err=True)
            sys.exit(1)
        click.echo(f"Bumped changes from {tool['sp']['version']} -> {new_version} tag.")

        data['tool']['sp']['version'] = new_version
        with open(self.project_toml, 'w', encoding='utf-8') as toml_file:
            toml_file.write(tomlkit.dumps(data))
        return old, new_version
