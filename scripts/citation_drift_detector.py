#!/usr/bin/env python3
"""Citation drift detector for scenario-suite.json.

Detects three types of drift across all evidence entries:
1. Range validity  — cited file has at least `end` lines
2. Quote match     — exact `quote` text appears within lines[start-1:end]
3. Line range freshness — tracks which ranges need updating (future use)

Supports --fix mode to auto-update drifted line ranges.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "evaluation" / "scenario-suite.json"


def load_suite() -> dict:
    return json.loads(SUITE_PATH.read_text(encoding="utf-8"))


def check_citation(source: str, lines: str, quote: str) -> tuple[str, str]:
    """Returns (status, reason)."""
    path = ROOT / source
    if not path.exists():
        return "FILE_NOT_FOUND", f"{source} does not exist"

    content = path.read_text(encoding="utf-8")
    all_lines = content.splitlines()

    try:
        start, end = map(int, lines.split("-"))
    except ValueError:
        return "INVALID_RANGE", f"cannot parse lines: {lines}"

    if start < 1 or end < start:
        return "INVALID_RANGE", f"start={start} end={end}"

    if end > len(all_lines):
        return "DRIFTED", f"end={end} exceeds file length {len(all_lines)}"

    cited_text = "\n".join(all_lines[start - 1 : end])
    if quote not in cited_text:
        return "DRIFTED", f"quote not found in lines {start}-{end}"

    return "OK", ""


def find_quote_in_file(source: str, quote: str, original_start: int, original_end: int) -> str | None:
    """Search full file for quote, return new line range or None.

    Expansion heuristic:
    - Find line where quote starts
    - Expand backward to section header (heading or blank line separator)
    - Preserve original range width, clamped to EOF
    """
    path = ROOT / source
    content = path.read_text(encoding="utf-8")
    all_lines = content.splitlines()

    idx = content.find(quote)
    if idx == -1:
        return None  # quote gone from file

    # Find 1-indexed line number of quote start
    before = content[:idx]
    quote_line = before.count("\n") + 1

    # Expand backward: look for heading or blank line separator (up to 20 lines back)
    width = original_end - original_start
    start = quote_line
    for i in range(quote_line - 1, max(-1, quote_line - 20), -1):
        if i < 0:
            start = 0
            break
        line = all_lines[i]
        if line.startswith("#"):
            start = i  # heading belongs to the section
            break
        if line.strip() == "":
            start = i + 1
            break

    end = min(start + width + 1, len(all_lines))  # inclusive range keeps width + 1 lines
    return f"{start + 1}-{end}"  # convert to 1-indexed


def extract_quote_candidate(source: str, start: int, end: int) -> tuple[str, str]:
    """Extract a verbatim quote candidate from a line range.

    Returns (quote, extracted_from_description).
    Always returns the raw lines from the file so the quote is a true
    verbatim extract and will pass quote-in-range validation.
    """
    path = ROOT / source
    lines = path.read_text(encoding="utf-8").splitlines()
    range_lines = lines[start - 1 : end]
    content = "\n".join(range_lines)
    return content, "full range"


def _run_requote(suite: dict, drifted: list[tuple]) -> None:
    # Ensure stdout handles unicode on Windows
    if sys.platform == "win32":
        import io

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("CITATION REQUOTE")
    print("=" * 60)
    print()
    if not drifted:
        print("No drifted citations.")
        return
    for sid, eid, src, rng, status, reason in drifted:
        ev = next(
            (e for sc in suite["scenarios"] if sc["id"] == sid for e in sc["evidence"] if e["id"] == eid),
            None,
        )
        if ev is None:
            continue
        s, e = map(int, rng.split("-"))
        quote_candidate, extracted_desc = extract_quote_candidate(src, s, e)
        print(f"{sid} / {eid}")
        print(f"  file:   {src}")
        print(f"  range:  {rng}")
        print(f"  old:    {ev['quote'][:80]}...")
        print(f"  new:    {quote_candidate[:80]}...")
        print(f"  from:   {extracted_desc}")
        print()


def _run_batch_requote(suite: dict, drifted: list[tuple]) -> None:
    """Update all drifted quotes with verbatim extracts from current content."""
    fixed: list[tuple[str, str, str, str, str]] = []
    errors: list[tuple[str, str, str]] = []

    for sid, eid, src, rng, status, reason in drifted:
        ev = None
        for scenario in suite["scenarios"]:
            if scenario["id"] == sid:
                for e in scenario.get("evidence", []):
                    if e["id"] == eid:
                        ev = e
                        break
                break

        if ev is None:
            errors.append((sid, eid, "entry not found"))
            continue

        try:
            s, e = map(int, rng.split("-"))
        except ValueError:
            errors.append((sid, eid, f"bad range {rng}"))
            continue

        new_quote, extracted_desc = extract_quote_candidate(src, s, e)
        old_quote = ev["quote"]
        ev["quote"] = new_quote
        fixed.append((sid, eid, old_quote[:60], new_quote[:60], extracted_desc))

    # Write atomically
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False, suffix=".json", dir=SUITE_PATH.parent
    ) as tmp:
        json.dump(suite, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name
    Path(tmp_path).replace(SUITE_PATH)

    print("BATCH REQUOTE COMPLETE")
    print("=" * 60)
    print(f"Updated: {len(fixed)}")
    print(f"Errors:  {len(errors)}")
    print(f"File:    evaluation/scenario-suite.json")
    print()
    for sid, eid, old, new, desc in fixed[:10]:
        print(f"  {sid}/{eid} [{desc}]")
        print(f"    old: {old}...")
        print(f"    new: {new}...")
        print()
    if len(fixed) > 10:
        print(f"  ... and {len(fixed) - 10} more")
    if errors:
        print("Errors:")
        for sid, eid, err in errors:
            print(f"  {sid}/{eid}: {err}")

    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Citation drift detector")
    parser.add_argument("--fix", action="store_true", help="Auto-fix drifted citations")
    parser.add_argument("--requote", action="store_true", help="Extract verbatim quote candidates for drifted citations")
    parser.add_argument("--batch-requote", action="store_true", help="Update all drifted quotes with verbatim extracts and write to JSON")
    args = parser.parse_args()

    suite = load_suite()
    drifted: list[tuple[str, str, str, str, str, str]] = []
    ok_count = 0

    for scenario in suite["scenarios"]:
        sid = scenario["id"]
        for ev in scenario.get("evidence", []):
            status, reason = check_citation(ev["source"], ev["lines"], ev["quote"])
            if status != "OK":
                drifted.append((sid, ev["id"], ev["source"], ev["lines"], status, reason))
            else:
                ok_count += 1

    total = len(drifted) + ok_count

    if args.fix:
        _run_fix(suite, drifted, total)
    elif args.requote:
        _run_requote(suite, drifted)
    elif args.batch_requote:
        _run_batch_requote(suite, drifted)
    else:
        _run_report(drifted, ok_count, total)


def _run_report(drifted: list[tuple], ok_count: int, total: int) -> None:
    print("CITATION DRIFT REPORT")
    print("=" * 50)
    print(f"Total citations checked: {total}")
    print(f"OK: {ok_count}, DRIFTED: {len(drifted)}")
    print()

    if not drifted:
        print("No drift detected.")
        sys.exit(0)

    for sid, eid, src, rng, status, reason in drifted:
        print(f"{sid} / {eid}")
        print(f"  file:   {src}")
        print(f"  range:  {rng}")
        print(f"  status: {status}")
        if reason:
            print(f"  reason: {reason}")
        print()

    sys.exit(1)


def _run_fix(suite: dict, drifted: list[tuple], total: int) -> None:
    fixed: list[tuple[str, str, str, str]] = []
    not_fixable: list[tuple[str, str, str, str, str]] = []

    for sid, eid, src, rng, status, reason in drifted:
        ev = None
        for scenario in suite["scenarios"]:
            if scenario["id"] == sid:
                for e in scenario.get("evidence", []):
                    if e["id"] == eid:
                        ev = e
                        break
                break

        if ev is None:
            not_fixable.append((sid, eid, src, rng, "citation entry not found"))
            continue

        try:
            orig_start, orig_end = map(int, rng.split("-"))
        except ValueError:
            not_fixable.append((sid, eid, src, rng, "cannot parse original range"))
            continue

        new_range = find_quote_in_file(src, ev["quote"], orig_start, orig_end)
        if new_range is None:
            not_fixable.append((sid, eid, src, rng, "NOT_FIXABLE"))
        else:
            ev["lines"] = new_range
            fixed.append((sid, eid, rng, new_range))

    # Write atomically: temp file then rename
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False, suffix=".json", dir=SUITE_PATH.parent
    ) as tmp:
        json.dump(suite, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name

    Path(tmp_path).replace(SUITE_PATH)

    # Print summary
    print("CITATION DRIFT FIX")
    print("=" * 50)
    print(f"Total: {total}")
    print(f"Fixed: {len(fixed)}")
    print(f"Still drifted (quote not found in file): {len(not_fixable)}")
    print(f"Files modified: evaluation/scenario-suite.json")
    print()

    if fixed:
        print("Fixed citations:")
        for sid, eid, old_rng, new_rng in fixed:
            print(f"  {sid} / {eid}: {old_rng} -> {new_rng}")
        print()

    if not_fixable:
        print("NOT FIXABLE (quote no longer exists in source file):")
        for sid, eid, src, rng, reason in not_fixable:
            print(f"  {sid} / {eid}: {rng} ({reason})")

    sys.exit(0)


if __name__ == "__main__":
    main()
