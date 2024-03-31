from enum import StrEnum


class VerVal(StrEnum):
    patch = 'patch'
    minor = 'minor'
    major = 'major'


class HVCS(StrEnum):
    gitlab = 'gitlab'
