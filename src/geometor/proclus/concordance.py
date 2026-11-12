"""Friedlein (1873) page-and-line concordance and section resolver for Proclus."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CodexUnitSpec:
    """Canonical unit in the Multi-Track Book Codex (`docsrc/in_euclidem/`)."""

    slug: str
    number_label: str
    title: str
    subtitle: str
    friedlein_start: int
    friedlein_end: int
    taylor_book: str


@dataclass(frozen=True)
class SectionSpec:
    """Fine-grained section within Proclus's Commentary mapped by Friedlein page/line."""

    unit_slug: str
    section_id: str
    title: str
    start_page: int
    start_line: int
    end_page: int
    end_line: int
    euclid_element: str | None = None


@dataclass(frozen=True)
class FriedleinLocus:
    """Normalized representation of a Friedlein (1873) page-and-line citation."""

    raw: str
    start_page: int
    start_line: int | None
    end_page: int
    end_line: int | None
    canonical: str


CODEX_UNITS: tuple[CodexUnitSpec, ...] = (
    CodexUnitSpec(
        slug="prologue-1",
        number_label="Prologue I",
        title="Prologue Part I: Mathematical Being & Common Science",
        subtitle=(
            "Intermediate Being (Metaxy), Limit & Unlimited, Common Mathematical "
            "Principles, Critique of Abstraction, and the Ascent to Dialectic"
        ),
        friedlein_start=3,
        friedlein_end=47,
        taylor_book="Book I (Chaps. I–XV)",
    ),
    CodexUnitSpec(
        slug="prologue-2",
        number_label="Prologue II",
        title="Prologue Part II: Philosophy & History of Geometry",
        subtitle=(
            "Mathematical Imagination (Phantasia & Probole), Intelligible Matter, "
            "The Eudemian Summary of Greek Geometry, and the Purpose of the Elements"
        ),
        friedlein_start=48,
        friedlein_end=84,
        taylor_book="Book II (Chaps. I–IX)",
    ),
    CodexUnitSpec(
        slug="definitions",
        number_label="Definitions",
        title="Commentary on the Definitions (I.Def.1–23)",
        subtitle=(
            "Point, Line & Flux, Straight Line, Surface, Plane & Horn Angles, "
            "Figure, Circle, Triangles, Quadrilaterals, and Parallel Lines"
        ),
        friedlein_start=85,
        friedlein_end=177,
        taylor_book="Book II (Definitions I–XXXV)",
    ),
    CodexUnitSpec(
        slug="postulates-axioms",
        number_label="Postulates & Axioms",
        title="Hypotheses, Postulates, Axioms & Propositional Form",
        subtitle=(
            "Epistemology of First Principles, Compass & Straightedge Postulates, "
            "Critique of Postulate 5, Common Notions, and the Six Parts of a Proposition"
        ),
        friedlein_start=178,
        friedlein_end=207,
        taylor_book="Book III (Petitions, Axioms & Prop. I Prefatory Sections)",
    ),
    CodexUnitSpec(
        slug="propositions-1-15",
        number_label="Propositions I.1–I.15",
        title="Commentary on Propositions I.1–I.15: Triangles, Congruence & Perpendiculars",
        subtitle=(
            "Equilateral Construction & Zeno's Critique, Superposition (I.4), Pappus's Proof "
            "of I.5, Converses & Reductio, Oenopides' Gnomon (I.12), Vertical Angles & Porisms"
        ),
        friedlein_start=208,
        friedlein_end=305,
        taylor_book="Book III (Propositions I–XV & Porisms)",
    ),
    CodexUnitSpec(
        slug="propositions-16-32",
        number_label="Propositions I.16–I.32",
        title="Commentary on Propositions I.16–I.32: Inequalities, Parallels & Angle-Sum",
        subtitle=(
            "Exterior Angle, Epicurean Critique of I.20, Thales' Ship-Distance Theorem (I.26), "
            "Ptolemy & Proclus on Postulate 5 (I.29), and the Pythagorean Angle-Sum Proof (I.32)"
        ),
        friedlein_start=305,
        friedlein_end=384,
        taylor_book="Book III (Props. XVI–XXVI) & Book IV (Props. XXVII–XXXII)",
    ),
    CodexUnitSpec(
        slug="propositions-33-48",
        number_label="Propositions I.33–I.48",
        title="Commentary on Propositions I.33–I.48: Areas, Application & Pythagoras",
        subtitle=(
            "Parallelograms & Locus Theorems (I.35), Pythagorean Application of Areas "
            "(Parabole, Hyperbole, Elleipsis, I.44), and Euclid's Proof of I.47–I.48"
        ),
        friedlein_start=384,
        friedlein_end=436,
        taylor_book="Book IV (Propositions XXXIII–XLVIII)",
    ),
)

CODEX_UNITS_BY_SLUG: dict[str, CodexUnitSpec] = {u.slug: u for u in CODEX_UNITS}

# Ordered section map covering Friedlein pp. 1–436 with exact line boundaries.
FRIEDLEIN_SECTIONS: tuple[SectionSpec, ...] = (
    # Prologue Part I (pp. 3–47)
    SectionSpec("prologue-1", "sec-prol1-metaxy", "Chap. I: Intermediate Mathematical Essence (Metaxy)", 1, 1, 5, 10),
    SectionSpec("prologue-1", "sec-prol1-peras-apeiron", "Chap. II: Limit (Peras) and the Unlimited (Apeiron)", 5, 11, 7, 12),
    SectionSpec("prologue-1", "sec-prol1-common-theorems", "Chap. III–IV: Common Theorems Pervading All Mathematics", 7, 13, 11, 25),
    SectionSpec("prologue-1", "sec-prol1-dianoia-abstraction", "Chap. V–VI: Dianoia, Innate Logoî, and Critique of Abstraction", 11, 26, 19, 19),
    SectionSpec("prologue-1", "sec-prol1-utility-ascent", "Chap. VII–X: Platonic Utility of Mathematics & Reply to Critics", 19, 20, 32, 20),
    SectionSpec("prologue-1", "sec-prol1-criteria-division", "Chap. XI–XIII: Criteria of Mathematics & Pythagorean Quadrivium", 32, 21, 37, 26),
    SectionSpec("prologue-1", "sec-prol1-geminus-classification", "Chap. XIII (cont.): Geminus's Classification of Pure & Mixed Sciences", 38, 1, 42, 8),
    SectionSpec("prologue-1", "sec-prol1-dialectic", "Chap. XIV–XV: Dialectic as Unifying Capstone & Name of Mathesis", 42, 9, 47, 28),
    # Prologue Part II (pp. 48–84)
    SectionSpec("prologue-2", "sec-prol2-matter-phantasia", "Chap. I–II: Intelligible Matter, Sensible Inexactitude & Phantasia", 48, 1, 57, 8),
    SectionSpec("prologue-2", "sec-prol2-probole-cosmos", "Chap. III: Projection (Probole) & Cosmic Geometry", 57, 9, 64, 6),
    SectionSpec("prologue-2", "sec-prol2-eudemian-summary", "Chap. IV: Origin of Geometry & The Eudemian Summary (Thales to Euclid)", 64, 7, 70, 18),
    SectionSpec("prologue-2", "sec-prol2-stoicheiosis", "Chap. V–VII: Purpose of Book I & Meaning of Element (Stoicheion)", 70, 19, 75, 4),
    SectionSpec("prologue-2", "sec-prol2-method-principles", "Chap. VIII–IX: Organization of First Principles, Problems & Theorems", 75, 5, 84, 25),
    # Definitions (pp. 85–177)
    SectionSpec("definitions", "sec-def-01", "Def. 1: Point (Semeion) as Indivisible Limit with Position", 85, 1, 96, 15, "I.def.1"),
    SectionSpec("definitions", "sec-def-02", "Def. 2: Line (Gramme), Flux of a Point & Classification of Curves", 96, 16, 103, 20, "I.def.2"),
    SectionSpec("definitions", "sec-def-03", "Def. 3: Extremities of a Line & Homoeomeric Lines", 103, 21, 109, 3, "I.def.3"),
    SectionSpec("definitions", "sec-def-04", "Def. 4: Straight Line (Eutheia) & Spiric/Conic Classifications", 109, 4, 113, 5, "I.def.4"),
    SectionSpec("definitions", "sec-def-05-07", "Defs. 5–7: Surface (Epiphaneia), Boundaries & Plane Surface", 113, 6, 121, 11, "I.def.7"),
    SectionSpec("definitions", "sec-def-08-09", "Defs. 8–9: Plane Angle, Category of Angle & Horn Angles (Keratoeides)", 121, 12, 131, 12, "I.def.8"),
    SectionSpec("definitions", "sec-def-10-12", "Defs. 10–12: Right Angle, Perpendicular, Obtuse & Acute Angles", 131, 13, 136, 17, "I.def.10"),
    SectionSpec("definitions", "sec-def-13-14", "Defs. 13–14: Boundary (Horos), Figure (Schema) & Protagoras on Tangency", 136, 18, 146, 23, "I.def.14"),
    SectionSpec("definitions", "sec-def-15-18", "Defs. 15–18: Circle, Center, Diameter (Thales) & Semicircle", 146, 24, 159, 6, "I.def.15"),
    SectionSpec("definitions", "sec-def-19-21", "Defs. 19–21: Rectilinear Figures & Sevenfold Species of Triangles", 159, 7, 168, 25, "I.def.20"),
    SectionSpec("definitions", "sec-def-22", "Def. 22: Quadrilaterals (Square, Oblong, Rhombus, Rhomboid, Trapezia)", 169, 1, 175, 1, "I.def.22"),
    SectionSpec("definitions", "sec-def-23", "Def. 23: Parallel Straight Lines (Euclid, Posidonius & Geminus)", 175, 2, 177, 25, "I.def.23"),
    # Postulates, Axioms & Formal Structure of Propositions (pp. 178–207)
    SectionSpec("postulates-axioms", "sec-post-epistemology", "Distinction of Hypotheses, Postulates & Axioms", 178, 1, 184, 29),
    SectionSpec("postulates-axioms", "sec-post-1-3", "Postulates 1–3: Straightedge & Compass Constructibility (Geminus)", 185, 1, 187, 27, "I.post.1"),
    SectionSpec("postulates-axioms", "sec-post-4", "Postulate 4: Equality of All Right Angles", 188, 1, 191, 15, "I.post.4"),
    SectionSpec("postulates-axioms", "sec-post-5", "Postulate 5: The Parallel Postulate & Asymptotic Curves", 191, 16, 193, 9, "I.post.5"),
    SectionSpec("postulates-axioms", "sec-axioms", "Common Notions (Axioms 1–5): Apollonius, Heron & Pappus", 193, 10, 198, 15, "I.cn.1"),
    SectionSpec("postulates-axioms", "sec-six-parts", "Problems vs. Theorems & The Six Canonical Parts of a Proposition", 199, 1, 207, 25),
    # Propositions I.1–I.15 & Excursus on Porisms (pp. 208–305, l. 16)
    SectionSpec("propositions-1-15", "sec-prop-01", "Prop. I.1: Equilateral Triangle, Cases & Zeno of Sidon's Objection", 208, 1, 219, 24, "I.1"),
    SectionSpec("propositions-1-15", "sec-prop-02-03", "Props. I.2–I.3: Transferring & Subtracting Segments", 220, 1, 232, 26, "I.2"),
    SectionSpec("propositions-1-15", "sec-prop-04", "Prop. I.4: First Congruence Theorem (SAS), Superposition & Carpus", 233, 1, 243, 25, "I.4"),
    SectionSpec("propositions-1-15", "sec-prop-05", "Prop. I.5: Isosceles Base Angles (Thales & Pappus's Symmetry Proof)", 244, 1, 251, 18, "I.5"),
    SectionSpec("propositions-1-15", "sec-prop-06", "Prop. I.6: Converse of I.5, Conversion Theory & Reductio ad Absurdum", 251, 19, 258, 11, "I.6"),
    SectionSpec("propositions-1-15", "sec-prop-07-08", "Props. I.7–I.8: Rigidity Lemma & SSS Congruence (Philo's Proof)", 258, 12, 269, 26, "I.8"),
    SectionSpec("propositions-1-15", "sec-prop-09-10", "Props. I.9–I.10: Angle & Line Bisection, Trisection & Indivisible Lines", 270, 1, 280, 4, "I.9"),
    SectionSpec("propositions-1-15", "sec-prop-11-12", "Props. I.11–I.12: Perpendiculars, Apollonius & Oenopides' Gnomon", 280, 5, 289, 25, "I.12"),
    SectionSpec("propositions-1-15", "sec-prop-13-15", "Props. I.13–I.15: Adjacent & Vertical Angles (Thales) & Porisms", 290, 1, 305, 16, "I.15"),
    # Propositions I.16–I.32 (pp. 305, l. 17 – 384, l. 21)
    SectionSpec("propositions-16-32", "sec-prop-16-17", "Props. I.16–I.17: Exterior Angle & Sum of Two Interior Angles", 305, 17, 312, 25, "I.16"),
    SectionSpec("propositions-16-32", "sec-prop-18-19", "Props. I.18–I.19: Greater Side & Greater Angle (Division Proof)", 313, 1, 321, 26, "I.18"),
    SectionSpec("propositions-16-32", "sec-prop-20-21", "Props. I.20–I.21: Triangle Inequality (Epicurean Critique, Heron, Porphyry)", 322, 1, 329, 26, "I.20"),
    SectionSpec("propositions-16-32", "sec-prop-22-23", "Props. I.22–I.23: Triangle Diorismos & Copying an Angle (Oenopides)", 330, 1, 335, 26, "I.23"),
    SectionSpec("propositions-16-32", "sec-prop-24-25", "Props. I.24–I.25: Hinge Theorems (Heron, Porphyry & Menelaus)", 336, 1, 347, 19, "I.24"),
    SectionSpec("propositions-16-32", "sec-prop-26", "Prop. I.26: ASA/AAS Congruence & Thales' Ship-Distance Theorem", 347, 20, 353, 26, "I.26"),
    SectionSpec("propositions-16-32", "sec-prop-27-28", "Props. I.27–I.28: Book IV Opening & Sufficient Conditions for Parallels", 354, 1, 364, 18, "I.27"),
    SectionSpec("propositions-16-32", "sec-prop-29", "Prop. I.29: Ptolemy's Treatise & Proclus's Attempted Proof of Postulate 5", 364, 19, 373, 4, "I.29"),
    SectionSpec("propositions-16-32", "sec-prop-30-31", "Props. I.30–I.31: Transitivity & Construction of Parallels", 373, 5, 376, 12, "I.30"),
    SectionSpec("propositions-16-32", "sec-prop-32", "Prop. I.32: Triangle Angle-Sum, Pythagorean Proof & Polygon Formula", 376, 13, 384, 21, "I.32"),
    # Propositions I.33–I.48 (pp. 384, l. 22 – 436)
    SectionSpec("propositions-33-48", "sec-prop-33-34", "Props. I.33–I.34: Parallelogrammic Areas & Diameter Bisection", 384, 22, 393, 28, "I.34"),
    SectionSpec("propositions-33-48", "sec-prop-35", "Prop. I.35: Equal Parallelograms & Birth of Locus Theorems", 394, 1, 400, 24, "I.35"),
    SectionSpec("propositions-33-48", "sec-prop-36-41", "Props. I.36–I.41: Equal Parallelograms & Triangles Between Parallels", 400, 25, 415, 16, "I.41"),
    SectionSpec("propositions-33-48", "sec-prop-42-43", "Props. I.42–I.43: Area Construction & Complements About the Diameter", 415, 17, 418, 28, "I.43"),
    SectionSpec("propositions-33-48", "sec-prop-44-45", "Props. I.44–I.45: Pythagorean Application of Areas (Parabole, Hyperbole, Elleipsis)", 419, 1, 423, 10, "I.44"),
    SectionSpec("propositions-33-48", "sec-prop-46", "Prop. I.46: Constructing the Square & Posidonius's Definition", 423, 11, 425, 25, "I.46"),
    SectionSpec("propositions-33-48", "sec-prop-47", "Prop. I.47: The Theorem of Pythagoras, Euclid's Generalization & Triples", 426, 1, 429, 28, "I.47"),
    SectionSpec("propositions-33-48", "sec-prop-48", "Prop. I.48: Converse of Pythagoras, Peroration & Manuscript Scholium", 430, 1, 436, 28, "I.48"),
)

# Explicit overrides for idiosyncratic key encodings in Heath's citations.json / Hoenen's citations.json
_EXPLICIT_LOCUS_OVERRIDES: dict[str, tuple[int, int | None, int, int | None]] = {
    "65-20": (65, 20, 65, 20),
    "67-6": (67, 6, 67, 6),
    "121-24-122-6": (121, 24, 122, 6),
    "189.190": (189, None, 190, None),
    "303-6": (303, 6, 303, 6),
    "304-2": (304, 2, 304, 2),
}


def format_canonical_locus(
    start_page: int,
    start_line: int | None,
    end_page: int,
    end_line: int | None,
) -> str:
    """Format a normalized Friedlein citation string."""
    if start_page == end_page:
        if start_line is None and end_line is None:
            return f"Friedlein {start_page}"
        if start_line == end_line or end_line is None:
            return f"Friedlein {start_page}, {start_line}"
        return f"Friedlein {start_page}, {start_line}–{end_line}"
    if start_line is None and end_line is None:
        return f"Friedlein {start_page}–{end_page}"
    return f"Friedlein {start_page}, {start_line}–{end_page}, {end_line}"


def parse_friedlein_locus(locus: str, display_hint: str = "") -> FriedleinLocus:
    """Parse a Friedlein (1873) page/line locus key into structured page and line bounds.

    Handles standard Teubner citations (``"12.14-22"``, ``"103.21-107.10"``),
    whole-page ranges (``"64-70"``, ``"399-400"``), compressed trailing-digit
    page ranges (``"303-4"``, ``"323-6"``, ``"424-5"``), and Hoenen/Heath
    shorthand keys (``"p97"``, ``"p185"``, ``"65-20"``, ``"189.190"``).
    """
    cleaned = locus.strip()
    if cleaned in _EXPLICIT_LOCUS_OVERRIDES:
        sp, sl, ep, el = _EXPLICIT_LOCUS_OVERRIDES[cleaned]
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=sl,
            end_page=ep,
            end_line=el,
            canonical=format_canonical_locus(sp, sl, ep, el),
        )

    # Strip leading 'p' or 'p.' (e.g. 'p97', 'p185')
    s = re.sub(r"^p\.?\s*", "", cleaned, flags=re.IGNORECASE)
    # Normalize unicode dashes and comma-spaces
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r",\s*", ".", s)

    # Pattern 1: p1.l1-p2.l2 (e.g. 103.21-107.10)
    m = re.fullmatch(r"(\d+)\.(\d+)-(\d+)\.(\d+)", s)
    if m:
        sp, sl, ep, el = (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=sl,
            end_page=ep,
            end_line=el,
            canonical=format_canonical_locus(sp, sl, ep, el),
        )

    # Pattern 2: p1.l1-l2 (same page line range, e.g. 12.14-22, 379.2-15)
    m = re.fullmatch(r"(\d+)\.(\d+)-(\d+)", s)
    if m:
        sp, sl, el = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=sl,
            end_page=sp,
            end_line=el,
            canonical=format_canonical_locus(sp, sl, sp, el),
        )

    # Pattern 3: p1.l1 (single page + line, e.g. 68.20, 426.6)
    m = re.fullmatch(r"(\d+)\.(\d+)", s)
    if m:
        sp, sl = int(m.group(1)), int(m.group(2))
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=sl,
            end_page=sp,
            end_line=sl,
            canonical=format_canonical_locus(sp, sl, sp, sl),
        )

    # Pattern 4: p1-p2 (page range or compressed page range, e.g. 64-70, 303-4, 323-6)
    m = re.fullmatch(r"(\d+)-(\d+)", s)
    if m:
        sp, second = int(m.group(1)), int(m.group(2))
        hint = display_hint.strip()
        if second < sp:
            # Check display_hint if singular 'p. X, Y'
            if re.search(rf"\bp\.\s*{sp}\s*,\s*{second}\b", hint):
                return FriedleinLocus(
                    raw=locus,
                    start_page=sp,
                    start_line=second,
                    end_page=sp,
                    end_line=second,
                    canonical=format_canonical_locus(sp, second, sp, second),
                )
            # Expand compressed trailing digits: e.g. 303-4 -> 303-304
            mod = 10 ** len(m.group(2))
            ep = (sp // mod) * mod + second
            if ep < sp:
                ep += mod
        else:
            ep = second
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=None,
            end_page=ep,
            end_line=None,
            canonical=format_canonical_locus(sp, None, ep, None),
        )

    # Pattern 5: single page integer (e.g. 269, 322, 351, 393)
    m = re.fullmatch(r"(\d+)", s)
    if m:
        sp = int(m.group(1))
        return FriedleinLocus(
            raw=locus,
            start_page=sp,
            start_line=None,
            end_page=sp,
            end_line=None,
            canonical=format_canonical_locus(sp, None, sp, None),
        )

    raise ValueError(f"Unrecognized Friedlein locus format: {locus!r}")


def resolve_friedlein_section(page: int, line: int | None = None) -> SectionSpec:
    """Resolve a Friedlein (1873) page and optional line number to its Codex section."""
    if page < 1 or page > 436:
        raise ValueError(f"Friedlein commentary page {page} out of range (1..436)")
    eff_line = line if line is not None else 15
    for sec in FRIEDLEIN_SECTIONS:
        if (page, eff_line) >= (sec.start_page, sec.start_line) and (page, eff_line) <= (
            sec.end_page,
            sec.end_line,
        ):
            return sec
    # Fallback by page containment if line exceeds 28 on a long page
    for sec in FRIEDLEIN_SECTIONS:
        if sec.start_page <= page <= sec.end_page:
            return sec
    raise LookupError(f"No section found for Friedlein p. {page}, l. {line}")


def default_resources_dir() -> Path:
    """Return the default ``resources/in_euclidem`` directory path."""
    return Path(__file__).resolve().parents[3] / "resources" / "in_euclidem"


def load_concordance(path: Path | None = None) -> dict[str, Any]:
    """Load ``concordance.json``."""
    target = path or (default_resources_dir() / "concordance.json")
    return json.loads(target.read_text(encoding="utf-8"))


def load_sources_manifest(path: Path | None = None) -> dict[str, Any]:
    """Load ``sources_manifest.json``."""
    target = path or (default_resources_dir() / "sources_manifest.json")
    return json.loads(target.read_text(encoding="utf-8"))


def verify_concordance(
    concordance_path: Path | None = None,
    manifest_path: Path | None = None,
    euclid_citations_path: Path | None = None,
    hoenen_citations_path: Path | None = None,
) -> dict[str, Any]:
    """Verify concordance integrity, source SHA-256 hashes, and sibling citation coverage."""
    res_dir = default_resources_dir()
    conc = load_concordance(concordance_path)
    manifest = load_sources_manifest(manifest_path)

    errors: list[str] = []

    # 1. Verify primary source files & SHA-256 hashes
    for src in manifest.get("sources", []):
        src_file = res_dir / src["file"]
        if not src_file.is_file():
            errors.append(f"Missing primary source file: {src_file}")
            continue
        actual_sha = hashlib.sha256(src_file.read_bytes()).hexdigest()
        if actual_sha != src.get("sha256"):
            errors.append(
                f"SHA-256 mismatch for {src['id']}: expected {src.get('sha256')}, got {actual_sha}"
            )

    # 2. Verify concordance entries
    entries = conc.get("entries", [])
    if len(entries) < 155:
        errors.append(f"Expected at least 155 concordance entries, found {len(entries)}")

    prev_key = (0, 0)
    indexed_euclid_keys: set[str] = set()
    indexed_hoenen_keys: set[str] = set()

    for entry in entries:
        sp = entry["friedlein_start_page"]
        sl = entry.get("friedlein_start_line") or 0
        ep = entry["friedlein_end_page"]
        unit = entry["codex_unit"]
        if unit not in CODEX_UNITS_BY_SLUG:
            errors.append(f"Invalid codex_unit {unit!r} in entry {entry.get('id')}")
        if sp < 1 or ep > 436 or ep < sp:
            errors.append(f"Invalid page bounds {sp}..{ep} in entry {entry.get('id')}")
        sort_tuple = (sp, sl)
        if sort_tuple < prev_key:
            errors.append(
                f"Entries out of Friedlein page/line order at {entry.get('id')}: {sort_tuple} < {prev_key}"
            )
        prev_key = sort_tuple

        for ec in entry.get("euclid_citations", []):
            indexed_euclid_keys.add(ec["citation_key"])
        for hc in entry.get("hoenen_citations", []):
            if hc.get("citation_key"):
                indexed_hoenen_keys.add(hc["citation_key"])

    # 3. Verify 100% coverage of sibling repos if present on disk
    geometor_root = res_dir.parents[2]
    e_path = euclid_citations_path or (geometor_root / "euclid" / "resources" / "heath" / "citations.json")
    if e_path.is_file():
        e_data = json.loads(e_path.read_text(encoding="utf-8"))
        expected_e = {k for k in e_data if k.startswith("proclus:in-euclid:")}
        missing_e = sorted(expected_e - indexed_euclid_keys)
        if missing_e:
            errors.append(f"Missing Euclid citation keys in concordance: {missing_e}")

    h_path = hoenen_citations_path or (
        geometor_root / "hoenen" / "resources" / "de_noetica_geometriae" / "citations.json"
    )
    if h_path.is_file():
        h_data = json.loads(h_path.read_text(encoding="utf-8"))
        expected_h = {k for k in h_data if k.startswith("proclus:in-euclid:")}
        missing_h = sorted(expected_h - indexed_hoenen_keys)
        if missing_h:
            errors.append(f"Missing Hoenen citation keys in concordance: {missing_h}")

    return {
        "valid": len(errors) == 0,
        "entry_count": len(entries),
        "euclid_keys_covered": len(indexed_euclid_keys),
        "hoenen_keys_covered": len(indexed_hoenen_keys),
        "source_count": len(manifest.get("sources", [])),
        "errors": errors,
    }
