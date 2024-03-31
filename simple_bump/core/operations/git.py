from pathlib import Path
from typing import NoReturn

import click
from git import RemoteProgress, Repo
from semver import Version

from simple_bump.core.config.dto import SPConfig
from simple_bump.core.types import VerVal


class GitOperations:
    def __init__(self, repo_path: Path | str, sp_config: SPConfig) -> None:
        self._repo = Repo(repo_path)
        self._sp = sp_config

    @property
    def determine_version_bump(self) -> VerVal | None:
        tags = sorted(self._repo.tags, key=lambda t: t.commit.committed_datetime)
        last_tag = tags[-1] if tags else None

        if last_tag:
            commits_since_last_tag = list(self._repo.iter_commits(rev=f'{last_tag}..HEAD'))
        else:
            commits_since_last_tag = list(self._repo.iter_commits())

        ver = None
        levels = self._sp.bump_levels.revert_levels
        for commit in commits_since_last_tag:
            message = commit.message.lower()
            # if no prefix -> it's bad commit message
            if ':' not in message:
                continue

            # breaking changes is always major
            if 'breaking' in message:
                return VerVal.major

            lv_prefix = levels.get(message.split(':')[0])
            if lv_prefix is not None:
                ver = lv_prefix
        return ver

    def push_changes(self) -> NoReturn:
        # only local work
        # todo: create git push by gitlab token
        progress = RemoteProgress()
        # todo: get remote repo from config ?
        origin = self._repo.remote(name='origin')
        origin.push(progress=progress)
        origin.push(progress=progress, tags=True)
        click.echo("Changes and tags have been pushed to the remote repository.")

    def commit_and_tag(self, old: str, new: Version, files_path: list[Path]) -> NoReturn:
        self._repo.index.add(files_path)
        # todo: get commit message from config
        self._repo.index.commit(self._sp.commit_msg.format(old=old, new=str(new)))
        click.echo("Committed files")

        new_tag = self._sp.version_fmt.format(major=new.major, minor=new.minor, patch=new.patch)
        self._repo.create_tag(new_tag)
        click.echo(f"Tagged -> {new_tag}")
