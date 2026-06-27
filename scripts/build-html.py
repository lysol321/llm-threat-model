#!/usr/bin/env python3
"""
build-html.py — regenerates the DATA_START..DATA_END block in llm-threat-model.html
from threat-model-data.json.

Edit threat-model-data.json, then run this script to update the HTML.

Usage:
    python scripts/build-html.py [--dry-run]

Workflow:
    1. python scripts/export-data.py   # seed JSON from current HTML (first time only)
    2. edit threat-model-data.json
    3. python scripts/build-html.py    # regenerate HTML
"""
import json
import re
import sys
from pathlib import Path

ROOT      = Path(__file__).parent.parent
HTML_FILE = ROOT / "llm-threat-model.html"
JSON_FILE = ROOT / "threat-model-data.json"

START_SENTINEL = "// ── DATA_START (managed by scripts/build-html.py) ──"
END_SENTINEL   = "// ── DATA_END ──"


def js(value) -> str:
    """Compact JSON serialisation for embedding in JS."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def build_data_block(data: dict) -> str:
    lines = [START_SENTINEL]

    if data.get("threats"):
        lines.append(f"const THREATS = {js(data['threats'])};")
    if data.get("dtree"):
        lines.append(f"const DTREE_DATA = {js(data['dtree'])};")

    # Assemble SIDEBAR_DATA from JSON sections
    sidebar_obj = {
        "citations":  data.get("sidebar", {}).get("citations",  []),
        "frameworks": data.get("sidebar", {}).get("frameworks", []),
        "regulatory": data.get("sidebar", {}).get("regulatory", []),
        "synthesis":  data.get("synthesis",  []),
        "concepts":   data.get("concepts",   []),
        "sources":    data.get("sources",    []),
        "evaluation": data.get("evaluation", []),
        "analysis":   data.get("analysis",   []),
    }
    lines.append(f"const SIDEBAR_DATA = {js(sidebar_obj)};")
    lines.append(END_SENTINEL)
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv

    if not JSON_FILE.exists():
        print(f"ERROR: {JSON_FILE} not found. Run export-data.py first.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    html = HTML_FILE.read_text(encoding="utf-8")

    pattern = re.compile(
        r'(' + re.escape(START_SENTINEL) + r').*?(' + re.escape(END_SENTINEL) + r')',
        re.DOTALL
    )

    if not pattern.search(html):
        print(f"ERROR: sentinels not found in {HTML_FILE}", file=sys.stderr)
        print(f"  Expected: {START_SENTINEL!r}", file=sys.stderr)
        sys.exit(1)

    new_block  = build_data_block(data)
    new_html, n = pattern.subn(new_block, html, count=1)

    if n == 0:
        print("ERROR: replacement failed.", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print("-- DRY RUN: new data block --")
        print(new_block)
    else:
        HTML_FILE.write_text(new_html, encoding="utf-8")
        threats_n = len(data.get("threats", []))
        dtree_n   = len(data.get("dtree",   []))
        print(f"Updated {HTML_FILE}")
        print(f"  threats={threats_n}  dtree nodes={dtree_n}")
        print(f"  sidebar sections: citations={len(data.get('sidebar',{}).get('citations',[]))} "
              f"frameworks={len(data.get('sidebar',{}).get('frameworks',[]))} "
              f"regulatory={len(data.get('sidebar',{}).get('regulatory',[]))}")
        print(f"  docs: synthesis={len(data.get('synthesis',[]))} "
              f"concepts={len(data.get('concepts',[]))} "
              f"sources={len(data.get('sources',[]))} "
              f"evaluation={len(data.get('evaluation',[]))} "
              f"analysis={len(data.get('analysis',[]))}")


if __name__ == "__main__":
    main()
