from pathlib import Path
from typing import NoReturn

import click
from git import GitCommandError, Repo
from semver import Version

from simple_bump.core.config.dto import SPConfig
from simple_bump.core.config.enums import HVCS, VerVal
from simple_bump.core.errors import NotFoundTokenError
from simple_bump.core.operations.progress_bar import GitRemoteProgress


class GitOperations:
    def __init__(self, repo_path: Path | str, sp_config: SPConfig) -> None:
        self._repo = Repo(repo_path)
        self._sp = sp_config

        self._progress = GitRemoteProgress()

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
        if not self.simple_push():
            self.push_by_token()
        click.echo("Changes and tags have been pushed to the remote repository.")

    def push_by_token(self) -> bool:
        repo = self._repo.remote(name=self._sp.git.remote)
        if not self._sp.git.token:
            raise NotFoundTokenError
        match self._sp.git.hvcs:
            case HVCS.gitlab:
                new_url = repo.url.replace('https://', f'https://oauth:{self._sp.git.token}@')
                repo.set_url(new_url)
        try:
            repo.push(progress=self._progress)
            repo.push(progress=self._progress, tags=True)
        except GitCommandError as gce:
            click.echo(gce, err=True)
            return False
        return True

    def simple_push(self) -> bool:
        try:
            repo = self._repo.remote(name=self._sp.git.remote)
            repo.push(progress=self._progress)
            repo.push(progress=self._progress, tags=True)
        except GitCommandError:
            return False
        return True

    def commit_and_tag(self, old: str, new: Version, files_path: list[Path]) -> NoReturn:
        self._repo.index.add(files_path)
        # todo: get commit message from config
        self._repo.index.commit(self._sp.commit_msg.format(old=old, new=str(new)))
        click.echo("Committed files")

        new_tag = self._sp.version_fmt.format(major=new.major, minor=new.minor, patch=new.patch)
        self._repo.create_tag(new_tag)
        click.echo(f"Tagged -> {new_tag}")
