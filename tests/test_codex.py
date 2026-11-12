"""Unit tests for the 4-track Book Codex, apparatus registries, Sphinx track extension, and CLI."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from geometor.proclus.cli import main as cli_main
from geometor.proclus.compile_codex import (
    default_docsrc_book_dir,
    slugify_key,
    verify_codex_tracks,
)
from geometor.proclus.concordance import CODEX_UNITS, default_resources_dir, load_concordance
from geometor.proclus.sphinx_ext import register_greek_book_track


def _extract_role_targets(rst_text: str, role_name: str) -> list[str]:
    """Extract target keys from inline ``:<role_name>:`Display <key>``` or ``:<role_name>:`key```."""
    pattern = re.compile(rf":{role_name}:`([^`]+)`")
    targets: list[str] = []
    for match in pattern.finditer(rst_text):
        body = match.group(1).strip()
        m_angle = re.match(r"^.+?\s+<([^<>]+)>$", body)
        targets.append(m_angle.group(1).strip() if m_angle else body)
    return targets


class TestCodexTracksAndStructure:
    """Verify the 7 canonical Codex units and 28 synchronized track files."""

    def test_verify_codex_tracks_passes_cleanly(self) -> None:
        report = verify_codex_tracks()
        assert report["valid"] is True, f"Codex verification errors: {report['errors']}"
        assert report["units"] == 7
        assert report["track_files"] == 28
        assert report["errors"] == []

    def test_all_concordance_section_anchors_exist_in_english_tracks(self) -> None:
        book_dir = default_docsrc_book_dir()
        all_en_text = "\n".join(
            (book_dir / u.slug / f"{u.slug}-en.rst").read_text(encoding="utf-8")
            for u in CODEX_UNITS
        )
        conc = load_concordance()
        missing_anchors = [
            entry["codex_section_id"]
            for entry in conc["entries"]
            if f".. _{entry['codex_section_id']}:" not in all_en_text
        ]
        assert missing_anchors == []


class TestApparatusRegistriesAndCrossReferences:
    """Verify JSON schemas and 100% resolution of :cite:, :person:, and :term: roles across docsrc."""

    def test_apparatus_json_schemas_and_mirrors(self) -> None:
        res_dir = default_resources_dir()
        root_res_dir = res_dir.parent

        citations = json.loads((res_dir / "citations.json").read_text(encoding="utf-8"))
        persons = json.loads((res_dir / "persons.json").read_text(encoding="utf-8"))
        glossary = json.loads((res_dir / "glossary.json").read_text(encoding="utf-8"))

        assert len(citations) >= 20
        for key, entry in citations.items():
            assert entry.get("author"), f"Missing author in citation {key}"
            assert entry.get("work"), f"Missing work in citation {key}"

        assert len(persons) >= 50
        for key, entry in persons.items():
            assert entry.get("name"), f"Missing name in person {key}"
            assert entry.get("summary"), f"Missing summary in person {key}"

        assert len(glossary) >= 40
        for key, entry in glossary.items():
            assert entry.get("headword") or entry.get("term"), f"Missing headword/term in glossary {key}"
            assert entry.get("definition"), f"Missing definition in glossary {key}"

        # Mirrored root resources/persons.json and resources/glossary.json must match
        mirrored_persons = json.loads((root_res_dir / "persons.json").read_text(encoding="utf-8"))
        mirrored_glossary = json.loads((root_res_dir / "glossary.json").read_text(encoding="utf-8"))
        assert set(mirrored_persons.keys()) == set(persons.keys())
        assert set(mirrored_glossary.keys()) == set(glossary.keys())

    def test_all_inline_apparatus_roles_resolve_in_registries(self) -> None:
        res_dir = default_resources_dir()
        book_dir = default_docsrc_book_dir()
        docsrc_dir = book_dir.parent

        citations = json.loads((res_dir / "citations.json").read_text(encoding="utf-8"))
        persons = json.loads((res_dir / "persons.json").read_text(encoding="utf-8"))
        glossary = json.loads((res_dir / "glossary.json").read_text(encoding="utf-8"))

        cite_slugs = {slugify_key(k) for k in citations} | set(citations.keys())
        person_slugs = {slugify_key(k) for k in persons} | set(persons.keys())
        term_slugs = {slugify_key(k) for k in glossary} | set(glossary.keys())

        unresolved_cites: list[tuple[str, str]] = []
        unresolved_persons: list[tuple[str, str]] = []
        unresolved_terms: list[tuple[str, str]] = []

        for rst_file in sorted(docsrc_dir.rglob("*.rst")):
            if "modules/api" in rst_file.as_posix():
                continue
            txt = rst_file.read_text(encoding="utf-8")
            rel = rst_file.relative_to(docsrc_dir).as_posix()
            for t in _extract_role_targets(txt, "cite"):
                if t not in cite_slugs and slugify_key(t) not in cite_slugs:
                    unresolved_cites.append((rel, t))
            for t in _extract_role_targets(txt, "person"):
                if t not in person_slugs and slugify_key(t) not in person_slugs:
                    unresolved_persons.append((rel, t))
            for t in _extract_role_targets(txt, "term"):
                if t not in term_slugs and slugify_key(t) not in term_slugs:
                    unresolved_terms.append((rel, t))

        assert unresolved_cites == [], f"Unresolved :cite: targets: {unresolved_cites}"
        assert unresolved_persons == [], f"Unresolved :person: targets: {unresolved_persons}"
        assert unresolved_terms == [], f"Unresolved :term: targets: {unresolved_terms}"


class TestGreekBookTrackAndCli:
    """Verify runtime Greek (1873) Book Codex track registration and CLI subcommands."""

    def test_register_greek_book_track_orders_four_tracks(self) -> None:
        publish_src = (
            Path(__file__).resolve().parents[3] / "photon-platform" / "publish" / "src"
        )
        if publish_src.is_dir() and str(publish_src) not in sys.path:
            sys.path.insert(0, str(publish_src))
        book = pytest.importorskip("photon_platform.publish.book")

        register_greek_book_track()
        found_docs = {
            "in_euclidem/prologue-2/prologue-2-en",
            "in_euclidem/prologue-2/prologue-2-el",
            "in_euclidem/prologue-2/prologue-2-summary",
            "in_euclidem/prologue-2/prologue-2-notes",
        }
        dummy_env = SimpleNamespace(found_docs=found_docs)

        tracks_from_en = book.detect_companion_tracks(
            dummy_env, "in_euclidem/prologue-2/prologue-2-en"
        )
        assert [t["key"] for t in tracks_from_en] == ["en", "el", "summary", "notes"]
        assert [t["label"] for t in tracks_from_en] == [
            "English",
            "Greek (1873)",
            "Summary",
            "Notes",
        ]
        assert [t["active"] for t in tracks_from_en] == [True, False, False, False]

        tracks_from_el = book.detect_companion_tracks(
            dummy_env, "in_euclidem/prologue-2/prologue-2-el"
        )
        assert [t["key"] for t in tracks_from_el] == ["en", "el", "summary", "notes"]
        assert [t["active"] for t in tracks_from_el] == [False, True, False, False]
        assert book._is_auxiliary_track_doc(
            dummy_env, "in_euclidem/prologue-2/prologue-2-el"
        ) is True

    def test_cli_summary_and_verify_exit_zero(self, capsys: object) -> None:
        assert cli_main(["summary"]) == 0
        assert cli_main(["verify"]) == 0
