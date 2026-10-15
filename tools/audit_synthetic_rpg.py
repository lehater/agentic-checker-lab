#!/usr/bin/env python3
"""Read-only, independent structural audit of an exported synthetic forward RPG.

This is deliberately *not* a semantic coverage checker. Human review is required.
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def analyze(folder: Path) -> dict:
    names = ("feature_spec", "feature_build", "feature_tree", "skeleton", "rpg")
    sources = {}
    for name in names:
        file = folder / f"{name}.json"
        if not file.is_file():
            raise ValueError(f"Missing artifact: {file}")
        with file.open("r", encoding="utf-8") as stream:
            sources[name] = json.load(stream)
        if not isinstance(sources[name], dict):
            raise ValueError(f"{file}: expected a top-level JSON object")

    data = sources["rpg"]
    root = data.get("root")
    if not isinstance(root, dict):
        raise ValueError("rpg.json: expected CoderMind nested 'root' node")
    edges = data.get("edges", [])
    if not isinstance(edges, list):
        raise ValueError("rpg.json: expected 'edges' list")

    errors = []
    inventory = []
    ids = Counter()

    def walk(node: dict, parents: tuple[str, ...] = ()) -> None:
        if not isinstance(node, dict):
            errors.append("Non-object child node")
            return
        ident, name = node.get("id"), node.get("name")
        if not isinstance(ident, str) or not ident:
            errors.append(f"Missing/invalid node id: {node!r}"[:200])
        else:
            ids[ident] += 1
        if not isinstance(name, str) or not name:
            errors.append(f"Missing/invalid node name: {ident!r}")
            name = "?"
        inventory.append({
            "id": ident,
            "name": name,
            "type": node.get("node_type"),
            "path": "/".join((*parents, name)),
        })
        children = node.get("children", [])
        if not isinstance(children, list):
            errors.append(f"Node {ident!r} has non-list children")
            return
        for child in children:
            walk(child, (*parents, name))

    walk(root)
    repeated = [name for name, count in ids.items() if count > 1]
    if repeated:
        errors.append(f"Duplicate IDs: {repeated[:15]!r}")

    missing_endpoints = []
    for idx, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"Non-object edge at index {idx}")
            continue
        src, dst = edge.get("src"), edge.get("dst")
        if src not in ids or dst not in ids:
            missing_endpoints.append({"index": idx, "src": src, "dst": dst})
    if missing_endpoints:
        errors.append(f"{len(missing_endpoints)} edges with unknown endpoints")

    types = Counter(str(item["type"]) for item in inventory)
    return {
        "status": "STRUCTURE_PASS_SEMANTICS_UNREVIEWED" if not errors else "STRUCTURE_FAIL",
        "repo_name": data.get("repo_name"),
        "node_count": len(inventory),
        "edge_count": len(edges),
        "node_types": dict(sorted(types.items())),
        "errors": errors,
        "invalid_edges_sample": missing_endpoints[:10],
        "semantic_review": {
            "status": "NOT_DONE",
            "required_ids": [f"R-SYN-{x:02}" for x in range(1, 7)],
            "note": "Inspect artifact content against the source requirements; names alone cannot prove coverage",
        },
        "node_inventory": inventory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Path to exported synthetic RPG artifacts")
    args = parser.parse_args()
    try:
        result = analyze(args.folder)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"RPG audit failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
