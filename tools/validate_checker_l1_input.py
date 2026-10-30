#!/usr/bin/env python3
"""Public, standard-library-only checker of the PROPOSED synthetic L1 input contract.

This checks data shape and evidence integrity, NOT ACL matching, relevance
selection, collector behavior, implementation quality, or an independent oracle.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv4Network
import json
import math
import re
from pathlib import Path
import sys


def fail(where: str, message: str) -> None:
    raise ValueError(f"{where}: {message}")


def keys(obj: object, where: str, required: set[str], optional: set[str] = frozenset()) -> dict:
    if not isinstance(obj, dict):
        fail(where, "object required")
    missing = required - obj.keys()
    unknown = obj.keys() - required - optional
    if missing:
        fail(where, "missing " + ", ".join(sorted(missing)))
    if unknown:
        fail(where, "unexpected " + ", ".join(sorted(unknown)))
    return obj


def ident(v: object, where: str) -> str:
    if not isinstance(v, str) or not v.strip():
        fail(where, "non-empty string required")
    return v


def port(v: object, where: str, *, query: bool) -> None:
    if v == "any":
        return
    if type(v) is int and 0 <= v <= 65535:
        return
    if not query:
        if isinstance(v, dict):
            x = keys(v, where, {"min", "max"})
            lo, hi = x["min"], x["max"]
            if type(lo) is int and type(hi) is int and 0 <= lo <= hi <= 65535:
                return
    fail(where, "port must be 0..65535, 'any', or a valid inclusive range (rule only)")


def ip(v: object, where: str, *, predicate: bool) -> None:
    if not isinstance(v, str):
        fail(where, "IPv4 string required")
    try:
        if predicate and "/" in v:
            IPv4Network(v, strict=True)
        else:
            IPv4Address(v)
    except ValueError as e:
        fail(where, "invalid or noncanonical IPv4 address/predicate: " + str(e))


def timestamp(v: object, where: str) -> None:
    if not isinstance(v, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)", v) is None:
        fail(where, "RFC3339 UTC timestamp with seconds and Z suffix required")
    try:
        t = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if t.utcoffset() != timedelta(0):
            fail(where, "timestamp must be UTC")
    except ValueError:
        fail(where, "invalid RFC3339 date-time")


def placement(v: object, where: str) -> None:
    if not isinstance(v, dict):
        fail(where, "object required")
    kind = v.get("kind")
    if kind == "global":
        keys(v, where, {"kind"})
    elif kind == "interface":
        x = keys(v, where, {"kind", "name", "direction"})
        ident(x["name"], where + ".name")
        if x["direction"] not in ("ingress", "egress"):
            fail(where, "direction must be ingress/egress")
    else:
        fail(where, "kind must be global/interface")


def rule(v: object, where: str) -> None:
    required = {"action", "src_ip", "dst_ip", "protocol", "src_port", "dst_port"}
    x = keys(v, where, required, {"extra"})
    if x["action"] not in ("permit", "deny"):
        fail(where, "action must be permit/deny")
    if x["protocol"] not in ("tcp", "udp", "any"):
        fail(where, "rule protocol must be tcp/udp/any")
    for k in ("src_ip", "dst_ip"):
        ip(x[k], where + "." + k, predicate=True)
    for k in ("src_port", "dst_port"):
        port(x[k], where + "." + k, query=False)
    if "extra" in x and not isinstance(x["extra"], dict):
        fail(where + ".extra", "object required")


def validate_payload(v: object) -> None:
    root = keys(v, "$", {"schema_version", "flow", "firewalls", "snapshots"})
    if type(root["schema_version"]) is not int or root["schema_version"] != 1:
        fail("$.schema_version", "expected integer 1")
    f = keys(root["flow"], "$.flow", {"src_ip", "dst_ip", "protocol"},
             {"src_port", "dst_port"})
    for k in ("src_ip", "dst_ip"):
        ip(f[k], "$.flow." + k, predicate=False)
    if f["protocol"] not in ("tcp", "udp"):
        fail("$.flow.protocol", "protocol must be tcp/udp")
    for k in ("src_port", "dst_port"):
        if k in f:
            port(f[k], "$.flow." + k, query=True)
        # Missing query port means "any"; both formats are valid, not missing evidence.

    if not isinstance(root["firewalls"], list) or not isinstance(root["snapshots"], list):
        fail("$", "firewalls and snapshots must be arrays")
    fw_ids: set[str] = set()
    expected_snapshots: set[tuple[str, str]] = set()
    for i, fw in enumerate(root["firewalls"]):
        where = f"$.firewalls[{i}]"
        x = keys(fw, where, {"id", "acls"})
        fid = ident(x["id"], where + ".id")
        if fid in fw_ids:
            fail(where, "duplicate firewall id")
        fw_ids.add(fid)
        if not isinstance(x["acls"], list):
            fail(where + ".acls", "array required")
        for j, acl in enumerate(x["acls"]):
            aw = f"{where}.acls[{j}]"
            a = keys(acl, aw, {"id", "placements"})
            aid = ident(a["id"], aw + ".id")
            expected_snapshots.add((fid, aid))
            if not isinstance(a["placements"], list):
                fail(aw + ".placements", "array required")
            for k, p in enumerate(a["placements"]):
                placement(p, f"{aw}.placements[{k}]")
            # Multiple ACL references under one FW are intentionally allowed;
            # the future Checker must consolidate groups and distinct placements.

    seen: set[tuple[str, str]] = set()
    for i, snap in enumerate(root["snapshots"]):
        sw = f"$.snapshots[{i}]"
        s = keys(snap, sw, {"device_id", "acl_id", "last_success_at", "rules"})
        sid = (ident(s["device_id"], sw + ".device_id"),
               ident(s["acl_id"], sw + ".acl_id"))
        if sid in seen:
            fail(sw, "duplicate snapshot identity")
        seen.add(sid)
        if sid not in expected_snapshots:
            fail(sw, "snapshot for non-relevant device/ACL")
        timestamp(s["last_success_at"], sw + ".last_success_at")
        if not isinstance(s["rules"], list):
            fail(sw + ".rules", "array required")
        for j, item in enumerate(s["rules"]):
            rule(item, f"{sw}.rules[{j}]")
    if expected_snapshots != seen:
        fail("$.snapshots", "missing snapshot for " + ", ".join(
            sorted(f"{a}/{b}" for a, b in expected_snapshots - seen)))


def _unique_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for name, val in pairs:
        if name in result:
            raise ValueError("duplicate JSON object key: " + name)
        result[name] = val
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="local proposed synthetic input JSON")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"),
                          object_pairs_hook=_unique_keys)
        validate_payload(data)
    except (ValueError, OSError, UnicodeError) as e:
        print("INVALID proposed L1 input:", e, file=sys.stderr)
        return 1
    print("VALID proposed L1 input (shape/evidence only; not an oracle)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
