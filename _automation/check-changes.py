import json
from deepdiff import DeepDiff
from mergedeep import merge
import os
from pathlib import Path

with open("new.snap", "r") as j:
    snap = json.load(j)

with open("previous.snap", "r") as j:
    ref = json.load(j)

def recursive_get(d, keys):
    if len(keys) == 1:
        return d[keys[0]]
    return recursive_get(d[keys[0]], keys[1:])


diff = DeepDiff(ref, snap)
changes = {}
if 'type_changes' in diff:
    changes.update(diff['type_changes'])
if 'values_changed' in diff:
    changes.update(diff['values_changed'])
if 'type_changes' and 'values_changed' not in diff:
    changes = False


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

    print(json.dumps(result, indent=1))

    path = 'global/snapshots/_users'
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    for subfolder in subfolders:
        for path in Path(subfolder).glob(f"P.FOH*.snap"):
            snapname = path
            print(f"Updated file {snapname}")
            with open(snapname, "r") as j:
                target = json.load(j)
            out = merge(target, result)
            with open(snapname, "w") as jsonFile:
                jsonFile.write(json.dumps(out, indent='\t'))

os.remove("new.snap")
os.remove("previous.snap")
