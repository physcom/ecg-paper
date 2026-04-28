"""
Fix for 'Elaman Nazarkulov - ara rapor değerlendirme formu v4.docx'.

The previous v4 was an almost-empty cover page because it was built from
scratch. The original template is in fact the full report (cover + all
sections + figures + references) — structurally identical to the 'short'
template. The fix is to reuse the same in-place editing approach from
fix_short_v4.py: copy the original, surgically replace text inside specific
cells, embed the new v4 figures, and save. Headers, first-page footer
(KTMÜ yönerge), cover-page logo (top-level P3), page size, and Times New
Roman fonts are preserved because we never touch them.
"""

from __future__ import annotations

from pathlib import Path

from fix_short_v4 import rewrite_short_v4

OUT_DIR = Path(r"C:\Users\enazarkulov\Documents\Мастер")
SRC = OUT_DIR / "Elaman Nazarkulov - ara rapor değerlendirme formu.docx"
DST = OUT_DIR / "Elaman Nazarkulov - ara rapor değerlendirme formu v4.docx"

if __name__ == "__main__":
    rewrite_short_v4(SRC, DST)
