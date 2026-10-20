from dataclasses import dataclass

from src.acl_checker.application.types import RelevanceSource, SnapshotSource
from src.acl_checker.domain.types import Flow


class ExpectedInputFailure(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class ValidatedInvocation:
    flow: Flow
    relevance: RelevanceSource
    snapshot: SnapshotSource
