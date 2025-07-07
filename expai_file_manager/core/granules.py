# Minimal EXPAI granules.py
import json
import os
from . import act

granule_list = []
GRANULES_PATH = os.path.join(os.path.dirname(__file__), '../best_granules.json')

class Granule:
    def __init__(self, pattern, action_fn):
        self.pattern = pattern
        self.action_fn = action_fn

    def to_dict(self):
        return {'pattern': self.pattern, 'action_fn': self.action_fn}

def load_granules(path=GRANULES_PATH):
    global granule_list
    if not os.path.exists(path):
        granule_list = []
        return
    with open(path, 'r') as f:
        data = json.load(f)
        granule_list = [Granule(**g) for g in data]

def save_granules(path=GRANULES_PATH):
    with open(path, 'w') as f:
        json.dump([g.to_dict() for g in granule_list], f, indent=2)

def get_granules():
    return granule_list

def add_granule(granule):
    granule_list.append(granule)
    save_granules()

def run_action(granule, *args, sandbox_path=None):
    # Call the action function from act.py
    fn = getattr(act, granule.action_fn, None)
    if fn:
        return fn(*args, sandbox_path=sandbox_path)
    return {'status': 'noop'}

def initialize_basic_granules():
    # Only add if granule_list is empty
    if granule_list:
        return
    basic = [
        Granule(pattern="move", action_fn="move_file"),
        Granule(pattern="copy", action_fn="copy_file"),
        Granule(pattern="delete", action_fn="delete_file"),
        Granule(pattern="create_file", action_fn="create_file"),
        Granule(pattern="create_folder", action_fn="create_folder"),
    ]
    for g in basic:
        add_granule(g) 