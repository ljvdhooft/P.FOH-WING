# Python program to read
# json file

import json
from deepdiff import DeepDiff
from mergedeep import merge
import os

with open("new.snap", "r") as j:
    snap = json.load(j)

with open("previous.snap", "r") as j:
    ref = json.load(j)

# make backup
# dt = str(datetime.now())[0:-7]
# with open("archive/%s_%s.snap" % (input, dt), "w") as jsonFile:
#     json.dump(snap, jsonFile)


def recursive_get(d, keys):
    if len(keys) == 1:
        return d[keys[0]]
    return recursive_get(d[keys[0]], keys[1:])


changes = DeepDiff(ref, snap)
changes = changes['values_changed'] if 'values_changed' in changes else False

print(changes)

if changes != False:
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

    print(result)

    out = merge(snap, result)

    # with open("global/snapshots/diff.snap", "w") as jsonFile:
    #     json.dump(result, jsonFile)


    path = 'global/snapshots/_users'
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    for subfolder in subfolders:
        print("File updated in " + subfolder)
        snapname = subfolder + '/P.FOH 2023 ' + subfolder[24:] + '.snap'
        with open(snapname, "w") as jsonFile:
            json.dump(out, jsonFile, sort_keys=True, indent=4)

os.remove("new.snap")
os.remove("previous.snap")
