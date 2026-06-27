#!/usr/bin/env python3
"""
export-data.py — seeds threat-model-data.json with THREATS and DTREE_DATA
extracted from the embedded JavaScript in llm-threat-model.html.

Run once (or whenever the HTML is edited directly) to sync the JSON file.
After seeding, edit threat-model-data.json and use build-html.py to regenerate.

Usage:
    python scripts/export-data.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_FILE = ROOT / "llm-threat-model.html"
JSON_FILE = ROOT / "threat-model-data.json"


def extract_js_array(html: str, var_name: str) -> list:
    pattern = rf'const {var_name} = (\[.+?\]);'
    m = re.search(pattern, html)
    if not m:
        print(f"ERROR: could not find 'const {var_name} = [...]' in HTML", file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))


def main():
    html = HTML_FILE.read_text(encoding="utf-8")

    threats = extract_js_array(html, "THREATS")
    dtree   = extract_js_array(html, "DTREE_DATA")

    print(f"Extracted {len(threats)} threats, {len(dtree)} decision-tree nodes.")

    data = json.loads(JSON_FILE.read_text(encoding="utf-8")) if JSON_FILE.exists() else {}
    data["threats"] = threats
    data["dtree"]   = dtree

    JSON_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written to {JSON_FILE}")


if __name__ == "__main__":
    main()
