from typing import Final

from simple_bump.core.types import VerVal

DEFAULT_BUMP_LEVELS: Final[dict[str, list[str]]] = {
    VerVal.major: [],
    VerVal.minor: ['feat'],
    VerVal.patch: ['fix'],
}

DEFAULT_CONFIG_FILE: Final[str] = 'pyproject.toml'
