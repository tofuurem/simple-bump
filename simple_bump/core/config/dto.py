from pydantic import BaseModel, Field


class RulesCommit(BaseModel):
    patch: list[str] = []
    minor: list[str] = []
    major: list[str] = []


class SBConfig(BaseModel):
    version: str | None
    commit_message: str = ''
    rules: RulesCommit = Field(default_factory=RulesCommit)
