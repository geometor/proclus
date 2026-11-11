"""Runtime Sphinx & photon-platform/publish integration for GEOMETOR Proclus.

Registers the ``el`` ("Greek (1873)") companion track in ``photon_platform.publish.book``
at build time (without modifying ``photon-platform/publish``) and configures
offline-safe local intersphinx inventories for ``euclid``, ``elements``, and ``hoenen``.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any


def register_greek_book_track() -> None:
    """Extend ``photon_platform.publish.book`` to recognize ``<stem>-el`` Greek tracks."""
    try:
        from photon_platform.publish import book
    except ImportError:
        return

    el_pattern = (r"^(.+)[._-]el$", "el", "Greek (1873)")
    if not any(key == "el" for _pat, key, _lbl in book._TRACK_SUFFIX_PATTERNS):
        book._TRACK_SUFFIX_PATTERNS.append(el_pattern)

    book._AUX_TRACK_BASENAMES.add("el")
    el_aux_re = re.compile(r"^.+[._-]el$")
    if not any(p.pattern == el_aux_re.pattern for p in book._AUX_TRACK_PATTERNS):
        book._AUX_TRACK_PATTERNS.append(el_aux_re)

    if getattr(book.detect_companion_tracks, "_proclus_el_patched", False):
        return

    orig_detect = book.detect_companion_tracks

    def _detect_with_greek(env: Any, pagename: str) -> list[dict[str, Any]]:
        found_docs: set[str] = set(getattr(env, "found_docs", set()))
        if not found_docs:
            return []

        doc_dir = os.path.dirname(pagename)
        basename = os.path.basename(pagename)
        stem = book._extract_unit_stem(basename, doc_dir)
        if basename == "el" and doc_dir:
            stem = os.path.basename(doc_dir)

        def _qual(local_name: str) -> str:
            return f"{doc_dir}/{local_name}" if doc_dir else local_name

        # Get standard tracks via reference pagename (`-en` if current is `-el`)
        probe_page = pagename
        el_candidates = [_qual(f"{stem}.el"), _qual(f"{stem}_el"), _qual(f"{stem}-el"), _qual("el")]
        el_doc = next((c for c in el_candidates if c in found_docs), None)
        if el_doc and pagename == el_doc:
            en_cand = next(
                (c for c in (_qual(f"{stem}-en"), _qual(f"{stem}_en"), _qual(f"{stem}.en")) if c in found_docs),
                None,
            )
            if en_cand:
                probe_page = en_cand

        tracks = orig_detect(env, probe_page)
        if not el_doc:
            return tracks

        # Recompute active flags against actual pagename and insert Greek (1873) right after English
        updated: list[dict[str, Any]] = []
        inserted_el = False
        el_entry = {
            "key": "el",
            "label": "Greek (1873)",
            "docname": el_doc,
            "active": el_doc == pagename,
        }
        for tr in tracks:
            if tr.get("docname") == el_doc:
                continue
            item = dict(tr)
            item["active"] = item.get("docname") == pagename
            updated.append(item)
            if item.get("key") == "en" and not inserted_el:
                updated.append(el_entry)
                inserted_el = True

        if not inserted_el:
            updated.insert(0, el_entry)

        return updated if len(updated) >= 2 else []

    _detect_with_greek._proclus_el_patched = True  # type: ignore[attr-defined]
    book.detect_companion_tracks = _detect_with_greek


def configure_local_intersphinx(intersphinx_mapping: dict[str, Any], project_root: Path) -> None:
    """Bind local ``objects.inv`` files for ``euclid``, ``elements``, and ``hoenen`` and drop unreachable remote-only targets."""
    geometor_dir = project_root.parent
    for sister in ("euclid", "elements", "hoenen"):
        inv = geometor_dir / sister / "docs" / "objects.inv"
        if inv.is_file():
            intersphinx_mapping[sister] = (
                f"https://geometor.github.io/{sister}",
                str(inv.resolve()),
            )
    # Remove remote-only inventories without a local file so offline builds produce zero warnings
    for key in list(intersphinx_mapping.keys()):
        _uri, inv_target = intersphinx_mapping[key]
        if inv_target is None:
            intersphinx_mapping.pop(key, None)


def setup(app: Any) -> dict[str, Any]:
    """Sphinx extension entry point."""
    register_greek_book_track()
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
