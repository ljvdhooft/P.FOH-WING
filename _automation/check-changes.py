# Python program to read
# json file

import json
from datetime import datetime
from deepdiff import DeepDiff
from mergedeep import merge

input = "P.FOH 2023"
ref = "changes"
output = ""

with open("global/snapshots/%s.snap" % input, "r") as jsonFile:
    snap = json.load(jsonFile)

with open("global/snapshots/%s.snap" % ref, "r") as jsonFile:
    ref = json.load(jsonFile)

# make backup
# dt = str(datetime.now())[0:-7]
# with open("archive/%s_%s.snap" % (input, dt), "w") as jsonFile:
#     json.dump(snap, jsonFile)


def recursive_get(d, keys):
    if len(keys) == 1:
        return d[keys[0]]
    return recursive_get(d[keys[0]], keys[1:])


changes = DeepDiff(snap, ref)['values_changed']

result = {}
for change in changes:
    keys = change[6:-2].split('\'][\'')
    i = 1
    new_dict = current = {}
    for key in keys:
        if i == len(keys):
            current[key] = changes[change]['new_value']
        else:
            current[key] = {}
            current = current[key]
            i += 1
    merge(result, new_dict)

out = merge(snap, result)

print(out)

with open("global/snapshots/diff.snap", "w") as jsonFile:
    json.dump(result, jsonFile)


if output == "":
    with open("global/snapshots/P.FOH 2023.snap", "w") as jsonFile:
        json.dump(snap, jsonFile)
else:
    with open("global/snapshots/%s.snap" % output, "w") as jsonFile:
        json.dump(out, jsonFile)
