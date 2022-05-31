import json
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def get_asset(name: str) -> dict:
    with open(f'{SCRIPT_DIR}{os.sep}assets{os.sep}{name}') as f:
        return json.load(f)
