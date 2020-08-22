import re
import glob
import os
import yaml


RE_DATAHUB_READ = re.compile(
    r"""
Datahub\.read\(         # Datahub.read( prefix
\s*                     # Skip leading whitespace
["']                    # quotes
(?P<path>.*?)           # resource path
["']                    # quotes
""",
    re.MULTILINE | re.VERBOSE,
)

RE_TARGET = re.compile(
    r"""
\[                      # [ prefix
\s*                     # Skip leading whitespace
["']                    # quotes
(?P<path>..://.*?)           # target path
["']                    # quotes
\s*                     # Skip leading whitespace
\]                      # ] suffix
""",
    re.MULTILINE | re.VERBOSE,
)


# rr = [x.groupdict() for x in RE_TARGET.finditer(test_str)]
# print(rr)

# rr = [x.groupdict() for x in RE_DATAHUB_READ.finditer(test_str)]
# print(rr)

path_mask = "downloads/.octave/ekatra_test/companies/ekatra_inc/blueprints/biotite/localActions/*"

INDEX = []

for p in sorted(glob.glob(path_mask)):
    # print(p)
    metafile = os.path.join(p, "meta.yaml")
    with open(metafile) as fileptr:
        meta = yaml.safe_load(fileptr)
        # print(meta)
    actionfile = os.path.join(p, "action.js")
    with open(actionfile) as fileptr:
        actionjs = fileptr.read()
        rr_targets = set([x.groupdict()['path'].replace('" + aux.counter.i + "', "X") for x in RE_TARGET.finditer(actionjs)])
        # print(rr_targets)
        meta['targets'] = rr_targets

        rr_datahub = set([x.groupdict()['path'] for x in RE_DATAHUB_READ.finditer(actionjs)])
        # print(rr_datahub)
        meta['reads'] = rr_datahub
        INDEX.append(meta)
# print(INDEX)
print('digraph G {')
print('ranksep=3;')
print('rank = "some";');
print('rankdir="LR";');
print()
print("    node [shape=box, color=blue, style=filled];")
for item in INDEX:
    print('"{source}"'.format(**item))

print("    node [shape=box, color=green, style=filled];")
for item in INDEX:
    print('"{source}" -> "{description}"'.format(**item))

print("    node [shape=box, color=yellow, style=filled];")
for item in INDEX:
    description = item.get("description")
    for path in sorted(item.get("targets")):
        print('"{description}" -> "{path}";'.format(path=path, description=description))

for item in INDEX:
    description = item.get("description")
    # paths = ['"%s"' % path for path in item.get('reads')]
    # if paths:
    #     print('"{description}" -> {{ {paths} }}'.format(paths=", ".join(paths), description=description))

print('}')