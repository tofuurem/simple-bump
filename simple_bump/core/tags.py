from pathlib import Path

import toml
from typing import Literal

import click
import semver
from git import Repo
import sys

from simple_bump.core.config.dto import SBConfig


def update_version_in_toml(file_path, version_bump: Literal['patch', 'minor', 'major']):
    """
    Обновляет версию в pyproject.toml.

    :param file_path: Путь к файлу pyproject.toml.
    :param version_bump: Тип обновления ('major', 'minor', 'patch').
    """
    # Читаем содержимое TOML файла
    with open(file_path, 'r') as toml_file:
        data = toml.load(toml_file)
    if 'tool' not in data and 'sp' not in data['tool']:
        # todo: create base config
        raise
    # config = SBConfig(**data['tool']['sp'])
    config = data['tool']['sp']

    # Обновляем версию
    new_version = semver.VersionInfo.parse(config['version']).next_version(part=version_bump)
    click.echo(f'Bumped changes from {config['version']} -> {new_version} tag.')

    # Записываем обновленную версию обратно в TOML
    data['tool']['sp']['version'] = str(new_version)
    with open(file_path, 'w') as toml_file:
        toml.dump(data, toml_file)

    return str(new_version)


def commit_and_tag(repo_path: Path | str, new_version: str, files_path: list[Path | str]) -> None:
    """
    Делает коммит с обновленной версией и ставит на него тег.

    :param repo_path: Путь к репозиторию.
    :param new_version: Новая версия.
    :param files_path: Путь к файлам, которые были обновлены.
    """
    repo = Repo(repo_path)
    repo.index.add(files_path)
    repo.index.commit(f"Bump version to {new_version}")
    new_tag = f"v{new_version}"
    repo.create_tag(new_tag)
    click.echo(f"Committed and tagged with {new_tag}")


def push_changes(repo_path: Path | str) -> None:
    """
    Пушит все изменения в репозиторий, включая теги.
    """
    repo = Repo(repo_path)
    origin = repo.remote(name='origin')
    origin.push()
    origin.push(tags=True)
    click.echo("Changes and tags have been pushed to the remote repository.")
