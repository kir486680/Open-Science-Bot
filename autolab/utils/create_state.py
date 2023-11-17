# 1. Writes a JSON file with the "defaults", i.e. 0,0 for x, y, 0 for z, and open for gripper.

import json

default_state = {
    "x": 0,
    "y": 0,
    "z": 0,
    "gripper": "open"
}

with open("state.json", "w") as f:
    json.dump(default_state, f, indent=4)

