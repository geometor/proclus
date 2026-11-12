"""Unit tests for Friedlein (1873) locus parsing, section resolution, and concordance coverage."""

from __future__ import annotations

import pytest

from geometor.proclus.concordance import (
    CODEX_UNITS,
    FRIEDLEIN_SECTIONS,
    load_concordance,
    load_sources_manifest,
    parse_friedlein_locus,
    resolve_friedlein_section,
    verify_concordance,
)


class TestParseFriedleinLocus:
    """Verify Friedlein (1873) locus normalization across Teubner, Heath, and Hoenen notations."""

    def test_same_page_line_range(self) -> None:
        loc = parse_friedlein_locus("12.14-22")
        assert loc.start_page == 12
        assert loc.start_line == 14
        assert loc.end_page == 12
        assert loc.end_line == 22
        assert loc.canonical == "Friedlein 12, 14–22"

    def test_cross_page_line_range(self) -> None:
        loc = parse_friedlein_locus("103.21-107.10")
        assert loc.start_page == 103
        assert loc.start_line == 21
        assert loc.end_page == 107
        assert loc.end_line == 10
        assert loc.canonical == "Friedlein 103, 21–107, 10"

    def test_whole_page_range(self) -> None:
        loc = parse_friedlein_locus("64-70")
        assert loc.start_page == 64
        assert loc.start_line is None
        assert loc.end_page == 70
        assert loc.end_line is None
        assert loc.canonical == "Friedlein 64–70"

    def test_compressed_trailing_digit_page_ranges(self) -> None:
        loc_a = parse_friedlein_locus("303-4", display_hint="pp. 303-4")
        assert (loc_a.start_page, loc_a.end_page, loc_a.start_line) == (303, 304, None)
        assert loc_a.canonical == "Friedlein 303–304"

        loc_b = parse_friedlein_locus("323-6")
        assert (loc_b.start_page, loc_b.end_page) == (323, 326)

        loc_c = parse_friedlein_locus("424-5")
        assert (loc_c.start_page, loc_c.end_page) == (424, 425)

    def test_explicit_idiosyncratic_heath_keys(self) -> None:
        loc_65 = parse_friedlein_locus("65-20")
        assert (loc_65.start_page, loc_65.start_line, loc_65.end_page, loc_65.end_line) == (65, 20, 65, 20)

        loc_303_6 = parse_friedlein_locus("303-6")
        assert (loc_303_6.start_page, loc_303_6.start_line) == (303, 6)

        loc_121 = parse_friedlein_locus("121-24-122-6")
        assert (loc_121.start_page, loc_121.start_line, loc_121.end_page, loc_121.end_line) == (121, 24, 122, 6)

        loc_189 = parse_friedlein_locus("189.190")
        assert (loc_189.start_page, loc_189.end_page, loc_189.start_line) == (189, 190, None)

    def test_hoenen_page_prefix_and_single_page(self) -> None:
        loc_p97 = parse_friedlein_locus("p97")
        assert (loc_p97.start_page, loc_p97.end_page, loc_p97.start_line) == (97, 97, None)
        assert loc_p97.canonical == "Friedlein 97"

        loc_p185 = parse_friedlein_locus("p. 185")
        assert (loc_p185.start_page, loc_p185.end_page) == (185, 185)

        loc_single = parse_friedlein_locus("322")
        assert (loc_single.start_page, loc_single.end_page) == (322, 322)

    def test_invalid_locus_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unrecognized Friedlein locus"):
            parse_friedlein_locus("book-ii-chap-iv")


class TestResolveFriedleinSection:
    """Verify exact Friedlein page-and-line section routing across all seven Codex units."""

    @pytest.mark.parametrize(
        ("page", "line", "expected_unit", "expected_section"),
        [
            (4, 5, "prologue-1", "sec-prol1-metaxy"),
            (13, 10, "prologue-1", "sec-prol1-dianoia-abstraction"),
            (38, 12, "prologue-1", "sec-prol1-geminus-classification"),
            (52, 20, "prologue-2", "sec-prol2-matter-phantasia"),
            (65, 15, "prologue-2", "sec-prol2-eudemian-summary"),
            (97, 7, "definitions", "sec-def-02"),
            (121, 24, "definitions", "sec-def-08-09"),
            (176, 5, "definitions", "sec-def-23"),
            (185, 10, "postulates-axioms", "sec-post-1-3"),
            (191, 21, "postulates-axioms", "sec-post-5"),
            (203, 5, "postulates-axioms", "sec-six-parts"),
            (214, 18, "propositions-1-15", "sec-prop-01"),
            (249, 20, "propositions-1-15", "sec-prop-05"),
            (283, 7, "propositions-1-15", "sec-prop-11-12"),
            (305, 10, "propositions-1-15", "sec-prop-13-15"),
            (305, 20, "propositions-16-32", "sec-prop-16-17"),
            (322, 10, "propositions-16-32", "sec-prop-20-21"),
            (352, 14, "propositions-16-32", "sec-prop-26"),
            (365, 7, "propositions-16-32", "sec-prop-29"),
            (379, 2, "propositions-16-32", "sec-prop-32"),
            (384, 24, "propositions-33-48", "sec-prop-33-34"),
            (395, 13, "propositions-33-48", "sec-prop-35"),
            (419, 15, "propositions-33-48", "sec-prop-44-45"),
            (426, 6, "propositions-33-48", "sec-prop-47"),
            (432, 10, "propositions-33-48", "sec-prop-48"),
        ],
    )
    def test_landmark_loci_resolve_to_expected_sections(
        self,
        page: int,
        line: int,
        expected_unit: str,
        expected_section: str,
    ) -> None:
        sec = resolve_friedlein_section(page, line)
        assert sec.unit_slug == expected_unit
        assert sec.section_id == expected_section

    def test_every_friedlein_page_1_to_436_resolves(self) -> None:
        assert len(CODEX_UNITS) == 7
        assert len(FRIEDLEIN_SECTIONS) >= 45
        for page in range(1, 437):
            sec = resolve_friedlein_section(page)
            assert sec.start_page <= page <= sec.end_page

    def test_out_of_bounds_pages_raise_value_error(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            resolve_friedlein_section(0)
        with pytest.raises(ValueError, match="out of range"):
            resolve_friedlein_section(437)


class TestConcordanceAndSourcesVerification:
    """Verify primary source checksums and 100% concordance coverage of euclid & hoenen."""

    def test_verify_concordance_reports_valid_and_complete(self) -> None:
        report = verify_concordance()
        assert report["valid"] is True, f"Concordance errors: {report['errors']}"
        assert report["errors"] == []
        assert report["source_count"] == 7
        assert report["euclid_keys_covered"] == 156
        assert report["hoenen_keys_covered"] == 4
        assert report["entry_count"] >= 160

    def test_sources_manifest_and_concordance_metadata(self) -> None:
        manifest = load_sources_manifest()
        assert len(manifest["sources"]) == 7
        ids = {s["id"] for s in manifest["sources"]}
        assert ids == {
            "friedlein-1873-teubner-grc",
            "friedlein-1873-page-numbers",
            "friedlein-1873-wikisource-prologue-1",
            "friedlein-1873-wikisource-prologue-2",
            "friedlein-1873-wikisource-definitions",
            "taylor-1792-vol1-en",
            "taylor-1792-vol2-en",
        }

        conc = load_concordance()
        meta = conc["metadata"]
        assert meta["euclid_distinct_keys"] == 156
        assert meta["euclid_total_occurrences"] == 159
        assert meta["hoenen_distinct_keys"] == 4
        assert meta["hoenen_total_loci"] == 10
