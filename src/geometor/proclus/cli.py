"""Command-line interface for ``geometor-proclus``."""

from __future__ import annotations

import argparse
import json
import sys

from geometor.proclus.compile_codex import verify_codex_tracks, write_apparatus_pages
from geometor.proclus.concordance import CODEX_UNITS, verify_concordance


def main(argv: list[str] | None = None) -> int:
    """Run the ``geometor-proclus`` CLI."""
    parser = argparse.ArgumentParser(
        prog="geometor-proclus",
        description="GEOMETOR Proclus Book Codex & Friedlein (1873) Concordance CLI",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("summary", help="Display Codex structure and concordance statistics")
    sub.add_parser("verify", help="Verify primary sources, concordance coverage, and Codex tracks")
    sub.add_parser("compile-apparatus", help="Render apparatus RST pages from JSON registries")

    args = parser.parse_args(argv)
    cmd = args.command or "summary"

    if cmd == "compile-apparatus":
        written = write_apparatus_pages()
        for p in written:
            print(f"Wrote {p}")
        return 0

    conc_report = verify_concordance()
    if cmd == "summary":
        print("GEOMETOR • proclus — Commentary on Book I of Euclid's Elements (ed. Friedlein 1873)")
        for u in CODEX_UNITS:
            print(f"  [{u.slug:18s}] Friedlein pp. {u.friedlein_start:3d}–{u.friedlein_end:3d} | {u.title}")
        print(json.dumps(conc_report, indent=2))
        return 0

    if cmd == "verify":
        codex_report = verify_codex_tracks()
        combined = {"concordance": conc_report, "codex": codex_report}
        print(json.dumps(combined, indent=2))
        if not conc_report["valid"] or not codex_report["valid"]:
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
