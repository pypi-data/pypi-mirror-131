from typing import List, Optional

from pydantic import BaseModel


class Commit(BaseModel):
    sha: str

    url: str


class StatusChecks(BaseModel):
    enforcement_level: str

    contexts: List[str]


class BranchProtection(BaseModel):
    required_status_checks: StatusChecks


class Branch(BaseModel):
    name: str

    commit: Commit

    protected: bool

    protection: Optional[BranchProtection]

    protection_url: Optional[str]
