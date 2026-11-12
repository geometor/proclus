import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from photon_platform.publish.global_conf import *  # noqa: E402, F403
import geometor.proclus as module  # noqa: E402
from geometor.proclus.sphinx_ext import (  # noqa: E402
    configure_local_intersphinx,
    register_greek_book_track,
)

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "proclus"
repo_name = "proclus"

setup_globals(org, org_name, repo, repo_name)  # noqa: F405

if "geometor.proclus.sphinx_ext" not in extensions:  # noqa: F405
    extensions.append("geometor.proclus.sphinx_ext")  # noqa: F405

register_greek_book_track()
configure_local_intersphinx(
    intersphinx_mapping,  # noqa: F405
    Path(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))),
)

project = "GEOMETOR • proclus"
author = "Proclus Diadochus"
copyright = "c. 470 AD (Friedlein 1873 / Taylor 1788–1789) • Digital Edition GEOMETOR"
