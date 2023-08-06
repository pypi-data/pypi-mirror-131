#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Licenses module. Generate a license file."""
__author__ = "@britodfbr"  # pragma: no cover
from functools import partial
from pathlib import Path

from incolumepy.makefilelicense.exceptions import LicenseUnavailable


def licenses(license_name: str = "", outputfile: str = "") -> bool:
    """
    Got license text.

    :param license_name: [agpl apache bsl cc0 gpl lgpl mit mpl unlicense] default=mit
    :param outputfile: Output filename within license choiced.
    :return: A file named into outpufile with the license of reference
    """
    license_name = license_name.casefold() or "mit"
    outputfile = outputfile or "LICENSE"
    repo = Path(__file__).parents[0].joinpath("licenses")

    try:
        license_file = repo.joinpath(f"{license_name}.txt")
        Path(outputfile).write_text(license_file.read_text())
        return True
    except (AttributeError, FileNotFoundError) as e:
        raise LicenseUnavailable("license unavailable") from e


license_agpl = partial(licenses, "agpl")
license_apache = partial(licenses, "apache")
license_bsl = partial(licenses, "bsl")
license_cc0 = partial(licenses, "cc0")
license_gpl = partial(licenses, "gpl")
license_lgpl = partial(licenses, "lgpl")
license_mit = partial(licenses, "MIT")
license_mpl = partial(licenses, "mpl")
unlicense = partial(licenses, "unlicense")

if __name__ == "__main__":  # pragma: no cover
    print(licenses("xpto"))
