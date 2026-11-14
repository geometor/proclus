"""Deterministic apparatus compiler and Multi-Track Codex verifier for GEOMETOR Proclus."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from geometor.proclus.concordance import CODEX_UNITS, CODEX_UNITS_BY_SLUG, default_resources_dir


def slugify_key(key: str) -> str:
    """Slugify an apparatus key identically to ``photon_platform.publish.roles.geometry``."""
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def default_docsrc_book_dir() -> Path:
    """Return ``docsrc/in_euclidem`` path."""
    return Path(__file__).resolve().parents[3] / "docsrc" / "in_euclidem"


def render_concordance_rst(concordance: dict[str, Any]) -> str:
    """Render ``docsrc/in_euclidem/concordance.rst`` from ``concordance.json``."""
    entries = concordance["entries"]
    meta = concordance["metadata"]

    lines: list[str] = [
        ":navigation: footer",
        ":order: 90",
        ":nav_title: Concordance",
        ":layout: book",
        ":type: apparatus",
        "",
        ".. _friedlein-concordance:",
        "",
        "Friedlein Citation Concordance",
        "==============================",
        "",
        (
            "Complete bidirectional concordance mapping every passage of Proclus's "
            "*Commentary on the First Book of Euclid's Elements* (*ed.* Gottfried Friedlein, "
            f"Leipzig: B. G. Teubner, 1873) cited across **GEOMETOR** (`euclid` and `hoenen`) "
            f"— **{len(entries)} canonical Friedlein loci** encompassing "
            f"**{meta['euclid_distinct_keys']}** distinct `euclid` citation keys "
            f"({meta['euclid_total_occurrences']} citing occurrences across Heath Vols. I–III) "
            f"and **{meta['hoenen_total_loci']}** philosophical-epistemological loci in Hoenen's "
            "*De Noetica Geometriae*."
        ),
        "",
        "Overview by Codex Unit",
        "----------------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 26 16 14 44",
        "",
        "   * - Codex Unit",
        "     - Friedlein Pages",
        "     - Cited Loci",
        "     - Scope",
    ]

    by_unit: dict[str, list[dict[str, Any]]] = {u.slug: [] for u in CODEX_UNITS}
    for e in entries:
        by_unit[e["codex_unit"]].append(e)

    for u in CODEX_UNITS:
        u_entries = by_unit[u.slug]
        lines.extend(
            [
                f"   * - :doc:`{u.number_label} <{u.slug}/{u.slug}-en>`",
                f"     - pp. {u.friedlein_start}–{u.friedlein_end}",
                f"     - {len(u_entries)}",
                f"     - {u.subtitle}",
            ]
        )
    lines.append("")

    for u in CODEX_UNITS:
        u_entries = by_unit[u.slug]
        heading = f"{u.number_label} (Friedlein pp. {u.friedlein_start}–{u.friedlein_end})"
        lines.extend(
            [
                f".. _concordance-{u.slug}:",
                "",
                heading,
                "-" * len(heading),
                "",
                (
                    f"Codex tracks: :doc:`English <{u.slug}/{u.slug}-en>` · "
                    f":doc:`Greek (1873) <{u.slug}/{u.slug}-el>` · "
                    f":doc:`Summary <{u.slug}/{u.slug}-summary>` · "
                    f":doc:`Notes <{u.slug}/{u.slug}-notes>`"
                ),
                "",
            ]
        )
        for entry in u_entries:
            anchor = entry["id"]
            canon = entry["canonical_locus"]
            sec_id = entry["codex_section_id"]
            sec_title = entry["codex_section_title"]
            topic = entry["topic"]
            just_str = f" · Euclid :just:`{entry['euclid_element']}`" if entry.get("euclid_element") else ""

            lines.extend(
                [
                    f".. _{anchor}:",
                    "",
                    f"**{canon}** — :ref:`{sec_title} <{sec_id}>`{just_str}",
                    f"  {topic}",
                ]
            )

            cite_parts: list[str] = []
            for ec in entry.get("euclid_citations", []):
                vol_lbl = ec["volume"].replace("volume_", "Vol. ")
                folio = ec.get("folio", "")
                page = ec.get("page", "")
                key = ec["citation_key"]
                sec = ec.get("section", "")
                book_num = ec.get("book", "")
                loc_desc = f"Heath {vol_lbl}, p. {page}"
                if book_num:
                    loc_desc += f" (Bk. {book_num}, {sec})"
                elif sec:
                    loc_desc += f" ({sec})"
                if folio:
                    cite_parts.append(f"`euclid` ``{key}`` — {loc_desc} [folio ``{folio}``]")
                else:
                    cite_parts.append(f"`euclid` ``{key}`` — {loc_desc}")

            for hc in entry.get("hoenen_citations", []):
                h_page = hc.get("page", "")
                h_chap = hc.get("book", "")
                h_key = hc.get("citation_key") or "prose"
                h_disp = hc.get("display", "")
                cite_parts.append(
                    f"`hoenen` ``{h_key}`` — *De Noetica Geometriae* {h_chap}, p. {h_page} (*{h_disp}*)"
                )

            if cite_parts:
                lines.append("")
                for cp in cite_parts:
                    lines.append(f"  * {cp}")
            lines.append("")

    # Also note cross-work Timaeus commentary reference in Euclid
    if concordance.get("related_proclus_works"):
        lines.extend(
            [
                "Related Works of Proclus Cited in GEOMETOR",
                "------------------------------------------",
                "",
            ]
        )
        for rw in concordance["related_proclus_works"]:
            lines.append(
                f"* **{rw['work']}** (``{rw['citation_key']}``) — {rw['note']}"
            )
        lines.append("")

    return "\n".join(lines)


def render_bibliography_rst(citations: dict[str, dict[str, Any]]) -> str:
    """Render ``docsrc/in_euclidem/bibliography.rst`` from ``citations.json``."""
    lines: list[str] = [
        ":navigation: header",
        ":order: 6",
        ":nav_title: Bibliography",
        ":layout: book",
        ":type: apparatus",
        "",
        ".. _codex-bibliography:",
        "",
        "============",
        "Bibliography",
        "============",
        "",
        (
            "Critical register of primary editions, translations, ancient mathematical "
            "authorities cited by Proclus, and modern GEOMETOR companion treatises. "
            "Every ``:cite:`` reference in the Codex resolves directly to its entry below."
        ),
        "",
    ]

    groups = [
        ("Primary Editions & Translations of Proclus", "edition"),
        ("Ancient Philosophical & Mathematical Sources Cited by Proclus", "ancient"),
        ("Companion GEOMETOR & Modern Critical Works", "modern"),
    ]

    for group_title, category in groups:
        items = [(k, v) for k, v in citations.items() if v.get("category", "ancient") == category]
        if not items:
            continue
        lines.extend([group_title, "-" * len(group_title), ""])
        for key, entry in sorted(items, key=lambda kv: (kv[1].get("author", ""), kv[0])):
            slug = slugify_key(key)
            author = entry.get("author", "")
            work = entry.get("work", "")
            locus = entry.get("locus", "")
            year = entry.get("year", "")
            note = entry.get("note", "")
            url = entry.get("url", "")
            header = f"**{author}** — *{work}*"
            if locus:
                header += f" ({locus})"
            if year:
                header += f" [{year}]"
            lines.extend(
                [
                    f".. _cite-{slug}:",
                    "",
                    header,
                    f"  Key: ``{key}``",
                ]
            )
            if note:
                lines.append(f"  {note}")
            if url:
                lines.append(f"  Provenance: `{url} <{url}>`__")
            lines.append("")

    return "\n".join(lines)


def render_persons_rst(persons: dict[str, dict[str, Any]]) -> str:
    """Render ``docsrc/in_euclidem/persons.rst`` from ``persons.json``."""
    lines: list[str] = [
        ":navigation: header",
        ":order: 5",
        ":nav_title: People",
        ":layout: book",
        ":type: apparatus",
        "",
        ".. _codex-persons:",
        "",
        "======",
        "People",
        "======",
        "",
        (
            "Prosopographical register of geometers, philosophers, commentators, and "
            "editors appearing in Proclus's *Commentary* (including all twenty-three "
            "geometers of the **Eudemian Summary**, Friedlein pp. 64–70) and in the "
            "textual transmission of the Codex."
        ),
        "",
    ]

    eras = [
        ("Pre-Euclidean & Classical Geometers and Philosophers", "classical"),
        ("Euclid & Hellenistic Mathematicians and Critics", "hellenistic"),
        ("Late Antique & Neoplatonic Commentators", "neoplatonic"),
        ("Renaissance & Modern Editors, Translators, and Scholars", "modern"),
    ]

    for era_title, era_key in eras:
        items = [(k, v) for k, v in persons.items() if v.get("era", "classical") == era_key]
        if not items:
            continue
        lines.extend([era_title, "-" * len(era_title), ""])
        for key, entry in sorted(items, key=lambda kv: kv[1].get("sort_year", 0)):
            slug = slugify_key(key)
            name = entry["name"]
            greek = entry.get("greek", "")
            dates = entry.get("dates", "")
            summary = entry["summary"]
            loci = entry.get("friedlein_loci", "")
            title_line = f"**{name}**"
            if greek:
                title_line += f" (*{greek}*)"
            if dates:
                title_line += f" — {dates}"
            lines.extend(
                [
                    f".. _person-{slug}:",
                    "",
                    title_line,
                    f"  {summary}",
                ]
            )
            if loci:
                lines.append(f"  *Friedlein loci*: {loci}.")
            lines.append("")

    return "\n".join(lines)


def render_glossary_rst(glossary: dict[str, dict[str, Any]]) -> str:
    """Render ``docsrc/in_euclidem/glossary.rst`` from ``glossary.json``."""
    lines: list[str] = [
        ":navigation: footer",
        ":order: 93",
        ":nav_title: Glossary",
        ":layout: book",
        ":type: apparatus",
        "",
        ".. _codex-glossary:",
        "",
        "========",
        "Glossary",
        "========",
        "",
        (
            "Lexicon of Greek mathematical, logical, and Neoplatonic epistemological "
            "terminology in Proclus's *Commentary on Book I*, cross-referenced with "
            "Euclid's *Elements* and Petrus Hoenen's Scholastic-noetic vocabulary."
        ),
        "",
    ]

    for key, entry in sorted(glossary.items(), key=lambda kv: kv[0]):
        slug = slugify_key(key)
        term = entry["term"]
        greek = entry.get("greek", "")
        latin = entry.get("latin", "")
        english = entry.get("english", "")
        definition = entry["definition"]
        loci = entry.get("friedlein_loci", "")
        head = f"**{term}**"
        if greek:
            head += f" (*{greek}*)"
        if latin:
            head += f" · Lat. *{latin}*"
        if english:
            head += f" — {english}"
        lines.extend(
            [
                f".. _term-{slug}:",
                "",
                head,
                f"  {definition}",
            ]
        )
        if loci:
            lines.append(f"  *Friedlein loci*: {loci}.")
        lines.append("")

    return "\n".join(lines)


def write_apparatus_pages(
    resources_dir: Path | None = None,
    book_dir: Path | None = None,
) -> list[Path]:
    """Compile all four apparatus RST files (`concordance`, `bibliography`, `persons`, `glossary`)."""
    res = resources_dir or default_resources_dir()
    bdir = book_dir or default_docsrc_book_dir()
    bdir.mkdir(parents=True, exist_ok=True)

    concordance = json.loads((res / "concordance.json").read_text(encoding="utf-8"))
    citations = json.loads((res / "citations.json").read_text(encoding="utf-8"))
    persons = json.loads((res / "persons.json").read_text(encoding="utf-8"))
    glossary = json.loads((res / "glossary.json").read_text(encoding="utf-8"))

    outputs = [
        (bdir / "concordance.rst", render_concordance_rst(concordance)),
        (bdir / "bibliography.rst", render_bibliography_rst(citations)),
        (bdir / "persons.rst", render_persons_rst(persons)),
        (bdir / "glossary.rst", render_glossary_rst(glossary)),
    ]
    written: list[Path] = []
    for path, content in outputs:
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def verify_codex_tracks(book_dir: Path | None = None) -> dict[str, Any]:
    """Verify that all 7 Codex units have all 4 synchronized tracks and zero Python construction code."""
    bdir = book_dir or default_docsrc_book_dir()
    errors: list[str] = []
    track_counts = 0

    required_root_files = [
        "index.rst",
        "concordance.rst",
        "bibliography.rst",
        "persons.rst",
        "glossary.rst",
    ]
    for rf in required_root_files:
        if not (bdir / rf).is_file():
            errors.append(f"Missing book apparatus/index file: {bdir / rf}")

    code_block_re = re.compile(r"^\.\.\s+code-block::\s*(?:python|py)\b", re.MULTILINE)

    for unit in CODEX_UNITS:
        udir = bdir / unit.slug
        for suffix in ("en", "el", "summary", "notes"):
            f = udir / f"{unit.slug}-{suffix}.rst"
            if not f.is_file():
                errors.append(f"Missing unit track file: {f}")
                continue
            track_counts += 1
            txt = f.read_text(encoding="utf-8")
            if code_block_re.search(txt):
                errors.append(f"Forbidden embedded Python code-block found in historical treatise: {f}")
            if suffix in ("en", "el") and ".. folio::" not in txt:
                errors.append(f"Expected `.. folio::` Friedlein milestone markers in {f}")

    # Also check root index.rst has :layout: book
    idx_path = bdir / "index.rst"
    if idx_path.is_file():
        idx_txt = idx_path.read_text(encoding="utf-8")
        if ":layout: book" not in idx_txt:
            errors.append("Missing `:layout: book` metadata in docsrc/in_euclidem/index.rst")

    return {
        "valid": len(errors) == 0,
        "units": len(CODEX_UNITS_BY_SLUG),
        "track_files": track_counts,
        "errors": errors,
    }
