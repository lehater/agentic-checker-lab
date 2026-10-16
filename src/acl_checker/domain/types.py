from typing import Literal, TypedDict


class Flow(TypedDict):
    source: str
    destination: str
    protocol: Literal['tcp', 'udp']
    source_port: int
    destination_port: int


class OriginalRule(TypedDict):
    id: str
    source: str
    destination: str
    protocol: Literal['tcp', 'udp', 'any']
    source_ports: list[int]
    destination_ports: list[int]
    action: Literal['permit', 'deny']
