from pathlib import Path

from git import Repo


def determine_version_bump(repo_path: Path) -> str | None:
    """
    Определяет тип версии для обновления, основываясь на сообщениях коммитов с последнего тега.

    :param repo_path: Путь к локальному Git репозиторию.
    :return: Строка, указывающая на тип обновления версии ('major', 'minor', 'patch'), или None, если обновление не требуется.
    """
    repo = Repo(repo_path)
    # Получаем список тегов, отсортированных по дате создания
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    last_tag = tags[-1] if tags else None

    # Устанавливаем точку отсчета для поиска коммитов
    if last_tag:
        commits_since_last_tag = list(repo.iter_commits(rev=f'{last_tag}..HEAD'))
    else:
        # Если тегов нет, проверяем всю историю
        commits_since_last_tag = list(repo.iter_commits())

    # Флаги для определения типа обновления версии
    major, minor, patch = False, False, False

    for commit in commits_since_last_tag:
        message = commit.message.lower()
        if 'break' in message or 'major:' in message:
            major = True
            break  # Мажорное обновление имеет наивысший приоритет
        elif 'feat:' in message:
            minor = True
        elif 'fix:' in message:
            patch = True

    if major:
        return 'major'
    elif minor:
        return 'minor'
    elif patch:
        return 'patch'
    else:
        return None


# Пример использования (раскомментируйте для запуска)
if __name__ == '__main__':
    print(determine_version_bump('/Users/rabbit/Desktop/trip_crm/tfs_backend'))
