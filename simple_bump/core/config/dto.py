import os
from functools import cached_property

from pydantic import BaseModel, Field

from simple_bump.core.config.enums import HVCS, VerVal


class BumpLevels(BaseModel):
    major: list[str] = Field(default=[])
    minor: list[str] = Field(default=['feat'])
    patch: list[str] = Field(default=['fix'])

    @cached_property
    def revert_levels(self) -> dict[str, VerVal]:
        data = {}
        for lvl in self.major:
            data[lvl] = VerVal.major
        for lvl in self.minor:
            data[lvl] = VerVal.minor
        for lvl in self.patch:
            data[lvl] = VerVal.patch
        return data


class GitConfig(BaseModel):
    branch: str = 'main'
    remote: str = 'origin'
    hvcs: HVCS = HVCS.gitlab
    env_token: str = 'GL_TOKEN'

    @cached_property
    def token(self) -> str | None:
        return os.getenv(self.env_token)


class SPConfig(BaseModel):
    version: str = '0.0.0'
    version_fmt: str = 'v{major}.{minor}.{patch}'
    commit_msg: str = 'Bump version {old} -> {new}'
    version_files: list[str] = Field(default_factory=list)
    bump_levels: BumpLevels = Field(default_factory=BumpLevels)
    git: GitConfig = Field(default_factory=GitConfig)

    @property
    def base(self) -> dict[str, str]:
        return {'version': self.version}
