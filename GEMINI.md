# GEOMETOR • proclus

Critical digital reconstruction, **4-track Book Codex** (**English**, **Greek (1873)**, **Summary**, **Notes**), and bidirectional **Friedlein (1873) Citation Concordance** for **Proclus Diadochus's** *In Primum Euclidis Elementorum Librum Commentarii* (*Commentary on the First Book of Euclid's Elements*, c. 470 AD).

## Architectural Scope & Editorial Boundaries

- **100% Authentic Public-Domain Primary Sources (`resources/in_euclidem/sources/`)**:
  - **Greek Critical Text**: Gottfried Friedlein, *Procli Diadochi in primum Euclidis Elementorum librum commentarii* (Leipzig: B. G. Teubner, 1873, pp. 1–436; CTS `urn:cts:greekLit:tlg4036.tlg011.opp-grc1`), pairing human-proofread Unicode polytonic Greek (`el.wikisource.org`, pp. 3–177) with exact 1-to-1 Teubner page alignment (`friedlein_1873_teubner_djvu.txt`, pp. 178–436).
  - **Historical English Translation**: Thomas Taylor, *The Philosophical and Mathematical Commentaries of Proclus on the First Book of Euclid's Elements*, Vols. I–II (London, 1788–1789 / 1792; Project Gutenberg `#74253` and `#79455`).
  - **Copyright Discipline**: Never incorporate copyrighted modern translations (such as Glenn R. Morrow's 1970 Princeton translation). All modern terminological notes and structural summaries in `-summary.rst` and `-notes.rst` are written directly from Friedlein's 1873 Greek text.
- **Zero Embedded Construction Code**:
  - Like `geometor/euclid` and `geometor/hoenen`, `docsrc/in_euclidem/` is strictly a historical, philological, and philosophical Book Codex—it contains **zero executable Python construction scripts** (`geometor.model` / `geometor.explorer` code belongs downstream in `geometor/elements`).
- **Self-Contained Runtime Integration with `photon-platform/publish`**:
  - `src/geometor/proclus/sphinx_ext.py` registers the `el` (`"Greek (1873)"`) companion track in `photon_platform.publish.book` at Sphinx runtime and binds local `docs/objects.inv` inventories for `euclid`, `elements`, and `hoenen` without modifying `photon-platform/publish`.

## Key Modules & Apparatus Registries

- `src/geometor/proclus/concordance.py`: Defines the 7 `CODEX_UNITS` and 49 fine-grained `FRIEDLEIN_SECTIONS` (pp. 1–436), parses all Teubner/Heath/Hoenen locus notations (`parse_friedlein_locus`, `resolve_friedlein_section`), and verifies primary-source SHA-256 checksums plus 100% coverage of `euclid` and `hoenen` (`verify_concordance`).
- `src/geometor/proclus/compile_codex.py`: Deterministically compiles `concordance.rst`, `bibliography.rst`, `persons.rst`, and `glossary.rst` from JSON registries and verifies all 28 synchronized chapter track files (`verify_codex_tracks`).
- `src/geometor/proclus/sphinx_ext.py`: Runtime Sphinx hook (`register_greek_book_track`, `configure_local_intersphinx`).
- `src/geometor/proclus/cli.py`: `geometor-proclus` CLI (`summary`, `verify`, `compile-apparatus`).
- `resources/in_euclidem/`:
  - `sources_manifest.json`: Provenance metadata and SHA-256 hashes for all 7 primary source files.
  - `concordance.json`: **164 canonical Friedlein loci** covering **156/156** `euclid` `proclus:in-euclid:*` citation keys (159 occurrences) and **4/4** `hoenen` keys (10 explicit loci).
  - `citations.json` (22 bibliographic works), `persons.json` (54 prosopographical entries, mirrored to `resources/persons.json`), and `glossary.json` (44 Greek/Latin/English technical terms, mirrored to `resources/glossary.json`).

## Development Commands

```bash
# Verify primary sources, SHA-256 hashes, concordance coverage, and Codex tracks
pytest
ruff check src tests

# Regenerate apparatus RST pages from resources/in_euclidem/*.json
python3 -m geometor.proclus.cli compile-apparatus

# Build Sphinx Book Codex HTML documentation into docs/
publish build
```
