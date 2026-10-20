from collections.abc import Callable
from typing import Literal, TypedDict

from src.acl_checker.domain.types import OriginalRule


class ExpectedApplicationFailure(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class DeviceAclPair(TypedDict):
    device: str
    acl: str


class InterfacePlacement(TypedDict):
    interface: str
    direction: Literal['in', 'out']


GlobalPlacement = TypedDict('GlobalPlacement', {'global': Literal[True]})
Placement = InterfacePlacement | GlobalPlacement


class Snapshot(DeviceAclPair):
    placements: list[Placement]
    rules: list[OriginalRule]


RelevanceSource = Callable[[str, str], list[DeviceAclPair]]
SnapshotSource = Callable[[str, str], Snapshot]


class ReportGroup(DeviceAclPair):
    placements: list[Placement]
    status: Literal['MATCHES', 'NO_MATCH']
    rules: list[OriginalRule]


ReportGroups = list[ReportGroup]
