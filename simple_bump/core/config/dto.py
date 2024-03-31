from functools import cached_property

from pydantic import BaseModel, Field

from simple_bump.core.types import VerVal


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


class SPConfig(BaseModel):
    version: str = '0.0.0'
    version_fmt: str = 'v{major}.{minor}.{patch}'
    commit_msg: str = 'Bump version {old} -> {new}'
    version_files: list[str] = Field(default_factory=list)
    bump_levels: BumpLevels = Field(default_factory=BumpLevels)

    @property
    def base(self) -> dict[str, str]:
        return {'version': self.version}
