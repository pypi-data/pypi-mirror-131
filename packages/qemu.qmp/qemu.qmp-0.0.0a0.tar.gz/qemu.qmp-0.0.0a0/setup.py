#!/usr/bin/env python3
"""
QEMU QMP library installer script
Copyright (c) 2020-2021 John Snow for Red Hat, Inc.
"""

import setuptools
import pkg_resources

try:
    import setuptools_scm
    _HAVE_SCM = True
except ModuleNotFoundError:
    _HAVE_SCM = False


def main():
    """
    QEMU tooling installer
    """

    # https://medium.com/@daveshawley/safely-using-setup-cfg-for-metadata-1babbe54c108
    pkg_resources.require('setuptools>=39.2')

    if _HAVE_SCM:
        setuptools.setup(use_scm_version={'fallback_version': '0.0.0'})
    else:
        setuptools.setup()


if __name__ == '__main__':
    main()
