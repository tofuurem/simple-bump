from functools import cached_property
from pathlib import Path

import click
import semver
import tomlkit

from simple_bump.core.config.constants import DEFAULT_CONFIG_FILE
from simple_bump.core.config.dto import SPConfig
from simple_bump.core.config.enums import VerVal
from simple_bump.core.errors import NotFoundConfigError


class FilesOperation:
    def __init__(self, repo_path: Path, ) -> None:
        self._rp = repo_path
        self._data: tomlkit.TOMLDocument = self.read_project_config()
        self.sp_config = self.get_spconfig()

    @cached_property
    def project_toml(self) -> Path:
        return self._rp.joinpath(DEFAULT_CONFIG_FILE)

    def check_exists_file(self) -> None:
        if not self.project_toml.exists():
            raise FileNotFoundError

    def write_config(self, base: bool) -> None:
        if 'tool' not in self._data:
            self._data['tool'] = {'sp': {}}
        elif 'tool' in self._data and 'sp' not in self._data['tool']:
            self._data['tool']['sp'] = {}

        if base:
            self._data['tool']['sp'] = self.sp_config.base
        else:
            self._data['tool']['sp'] = self.sp_config.model_dump()

        self.write_project_config()

    def get_spconfig(self, raised: bool = False) -> SPConfig:
        try:
            sp_config = SPConfig(**self._data['tool']['sp'])
        except KeyError:
            if raised:
                raise NotFoundConfigError
            sp_config = SPConfig()
        return sp_config

    def read_project_config(self) -> tomlkit.TOMLDocument:
        self.check_exists_file()
        with open(self.project_toml, 'r', encoding='utf-8') as f:
            return tomlkit.parse(f.read())

    def write_project_config(self) -> None:
        with open(self.project_toml, 'w', encoding='utf-8') as toml_file:
            toml_file.write(tomlkit.dumps(self._data))

    def update_version_in_files(self, version_bump: VerVal) -> tuple[str, semver.Version]:
        try:
            new_version = semver.VersionInfo.parse(self.sp_config.version).next_version(part=version_bump)
        except Exception as ex:
            click.echo(f'No version in config, or bad style: {ex}', err=True)
            raise ex
        click.echo(f"Bumped changes from {self.sp_config.version} -> {str(new_version)} tag.")
        # todo: update other versions in files
        if 'project' in self._data and 'version' in self._data['project']:
            self._data['project']['version'] = str(new_version)

        self._data['tool']['sp']['version'] = str(new_version)
        self.write_project_config()
        return self.sp_config.version, new_version
