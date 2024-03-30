from pathlib import Path
from typing import NoReturn

import click
from git import Repo

from simple_bump.core.types import VerVal


class GitOperations:
    def __init__(self, repo_path: Path | str) -> None:
        self._repo = Repo(repo_path)

    @property
    def determine_version_bump(self) -> VerVal | None:
        """
        Определяет тип версии для обновления, основываясь на сообщениях коммитов с последнего тега.
        :return: Строка, указывающая на тип обновления версии ('major', 'minor', 'patch')
        """
        tags = sorted(self._repo.tags, key=lambda t: t.commit.committed_datetime)
        last_tag = tags[-1] if tags else None

        if last_tag:
            commits_since_last_tag = list(self._repo.iter_commits(rev=f'{last_tag}..HEAD'))
        else:
            commits_since_last_tag = list(self._repo.iter_commits())

        ver = None

        for commit in commits_since_last_tag:
            message = commit.message.lower()
            if 'break' in message or 'major:' in message:
                return VerVal.major
            elif 'feat:' in message:
                ver = VerVal.minor
            elif 'fix:' in message:
                ver = VerVal.patch
        return ver

    def push_changes(self) -> NoReturn:
        # todo: get remote repo from config ?
        origin = self._repo.remote(name='origin')
        # todo: added progress bar
        origin.push()
        origin.push(tags=True)
        click.echo("Changes and tags have been pushed to the remote repository.")

    def commit_and_tag(self, old: str, new: str, files_path: list[Path]) -> NoReturn:
        self._commit(files_path, old, new)
        self._tag(new)

    def _commit(self, files_path: list[Path], old: str, new: str) -> NoReturn:
        self._repo.index.add(files_path)
        # todo: get commit message from config
        self._repo.index.commit('Bump version {old} -> {new}'.format(old=old, new=new))
        # todo: get tag type from config
        click.echo("Committed files")

    def _tag(self, new: str) -> NoReturn:
        new_tag = f"v{new}"
        self._repo.create_tag(new_tag)
        click.echo(f"Tagged -> {new_tag}")
