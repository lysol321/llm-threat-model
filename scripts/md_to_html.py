"""Minimal Markdown -> HTML converter, stdlib only.

Covers the subset used in this repo's synthesis docs:
  - ATX headers (# ... ######)
  - paragraphs
  - bullet lists (- * +)
  - ordered lists (1. ...)
  - fenced code blocks (``` with optional language)
  - inline code, bold, italic
  - links [text](url)
  - horizontal rules (---)
  - blockquotes (>)
  - GFM tables

Not covered (not present in source files): footnotes, nested blockquotes,
task lists, raw HTML in markdown, reference-style links.

Output is HTML-safe (text content is escaped) and ready for embedding via
innerHTML. Inputs are author-controlled (synthesis corpus), not user input.
"""
from __future__ import annotations

import re
from html import escape


# ── Inline transforms ────────────────────────────────────────────────

def _inline(text: str) -> str:
    # Extract inline code first; protect from further processing.
    code_tokens: list[str] = []

    def stash(m: re.Match) -> str:
        code_tokens.append(escape(m.group(1), quote=False))
        return f"\x00CODE{len(code_tokens) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)

    # Escape HTML-special characters in remaining text.
    text = escape(text, quote=False)

    # Links: [text](url) — escape URL minimally (allow http, https, mailto, anchors, paths).
    def link_sub(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        # Conservative URL filter: allow common safe schemes + relative paths/anchors.
        if not re.match(r"^(https?://|mailto:|#|/|\.)", url):
            return f"[{label}]({url})"
        return f'<a href="{escape(url, quote=True)}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_sub, text)

    # Bold then italic (bold first so ** is consumed before *).
    # Use word-boundary anchors so identifiers like Wild_vs_Theory aren't mangled.
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)__([^_]+)__(?!\w)", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\b\*([^*\s][^*]*?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)\b_([^_\s][^_]*?)_(?!\w)", r"<em>\1</em>", text)

    # Restore inline code tokens.
    def unstash(m: re.Match) -> str:
        idx = int(m.group(1))
        return f"<code>{code_tokens[idx]}</code>"

    text = re.sub(r"\x00CODE(\d+)\x00", unstash, text)
    return text


# ── Block-level parser ───────────────────────────────────────────────

_FENCE_RE = re.compile(r"^```(\w*)\s*$")
_HR_RE    = re.compile(r"^\s{0,3}(?:-\s?){3,}\s*$|^\s{0,3}(?:\*\s?){3,}\s*$|^\s{0,3}(?:_\s?){3,}\s*$")
_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_UL_RE    = re.compile(r"^\s{0,3}[-*+]\s+(.+)$")
_OL_RE    = re.compile(r"^\s{0,3}\d+\.\s+(.+)$")
_BQ_RE    = re.compile(r"^\s{0,3}>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


def _flush_paragraph(buf: list[str], out: list[str]) -> None:
    if not buf:
        return
    text = " ".join(buf).strip()
    if text:
        out.append(f"<p>{_inline(text)}</p>")
    buf.clear()


def _render_table(lines: list[str]) -> str:
    """Render a GFM table. Caller guarantees the header + separator lines are present."""
    def split_row(row: str) -> list[str]:
        s = row.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        return [c.strip() for c in s.split("|")]

    header = split_row(lines[0])
    body_rows = [split_row(r) for r in lines[2:]]
    th = "".join(f"<th>{_inline(h)}</th>" for h in header)
    trs = []
    for row in body_rows:
        cells = "".join(f"<td>{_inline(c)}</td>" for c in row)
        trs.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"


def render(md: str, compact: bool = False) -> str:
    """Convert a markdown string to an HTML string (no <html>/<body> wrapper).

    compact=True joins block elements with no newlines — produces a single line
    of HTML safe to embed inside a JS string literal. Default keeps block
    elements on separate lines for readable output.
    """
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ── fenced code block ──
        m = _FENCE_RE.match(line)
        if m:
            lang = m.group(1) or ""
            i += 1
            body: list[str] = []
            while i < n and not _FENCE_RE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            # Code block body: real newlines in compact mode would break the JS
            # string literal. Escape first (so & becomes &amp;), THEN replace
            # newlines with the HTML entity &#10; — order matters, otherwise
            # escape() turns our & into &amp;.
            code_body = escape("\n".join(body), quote=False)
            if compact:
                code_body = code_body.replace("\n", "&#10;")
            cls = f' class="lang-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{code_body}</code></pre>")
            continue

        # ── horizontal rule ──
        if _HR_RE.match(line):
            _flush_paragraph(para, out)
            out.append("<hr>")
            i += 1
            continue

        # ── header ──
        m = _HEADER_RE.match(line)
        if m:
            _flush_paragraph(para, out)
            level = len(m.group(1))
            out.append(f"<h{level}>{_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # ── table (header + separator + 1+ body rows) ──
        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            _flush_paragraph(para, out)
            j = i + 2
            while j < n and "|" in lines[j] and lines[j].strip():
                j += 1
            out.append(_render_table(lines[i:j]))
            i = j
            continue

        # ── blockquote ──
        if _BQ_RE.match(line):
            _flush_paragraph(para, out)
            bq: list[str] = []
            while i < n:
                bq_match = _BQ_RE.match(lines[i])
                if bq_match:
                    bq.append(bq_match.group(1))
                    i += 1
                elif lines[i].strip() == "":
                    bq.append("")
                    i += 1
                else:
                    break
            inner = render("\n".join(bq).strip("\n"), compact=compact)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # ── bullet list ──
        if _UL_RE.match(line):
            _flush_paragraph(para, out)
            items: list[str] = []
            while i < n:
                ul_match = _UL_RE.match(lines[i])
                if not ul_match:
                    break
                items.append(f"<li>{_inline(ul_match.group(1))}</li>")
                i += 1
            out.append(f"<ul>{''.join(items)}</ul>")
            continue

        # ── ordered list ──
        if _OL_RE.match(line):
            _flush_paragraph(para, out)
            items = []
            while i < n:
                ol_match = _OL_RE.match(lines[i])
                if not ol_match:
                    break
                items.append(f"<li>{_inline(ol_match.group(1))}</li>")
                i += 1
            out.append(f"<ol>{''.join(items)}</ol>")
            continue

        # ── blank line: paragraph break ──
        if not stripped:
            _flush_paragraph(para, out)
            i += 1
            continue

        # ── paragraph text ──
        para.append(line)
        i += 1

    _flush_paragraph(para, out)
    return "".join(out) if compact else "\n".join(out)
