import json
import os
import blackboxprotobuf

dir_path = os.path.dirname(os.path.abspath(__file__))
DUMPS_FOLDER = "dumps"
OUT_FOLDER = "out"
diffs = {}
MAP_TYPE = {
    "3": "bool",
    "4": "int",
    "5": "str"
    }

def _get_value_and_type(exp_json):

    for el in ["3", "4", "5"]:
        if (val := exp_json.get(el, None)) is not None:  
            return val.get("1", "EMPTY"), MAP_TYPE[el]
    
    raise Exception(exp_json)


def get_flags(filename: str):
    with open(os.path.join(dir_path, f"{DUMPS_FOLDER}\\{filename}"), "r") as f:
        message, typedef = blackboxprotobuf.protobuf_to_json(bytes.fromhex(f.read()))
        message_json = json.loads(message)

    with open(os.path.join(dir_path, f"{OUT_FOLDER}\\json-{filename}.json"), "wb") as f:
        f.write(message.encode("utf-8"))

    experiments = message_json["1"]["1"]["1"]["3"]
    res = {}
    for el in experiments:
        exp_category = el["1"]["1"]
        exp_id = el["1"]["2"]
        id = f"{exp_category}::{exp_id}"
        value, type = _get_value_and_type(el)
        if id not in res: res[id] = {} 
        res[id]["value"] = value
        res[id]["type"] = type
    
    with open(os.path.join(dir_path, f"{OUT_FOLDER}\\flags-{filename}.json"), "wb") as f:
        f.write(json.dumps(res, indent=2, sort_keys=True).encode("utf-8"))

    return res


def generate_diff(left: dict, right: dict):
    all_ids = set(left.keys()) | set(right.keys())

    for id in all_ids:
        exists_left = left.get(id, None)
        exists_right = right.get(id, None)

        value_left = left[id]["value"] if exists_left else "MISSING_LEFT"
        value_right = right[id]["value"] if exists_right else "MISSING_RIGHT"

        if value_left == value_right:
            continue

        if exists_left and exists_right and left[id]["type"] != right[id]["type"]:
            raise Exception(f"Type is different. {id}")
        
        value_type = left[id]["type"] if exists_left else right[id]["type"]


        if id not in diffs: diffs[id] = {}
        diffs[id]["value_left"] = value_left 
        diffs[id]["value_right"] = value_right
        diffs[id]["type"] = value_type

    with open(os.path.join(dir_path, f"{OUT_FOLDER}\\diffs.json"), "wb") as f:
        f.write(json.dumps(diffs, indent=2, sort_keys=True).encode("utf-8"))

    return diffs

flags_working = get_flags("dump-working")
flags_not_working = get_flags("dump-not-working")

diffs = generate_diff(flags_not_working, flags_working)