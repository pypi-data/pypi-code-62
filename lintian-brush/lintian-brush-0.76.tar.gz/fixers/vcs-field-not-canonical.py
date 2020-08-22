#!/usr/bin/python3

from debmutate.control import ControlEditor
from lintian_brush.fixer import report_result, fixed_lintian_tag
from lintian_brush.vcs import canonicalize_vcs_url


fields = set()


with ControlEditor() as updater:
    for name in updater.source:
        if not name.startswith("Vcs-"):
            continue
        new_value = canonicalize_vcs_url(
            name[len("Vcs-"):], updater.source[name])
        if new_value != updater.source[name]:
            fixed_lintian_tag(
                updater.source, 'vcs-field-not-canonical',
                '%s %s' % (updater.source[name], new_value))
            updater.source[name] = new_value
            fields.add(name)

report_result("Use canonical URL in " + ', '.join(sorted(fields)) + '.')
