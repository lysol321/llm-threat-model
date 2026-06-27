#!/usr/bin/env python3
"""
build-html.py — regenerates the DATA_START..DATA_END block in llm-threat-model.html
from threat-model-data.json.

Edit threat-model-data.json, then run this script to update the HTML.

Usage:
    python scripts/build-html.py [--dry-run]
    python scripts/build-html.py --no-md       # skip MD->HTML (use html field as-is)

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


def embed_synthesis_html(synthesis_entries: list, no_md: bool) -> list:
    """Attach an `html` field to each synthesis entry, reading the markdown file
    and rendering it via the stdlib-only md_to_html converter. Pass --no-md to
    preserve any pre-existing `html` field without touching the source files."""
    if no_md:
        return synthesis_entries

    from md_to_html import render  # local import; only needed for the MD pass

    out = []
    for s in synthesis_entries:
        file_field = s.get("file")
        if not file_field:
            out.append(s)
            continue
        md_path = ROOT / file_field
        if not md_path.exists():
            print(f"WARN: {md_path} not found — synthesis entry '{s.get('title')}' has no html", file=sys.stderr)
            out.append(s)
            continue
        # Normalize line endings: synthesis files may be CRLF on Windows; the
        # converter expects LF. Without this, embedded HTML would contain \r\n
        # inside JSON string values (invalid JSON).
        md_text = md_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        # compact=True: emit single-line HTML safe to embed in a JS string literal
        # (real LF bytes would break the JS string parse).
        html = render(md_text, compact=True)
        out.append({**s, "html": html})
    return out


def build_data_block(data: dict, no_md: bool) -> str:
    lines = [START_SENTINEL]

    if data.get("threats"):
        lines.append(f"const THREATS = {js(data['threats'])};")
    if data.get("dtree"):
        lines.append(f"const DTREE_DATA = {js(data['dtree'])};")

    synthesis_with_html = embed_synthesis_html(data.get("synthesis", []), no_md)

    # Assemble SIDEBAR_DATA from JSON sections
    sidebar_obj = {
        "citations":  data.get("sidebar", {}).get("citations",  []),
        "frameworks": data.get("sidebar", {}).get("frameworks", []),
        "regulatory": data.get("sidebar", {}).get("regulatory", []),
        "synthesis":  synthesis_with_html,
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
    no_md   = "--no-md"   in sys.argv

    if not JSON_FILE.exists():
        print(f"ERROR: {JSON_FILE} not found. Run export-data.py first.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    # Read as binary to preserve original line endings (Windows CRLF).
    html = HTML_FILE.read_bytes().decode("utf-8")

    pattern = re.compile(
        r'(' + re.escape(START_SENTINEL) + r').*?(' + re.escape(END_SENTINEL) + r')',
        re.DOTALL
    )

    if not pattern.search(html):
        print(f"ERROR: sentinels not found in {HTML_FILE}", file=sys.stderr)
        print(f"  Expected: {START_SENTINEL!r}", file=sys.stderr)
        sys.exit(1)

    new_block  = build_data_block(data, no_md)
    new_html, n = pattern.subn(new_block, html, count=1)

    if n == 0:
        print("ERROR: replacement failed.", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print("-- DRY RUN: new data block --")
        print(new_block[:2000] + ("..." if len(new_block) > 2000 else ""))
    else:
        # Write as binary to preserve original line endings (Windows CRLF).
        HTML_FILE.write_bytes(new_html.encode("utf-8"))
        threats_n = len(data.get("threats", []))
        dtree_n   = len(data.get("dtree",   []))
        syn_n     = len(data.get("synthesis", []))
        syn_with_html = sum(1 for s in data.get("synthesis", []) if s.get("file"))
        print(f"Updated {HTML_FILE}")
        print(f"  threats={threats_n}  dtree nodes={dtree_n}")
        print(f"  sidebar sections: citations={len(data.get('sidebar',{}).get('citations',[]))} "
              f"frameworks={len(data.get('sidebar',{}).get('frameworks',[]))} "
              f"regulatory={len(data.get('sidebar',{}).get('regulatory',[]))}")
        print(f"  docs: synthesis={syn_n} (inlined html={syn_with_html}{'skipped --no-md' if no_md else ''}) "
              f"concepts={len(data.get('concepts',[]))} "
              f"sources={len(data.get('sources',[]))} "
              f"evaluation={len(data.get('evaluation',[]))} "
              f"analysis={len(data.get('analysis',[]))}")


if __name__ == "__main__":
    main()
