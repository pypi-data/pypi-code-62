#!/usr/bin/python3

from lintian_brush.fixer import (
    report_result,
    fixed_lintian_tag,
    )
import re
from typing import List


for name in ['configure.ac', 'configure.in']:
    oldlines: List[bytes] = []
    newlines: List[bytes] = []
    try:
        with open(name, 'rb') as f:
            for lineno, line in enumerate(f, 1):
                newline = re.sub(
                    b'AC_PATH_PROG\\s*\\(\\s*PKG_CONFIG\\s*'
                    b',\\s*pkg-config\\s*(,\\s*.*\\s*?)\\)',
                    b'PKG_PROG_PKG_CONFIG', line)
                if line != newline:
                    fixed_lintian_tag(
                        'source',
                        'autotools-pkg-config-macro-not-cross-compilation-'
                        'safe', info='%s (line %d)' % (name, lineno))
                newlines.append(newline)
    except FileNotFoundError:
        continue
    if oldlines != newlines:
        with open(name, 'wb') as f:
            f.writelines(newlines)


report_result(
    """Use cross-build compatible macro for finding pkg-config.

The package uses AC_PATH_PROG to discover the location of pkg-config(1). This
macro fails to select the correct version to support cross-compilation.

This patch changes it to use PKG_PROG_PKG_CONFIG macro from pkg.m4.

Refer to https://bugs.debian.org/884798 for details.""",
    patch_name='ac-path-pkgconfig')
