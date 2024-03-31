from dataclasses import dataclass

from simple_bump.core.config.enums import VerVal


@dataclass
class BumpParams:
    major: bool = False
    minor: bool = False
    patch: bool = False
    push: bool = False

    @property
    def next_version(self) -> VerVal | None:
        if self.major:
            return VerVal.major
        if self.minor:
            return VerVal.minor
        if self.patch:
            return VerVal.patch
        return None
