=========
changelog
=========

:project: geometor.proclus

0.1.1 (2026-11-13)
------------------

* Resolve 100% of marginal ``.. folio::`` source links (494 directives + 28 badges) to Friedlein (1873) Teubner Greek primary witness line anchors via ``publish folio-links``.

0.1.0 (2026-11-11)
------------------

**added**

- **Primary Public-Domain Source Archive (``resources/in_euclidem/sources/``)**:
  - Archived Gottfried Friedlein's 1873 B. G. Teubner critical Greek edition (*Procli Diadochi in primum Euclidis Elementorum librum commentarii*, CTS ``urn:cts:greekLit:tlg4036.tlg011.opp-grc1``), pairing human-proofread Unicode polytonic Greek for Prologue I, Prologue II, and Definitions (pp. 3–177) with 1-to-1 Teubner page alignment for Postulates, Axioms, and Propositions I.1–I.48 (pp. 178–436).
  - Archived Thomas Taylor's historical two-volume English translation (*The Philosophical and Mathematical Commentaries of Proclus on the First Book of Euclid's Elements*, London, 1788–1789 / 1792, Project Gutenberg ``#74253`` and ``#79455``), correcting three 18th-century Roman-numeral heading misprints in Vol. II (Props. XXI, XXVI, and XLVIII).
  - Verified all seven primary source files with SHA-256 checksums in ``resources/in_euclidem/sources_manifest.json``.
- **4-Track Multi-Track Book Codex (``docsrc/in_euclidem/``)**:
  - Built 7 canonical units × 4 synchronized tracks = 28 chapter track files (**English**, **Greek (1873)**, **Summary**, and **Notes**) with marginal ``.. folio::`` Friedlein page milestones and runtime ``Greek (1873)`` track registration for ``photon-platform/publish``.
- **Bidirectional Friedlein (1873) Citation Concordance (``concordance.py``, ``concordance.json``, ``concordance.rst``)**:
  - Mapped **164 canonical Friedlein loci** covering 100% of ``proclus:in-euclid:*`` citations in ``geometor/euclid`` (156 distinct keys, 159 occurrences across Heath Vols. I–III) and ``geometor/hoenen`` (4 ``citations.json`` keys, 10 explicit philosophical-epistemological loci across *De Noetica Geometriae*).
- **Scholarly Apparatus & CLI**:
  - Compiled ``bibliography.rst`` (22 sources), ``persons.rst`` (54 geometers, philosophers, and editors including all 23 geometers of the Eudemian Summary), and ``glossary.rst`` (44 Greek/Latin/English technical terms).
  - Added ``geometor-proclus`` CLI (``summary``, ``verify``, ``compile-apparatus``) and test suite.
