# HTML Architecture Design — LLM Threat Model

## Goal
Design HTML architecture until satisfied. After each step: test visually, self-review, commit. Stop if 3 straight iterations add nothing defensible.

## Session Log

### Pass 1: Initial Assessment
- Read entire HTML file
- File: 1000 lines, single monolithic structure
- Size: ~50KB (inline CSS + JS + data)
- Structure: Header + Nav + Main (7 tabs) + Script block

**Architecture Status:**
- ✓ Single-file simplicity
- ✓ No external dependencies
- ✓ Mobile-responsive (media queries present)
- ✓ Dark theme with accent colors
- ⚠ Large embedded data arrays (THREATS, DTREE_DATA)
- ⚠ All JS inline; no modular structure
- ⚠ No error boundaries for interactive features
- ? Accessibility: needs testing

### Pass 2: Visual & Interactive Testing
Tested all major features:
- ✓ Overview tab → stats cards, insight cards, how-to steps all render
- ✓ Threats tab → 14 threats display, filter/search buttons present, expand/collapse works
- ✓ Decision Tree tab → Q1-Q4 display, YES click triggers sub-questions, dynamic state updates
- ✓ Sticky header + nav work smoothly
- ✓ Print button functional (print styles defined)

**Working Well:**
- Tab switching smooth, tab state persists visually
- Threat card expand animation is fluid
- Decision Tree state logic works (sub-Qs appear on YES, summary updates)
- Color coding consistent (CRITICAL=red, HIGH=orange, MEDIUM=yellow, LOW=green)
- No JavaScript errors detected

**Improvement Opportunities (ranked by impact):**
1. **Data Extraction** — THREATS (14 items) + DTREE_DATA (4 Qs) should be JSON external files for maintainability
2. **Accessibility** — Missing ARIA labels on interactive elements (buttons, expandable sections, tab panels)
3. **Error Handling** — No try/catch around data rendering; malformed data would fail silently
4. **Code Modularity** — Consider splitting JS into (init, tabs, threats, dtree) — though single file is valid for this scale
5. **Keyboard Navigation** — Tab order and focus management could be improved

**Not Critical (polish only):**
- CSS is well-organized, CSS-in-head is acceptable for single-file app
- Print styles exist
- Mobile responsive design works

**Defensible Design Decision:** Single 1000-line file is reasonable for a static threat model that changes rarely. Trade-off: simplicity + easy distribution vs. harder maintenance. External data files would improve this.

**Next Step:** Focus on accessibility (ARIA labels, keyboard nav) and data extraction. Test keyboard-only usage.
