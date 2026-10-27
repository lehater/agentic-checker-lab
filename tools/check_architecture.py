#!/usr/bin/env python3
"""Validate declared architectural invariants for RPG skeletons and Python source.

Generic engine: project names, layer mappings, dependency directions and symbol
ownership come from an explicit JSON architecture contract, not hardcoded code.
Semantic SOLID/KISS/YAGNI assessment is not attempted by this tool.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path, PurePosixPath
import sys


class ContractError(ValueError):
    """The declared architecture contract cannot be interpreted safely."""


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != "architecture-contract/v1":
        raise ContractError("unsupported architecture contract schema")
    package_path = data.get("package_path")
    package_prefix = data.get("module_prefix")
    layers = data.get("layers")
    allowed = data.get("allowed_dependencies")
    owners = data.get("symbol_owners", {})
    feature_owners = data.get("feature_owners", {})
    nested = data.get("disallow_nested_layer_roots", True)
    if (not isinstance(package_path, str) or not package_path or
            not isinstance(package_prefix, str) or not package_prefix or
            not isinstance(layers, dict) or not layers or
            not isinstance(allowed, dict) or not isinstance(owners, dict) or
            not isinstance(feature_owners, dict) or
            not isinstance(nested, bool)):
        raise ContractError("missing or invalid package_path/module_prefix/layers/allowed_dependencies/symbol_owners")
    pp = PurePosixPath(package_path)
    if pp.is_absolute() or ".." in pp.parts or "." == package_path:
        raise ContractError("package_path must be a relative directory")
    if not all(part.isidentifier() for part in package_prefix.split(".")):
        raise ContractError("module_prefix must be a dotted Python package")
    root_to_layer = {}
    for layer, roots in layers.items():
        if not isinstance(layer, str) or not layer or not isinstance(roots, list) or not roots:
            raise ContractError("layers must map layer IDs to nonempty lists of directory names")
        for root in roots:
            if not isinstance(root, str) or not root.isidentifier() or root in root_to_layer:
                raise ContractError("each layer root must be a unique single directory name")
            root_to_layer[root] = layer
    if set(allowed) != set(layers):
        raise ContractError("allowed_dependencies must cover exactly the declared layers")
    for layer, targets in allowed.items():
        if not isinstance(targets, list) or any(t not in layers for t in targets):
            raise ContractError(f"unknown allowed dependency for {layer}")
    for symbol, layer in owners.items():
        if not isinstance(symbol, str) or not symbol.isidentifier() or layer not in layers:
            raise ContractError("symbol_owners must map Python names to declared layers")
    for feature, layer in feature_owners.items():
        if not isinstance(feature, str) or not feature.strip() or layer not in layers:
            raise ContractError("feature_owners must map exact feature IDs to declared layers")
    data["_root_to_layer"] = root_to_layer
    return data


def _parts_below_package(path: str, contract: dict) -> tuple[str, ...]:
    path_parts = PurePosixPath(path.replace("\\", "/")).parts
    package_parts = PurePosixPath(contract["package_path"]).parts
    for start in range(len(path_parts) - len(package_parts) + 1):
        if path_parts[start:start + len(package_parts)] == package_parts:
            return tuple(path_parts[start + len(package_parts):])
    return ()


def _layer_for_parts(parts: tuple[str, ...], contract: dict) -> str | None:
    return contract["_root_to_layer"].get(parts[0]) if parts else None


def _validate_layout(parts: tuple[str, ...], path: str, contract: dict) -> list[str]:
    layer = _layer_for_parts(parts, contract)
    if layer is None:
        return []
    errs = []
    if contract["disallow_nested_layer_roots"]:
        for root in parts[1:-1]:
            if root in contract["_root_to_layer"]:
                errs.append(f"{path}: nested layer root {root!r} inside layer {layer!r}")
    return errs


def _skeleton_files(node: object):
    if isinstance(node, list):
        for child in node:
            yield from _skeleton_files(child)
    elif isinstance(node, dict):
        if node.get("type") == "file" and isinstance(node.get("path"), str):
            yield node["path"], node.get("feature_paths", [])
        for val in node.values():
            if isinstance(val, (dict, list)):
                yield from _skeleton_files(val)


def check_skeleton(path: Path, contract: dict) -> tuple[list[str], int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    files = list(_skeleton_files(data.get("root", data)))
    errors = []
    matched = 0
    for path_str, feature_paths in files:
        parts = _parts_below_package(path_str, contract)
        if parts:
            matched += 1
            errors.extend(_validate_layout(parts, path_str, contract))
            if not isinstance(feature_paths, list):
                errors.append(f"{path_str}: invalid feature_paths list")
                continue
            layer = _layer_for_parts(parts, contract)
            for feature in feature_paths:
                expected = contract["feature_owners"].get(feature) if isinstance(feature, str) else None
                if expected and layer != expected:
                    errors.append(f"{path_str}: feature {feature!r} belongs in {expected}, found {layer or 'unclassified'}")
    if not matched:
        errors.append(f"{path}: no files matching declared package_path {contract['package_path']}")
    return sorted(set(errors)), matched


def _module_name(rel: Path, prefix: str) -> str:
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join([prefix, *parts])


def _import_names(tree: ast.AST, module: str, is_init: bool):
    current_package = module if is_init else module.rsplit(".", 1)[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                yield item.name
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = current_package.split(".")
                keep = len(parts) - node.level + 1
                prefix = ".".join(parts[:max(0, keep)])
                name = ".".join(x for x in (prefix, node.module or "") if x)
            else:
                name = node.module or ""
            yield name
            for alias in node.names:
                if alias.name != "*":
                    yield ".".join(x for x in (name, alias.name) if x)


def _layer_for_import(module: str, contract: dict) -> str | None:
    prefix = contract["module_prefix"]
    if not module.startswith(prefix + "."):
        return None
    relative = module[len(prefix) + 1:].split(".")
    return contract["_root_to_layer"].get(relative[0])


def check_source(root: Path, contract: dict) -> tuple[list[str], int]:
    if not root.is_dir():
        return [f"{root}: source root does not exist"], 0
    prefix = contract["module_prefix"]
    modules = {}
    errors = []
    for file in sorted(root.rglob("*.py")):
        rel = file.relative_to(root)
        path_parts = rel.parts
        layer = _layer_for_parts(path_parts, contract)
        errors.extend(_validate_layout(path_parts, str(file), contract))
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"{file}: syntax/read error: {exc}")
            continue
        name = _module_name(rel, prefix)
        modules[name] = (file, tree)
        if layer:
            for definition in tree.body:
                if isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    target_layer = contract["symbol_owners"].get(definition.name)
                    if target_layer and target_layer != layer:
                        errors.append(f"{file}: {definition.name} belongs in {target_layer}, found {layer}")
    edges = {name: set() for name in modules}
    for name, (file, tree) in modules.items():
        origin = _layer_for_import(name, contract)
        for target in set(_import_names(tree, name, file.name == "__init__.py")):
            dest = _layer_for_import(target, contract)
            if origin and dest and dest not in contract["allowed_dependencies"][origin]:
                errors.append(f"{file}: forbidden {origin} -> {dest} import: {target}")
            if target in modules:
                edges[name].add(target)
    visited = set()
    active = set()

    def walk(name: str, path: list[str]) -> None:
        if name in active:
            cycle = path[path.index(name):]
            errors.append("module import cycle: " + " -> ".join(cycle))
            return
        if name in visited:
            return
        active.add(name)
        for dest in sorted(edges[name]):
            walk(dest, [*path, dest])
        active.remove(name)
        visited.add(name)

    for name in sorted(edges):
        if name not in visited:
            walk(name, [name])
    if not modules:
        errors.append(f"{root}: no Python files")
    return sorted(set(errors)), len(modules)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--contract", type=Path, default=Path("docs/engineering/architecture-contract.json"),
                   help="JSON architecture contract, default docs/engineering/architecture-contract.json")
    p.add_argument("--skeleton", type=Path, help="RPG skeleton.json, pre-codegen")
    p.add_argument("--source-root", type=Path, help="Python package source root, post-codegen")
    p.add_argument("--json", action="store_true", help="Machine-readable verdict")
    args = p.parse_args()
    if not (args.skeleton or args.source_root):
        p.error("provide --skeleton and/or --source-root")
    counts = {}
    errors = []
    try:
        contract = load_contract(args.contract)
        if args.skeleton:
            result, counts["skeleton_files"] = check_skeleton(args.skeleton, contract)
            errors.extend(result)
        if args.source_root:
            result, counts["source_modules"] = check_source(args.source_root, contract)
            errors.extend(result)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        errors.append(f"invalid contract/input: {exc}")
    report = {"status": "FAIL" if errors else "PASS", "checked": counts,
              "violations": sorted(set(errors))}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Architecture {report['status']}: {counts}")
        for error in report["violations"]:
            print(f" - {error}")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
