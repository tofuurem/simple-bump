import os
import sys
from pathlib import Path

import click

from simple_bump.cli.dto import BumpParams
from simple_bump.core.operations import FilesOperation, GitOperations


class Handler:
    def __init__(self) -> None:
        rel_path = Path(os.path.dirname(os.path.abspath(sys.argv[1])))

        self._fio = FilesOperation(rel_path)
        self._gio = GitOperations(rel_path, self._fio.sp_config)

    def bump(self, bp: BumpParams) -> None:
        new_version = bp.next_version or self._gio.determine_version_bump
        if new_version is None:
            click.echo('No changes to bump')
            return

        old, new = self._fio.update_version_in_files(new_version)
        self._gio.commit_and_tag(old, new, [self._fio.project_toml])
        if bp.push:
            self._gio.push_changes()

    def push(self) -> None:
        self._gio.push_changes()

    def init_config(self, base: bool) -> None:
        self._fio.write_config(base)
