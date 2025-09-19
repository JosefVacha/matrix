#!/usr/bin/env python3
"""
Validate model registry metadata against schema (basic, stdlib-only)
Usage:
  python scripts/qa/validate_model_metadata.py --file models/M3_DEMO/metadata.json --schema docs/schemas/model_metadata.schema.json
"""

import argparse
import json
import sys
import pathlib


def load_json(path):
    with open(path) as f:
        return json.load(f)


def validate(meta, schema):
    errors = []
    # Required keys
    for k in schema.get("required", []):
        if k not in meta:
            errors.append(f"Missing required key: {k}")
    # Type checks
    props = schema.get("properties", {})
    for k, v in props.items():
        if k in meta:
            typ = v.get("type")
            if typ:
                if isinstance(typ, list):
                    if not any(isinstance(meta[k], _type_py(t)) for t in typ):
                        errors.append(
                            f"Key {k} type mismatch: {type(meta[k])} not in {typ}"
                        )
                else:
                    if not isinstance(meta[k], _type_py(typ)):
                        errors.append(
                            f"Key {k} type mismatch: {type(meta[k])} != {typ}"
                        )
            # Enum check
            if "enum" in v:
                if meta[k] not in v["enum"]:
                    errors.append(f"Key {k} value {meta[k]} not in enum {v['enum']}")
    return errors


def _type_py(t):
    # Map JSON schema types to Python types
    return {
        "string": str,
        "integer": int,
        "array": list,
        "object": dict,
        "null": type(None),
    }.get(t, object)


def main():
    parser = argparse.ArgumentParser(
        description="Validate model registry metadata against schema"
    )
    parser.add_argument("--file", required=True)
    parser.add_argument("--schema", default="docs/schemas/model_metadata.schema.json")
    args = parser.parse_args()
    meta = load_json(args.file)
    schema = load_json(args.schema)
    errors = validate(meta, schema)
    if errors:
        print(json.dumps({"pass": False, "errors": errors}, indent=2))
        sys.exit(1)
    else:
        print(json.dumps({"pass": True}, indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
