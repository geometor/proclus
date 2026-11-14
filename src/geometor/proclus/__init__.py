"""GEOMETOR Proclus: Multi-Track Book Codex and Friedlein Citation Concordance.

Scholarly digital reconstruction and apparatus for Proclus Diadochus's
*In Primum Euclidis Elementorum Librum Commentarii* (*Commentary on the First
Book of Euclid's Elements*, c. 470 AD), grounded in Gottfried Friedlein's 1873
Teubner Greek edition and Thomas Taylor's 1788–1789/1792 English translation,
and cross-linked with ``geometor/euclid``, ``geometor/elements``, and
``geometor/hoenen``.
"""

from geometor.proclus.concordance import (
    CODEX_UNITS,
    FRIEDLEIN_SECTIONS,
    CodexUnitSpec,
    FriedleinLocus,
    SectionSpec,
    load_concordance,
    load_sources_manifest,
    parse_friedlein_locus,
    resolve_friedlein_section,
    verify_concordance,
)

__version__ = "0.1.2"

__all__ = [
    "CODEX_UNITS",
    "FRIEDLEIN_SECTIONS",
    "CodexUnitSpec",
    "FriedleinLocus",
    "SectionSpec",
    "__version__",
    "load_concordance",
    "load_sources_manifest",
    "parse_friedlein_locus",
    "resolve_friedlein_section",
    "verify_concordance",
]
