GEOMETOR • proclus
==================

.. image:: https://img.shields.io/github/license/geometor/proclus.svg
   :target: https://github.com/geometor/proclus/blob/main/LICENSE

**Digital critical reconstruction, 4-track Book Codex, and Friedlein (1873) Citation Concordance of Proclus Diadochus's Commentary on the First Book of Euclid's Elements (c. 470 AD).**

Overview
--------

``geometor.proclus`` brings **Proclus Lycius Diadochus's** *In Primum Euclidis Elementorum Librum Commentarii* (*Πρόκλου Διαδόχου Εἰς τὸ πρῶτον τῶν Εὐκλείδου Στοιχείων*) into the **GEOMETOR** classical canon as a de-paginated, semantically cross-referenced **4-track Book Codex** powered by `photon-platform/publish <https://github.com/photon-platform/publish>`_.

Standing at the philosophical, historical, and logical crossroads of Greek mathematics, Proclus's *Commentary* is the single richest ancient companion to Euclid's *Elements*:

- **History of Pre-Euclidean Geometry**: Preserves **Eudemus of Rhodes's** otherwise lost *History of Geometry* (**The Eudemian Summary**, *Friedlein* pp. 64–70), recording twenty-three foundational geometers from **Thales** and **Pythagoras** to **Eudoxus**, **Menaechmus**, and **Euclid**.
- **Epistemology of Mathematical Imagination**: Formulates the theory of **mathematical intermediate being** (*τὸ μεταξύ*), **discursive reason** (*διάνοια*), and **projection** (*προβολή*) into the passive intellect / **imagination** (*φαντασία*, *Friedlein* pp. 51–56)—the historical fountainhead of **Peter Hoenen's** inquiry in `geometor/hoenen <https://github.com/geometor/hoenen>`_.
- **Axiomatics & Formal Proof Structure**: Codifies the classical distinction between **hypotheses, postulates, and axioms** (*Friedlein* pp. 178–198), preserves **Ptolemy's** and **Proclus's** critiques of **Postulate 5** (*Friedlein* pp. 191–193, 365–373), and defines the **Six Canonical Parts of a Proposition** (*πρότασις*, *ἔκθεσις*, *διορισμός*, *κατασκευή*, *ἀπόδειξις*, *συμπέρασμα*, *Friedlein* pp. 203–207).
- **Critical Bridge Across GEOMETOR**: Provides bidirectional resolution for all **156** distinct ``proclus:in-euclid:*`` citation keys (159 occurrences) across Sir Thomas L. Heath's *Elements* in `geometor/euclid <https://github.com/geometor/euclid>`_ and all **10** explicit Friedlein loci in `geometor/hoenen <https://github.com/geometor/hoenen>`_.

Primary Public-Domain Sources
-----------------------------

All primary texts in ``resources/in_euclidem/sources/`` are 100% authentic public-domain witnesses verified by SHA-256 checksums in ``resources/in_euclidem/sources_manifest.json``:

1. **Critical Greek Edition — Gottfried Friedlein (Leipzig: B. G. Teubner, 1873)**:
   *Procli Diadochi in primum Euclidis Elementorum librum commentarii* (pp. 1–436, CTS ``urn:cts:greekLit:tlg4036.tlg011.opp-grc1``), combining human-proofread Unicode polytonic Greek from Greek Wikisource (pp. 3–177) with exact 1-to-1 Teubner page alignment from the Open Greek and Latin 600-PPI Greek source (pp. 178–436).
2. **Historical English Translation — Thomas Taylor (London, 1788–1789 / 1792)**:
   *The Philosophical and Mathematical Commentaries of Proclus on the First Book of Euclid's Elements*, Volumes I & II (Project Gutenberg ``#74253`` and ``#79455``).
3. **GEOMETOR Scholarly Apparatus**:
   Original structural summaries, philological notes, and cross-repository commentary composed directly from Friedlein's 1873 Greek text with zero copyrighted modern translations and **zero embedded Python construction scripts** inside the historical treatise.

4-Track Book Codex Structure
----------------------------

Each of the seven canonical divisions of ``docsrc/in_euclidem/`` is published across four synchronized tracks in the sticky ``:layout: book`` header (**English** · **Greek (1873)** · **Summary** · **Notes**):

1. **Prologue Part I** (``prologue-1``, *Friedlein* pp. 3–47): Intermediate Mathematical Being (*Metaxy*), Limit & Unlimited, Common Mathematical Science, *Dianoia* vs. Abstraction, Geminus's Classification, and Dialectic.
2. **Prologue Part II** (``prologue-2``, *Friedlein* pp. 48–84): Intelligible Matter, *Phantasia* & *Probole*, **The Eudemian Summary** (pp. 64–70), and the Meaning of *Stoicheion*.
3. **Definitions** (``definitions``, *Friedlein* pp. 85–177): Commentary on ``I.Def.1–23`` (Point, Flux of a Point, Homoeomeric Curves, Horn Angles, Circle, Seven Triangle Species, Quadrilaterals, and Parallels).
4. **Postulates, Axioms & Six Parts** (``postulates-axioms``, *Friedlein* pp. 178–207): Epistemology of First Principles, Geminus on Postulate 1, Critique of Postulate 5, Common Notions, and the **Six Canonical Parts of a Proposition** (pp. 203–207).
5. **Propositions I.1–I.15** (``propositions-1-15``, *Friedlein* pp. 208–305): Equilateral Triangle & Zeno of Sidon's Critique, Superposition (I.4), Pappus's Symmetry Proof of I.5, Conversion & *Reductio* (I.6), Philo's Proof of I.8, Oenopides' *Gnomon* (I.12), and Excursus on Porisms.
6. **Propositions I.16–I.32** (``propositions-16-32``, *Friedlein* pp. 305–384): Exterior Angle & Inequalities, Epicurean Critique of I.20, Thales' Ship-Distance Theorem (I.26), Ptolemy & Proclus on Postulate 5 (I.29, pp. 365–373), and Eudemus's Pythagorean Angle-Sum Proof (I.32, p. 379).
7. **Propositions I.33–I.48** (``propositions-33-48``, *Friedlein* pp. 384–436): Equal Parallelograms & Locus Theorems (I.35), Pythagorean Application of Areas (*Parabole*, *Hyperbole*, *Elleipsis*, I.44, pp. 419–420), and Euclid's Proof & Generalization of Pythagoras's Theorem (I.47–I.48, pp. 426–432).

Usage
-----

.. code-block:: bash

   # Inspect Codex unit bounds and verify primary-source & concordance integrity
   geometor-proclus summary
   geometor-proclus verify

   # Recompile apparatus RST pages from JSON registries
   geometor-proclus compile-apparatus

   # Run unit tests and linter
   pytest
   ruff check src tests

   # Build the Book Codex HTML documentation into docs/
   publish build

Resources & Related Projects
----------------------------

- **Live Edition**: https://geometor.github.io/proclus
- **Source Code**: https://github.com/geometor/proclus
- `GEOMETOR • euclid <https://github.com/geometor/euclid>`_: Sir Thomas L. Heath's *The Thirteen Books of Euclid's Elements* (citing Proclus across 156 Friedlein keys).
- `GEOMETOR • elements <https://github.com/geometor/elements>`_: Symbolic G-Index (``G.1``–``G.525``) and constructive demonstrations.
- `GEOMETOR • hoenen <https://github.com/geometor/hoenen>`_: Peter Hoenen's *De Noetica Geometriae* (1954), engaging Proclus on *phantasia*, *probole*, and first principles.
- `PHOTON • publish <https://github.com/photon-platform/publish>`_: Sphinx Book Codex publishing engine and theme.
