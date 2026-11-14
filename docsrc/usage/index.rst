:navigation: header
:order: 20
:nav_title: Usage

.. _proclus-usage:

==================
Using This Edition
==================

.. rubric:: Interactive Reader's Guide to the Digital Scriptorium Edition of Proclus's Commentary on Euclid

Welcome to the GEOMETOR critical edition of **Commentary on the First Book of Euclid's Elements** (*In Primum Euclidis Elementorum Librum Commentarii*). This digital edition is designed for deep mathematical reading, polytonic Greek philology, and axiomatic synthesis across Proclus Diadochus's Neoplatonic philosophy of geometry. Below are the key interactive features available throughout the site.

1. Synchronized Reading Tracks
------------------------------

Every unit in the Book Codex provides up to four synchronized reading tracks accessible directly from the chapter header navigation bar:

* **English (Primary Translation)**: Public-domain translation based on Thomas Taylor's landmark English edition (London, 1788–1789 / 1792), updated and segmented to Gottfried Friedlein's 1873 page milestones with GEOMETOR scholarly apparatus.
* **Greek (Friedlein 1873, ``-el``)**: Verbatim polytonic Greek text from Gottfried Friedlein's standard Teubner critical edition (*Procli Diadochi in primum Euclidis Elementorum librum commentarii*, Leipzig: B. G. Teubner, 1873).
* **Summary (Deductive Architecture)**: Proposition analyses, axiomatic classifications, Eudemian historical sequences, and Neoplatonic epistemological syntheses.
* **Notes (Scholarly Commentary)**: Greek philology, citations across Euclid's *Elements* (:cite:`heath:1926`), Scholastic-noetic reception in Petrus Hoenen S.J.'s *De Noetica Geometriae* (:cite:`hoenen:1954`), and cross-corpus links across the GEOMETOR ecosystem.

Use the track switcher in the chapter header bar to toggle seamlessly between perspectives while preserving your reading position.

2. Primary-Source Folio Milestones
----------------------------------

Every passage is calibrated to primary archival witnesses:

* **Marginal Folio Badges**: Marginal milestone pills (e.g., ``[p. 65]``, ``[p. 125]``, ``[p. 208]``) mark exact page boundaries in Gottfried Friedlein's 1873 Teubner edition.
* **Header Folio Indicator**: The top metadata bar identifies the active unit, Friedlein page span, and canonical locus.
* **Cross-Reference Anchors**: Explicit anchors enable direct deep linking across the GEOMETOR ecosystem.

3. Interactive Diagrams & Deductive Links
-----------------------------------------

The edition features calibrated mathematical plates and deductive links:

* **Geometric Hover Cards (``:g:``)**: Hovering over or clicking a geometric symbol displays coordinate, construction, and definition details.
* **Mathematical Equations (``:eq:``)**: Display formatted LaTeX typography with interactive term explanations.
* **Deductive Justifications (``:just:``)**: Direct cross-references to Euclid's definitions, postulates, axioms, and propositions (e.g., :just:`euclid:I.47`).

4. Full-Text Search with In-Page Highlighting
---------------------------------------------

The global search box in the sidebar provides instantaneous full-text search across all seven commentary units, apparatus tables, and commentary:

* Search queries automatically append `?highlight=` parameters to destination URLs.
* Matched terms are highlighted directly within the chapter body, Greek original, and scholia for immediate discovery.

5. Categories, Tags & Collection Views
--------------------------------------

Document collections throughout the site (such as the :doc:`Development Log <../log/index>`) support rich viewing modes:

* **Cards View**: Grid of entry cards with metadata badges and timestamps.
* **Banners View**: Wide banner layout for extended narrative overviews.
* **List View**: Dense tabular listing for fast scanning.
* **Taxonomy Facets**: Filter by topic tags (e.g., `prologue`, `definitions`, `postulates`, `eudemus`, `phantasia`).

6. People, Bibliography & Glossary Tooltips
-------------------------------------------

* **People (``:person:``)**: Historical figures and geometers (such as :person:`Proclus Lycius Diadochus <proclus>`, :person:`Gottfried Friedlein <friedlein>`, :person:`Thomas Taylor <taylor>`, :person:`Thales <thales>`, :person:`Pythagoras <pythagoras>`, and :person:`Euclid <euclid>`) display rich biographical hover cards linking to the :doc:`People Register <../in_euclidem/persons>`.
* **Citations (``:cite:``)**: Inline citations link to critical editions in the :doc:`Bibliography <../in_euclidem/bibliography>`.
* **Technical Terms (``:term:``)**: Technical Greek, Latin, and English terminology (such as *phantasia*, *metaxy*, *dianoia*, and *horos*) link to entries in the :doc:`Technical Glossary <../in_euclidem/glossary>`.
* **Theme Switching**: Toggle between Light and Dark themes via the header button to suit your reading environment.

7. Command-Line & Python API
----------------------------

The ``geometor-proclus`` CLI and Python package provide tools for concordance analysis, primary source verification, and apparatus management.

CLI Usage:

.. code-block:: bash

   # Display Codex structure and concordance statistics
   geometor-proclus summary

   # Verify primary sources, concordance coverage, and Codex tracks
   geometor-proclus verify

   # Recompile apparatus RST files from JSON registries
   geometor-proclus compile-apparatus

Python API Example:

.. code-block:: python

   from geometor.proclus.concordance import CODEX_UNITS, verify_concordance

   # Inspect all 7 Codex units
   for unit in CODEX_UNITS:
       print(f"{unit.number_label}: Friedlein pp. {unit.friedlein_start}-{unit.friedlein_end} ({unit.title})")

   # Verify 164 canonical Friedlein citation loci
   report = verify_concordance()
   print("Concordance valid:", report["valid"])
   print("Total Friedlein loci:", report["entries_count"])
