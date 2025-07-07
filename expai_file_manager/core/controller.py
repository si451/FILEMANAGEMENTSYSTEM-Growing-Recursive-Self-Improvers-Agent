# Minimal EXPAI controller.py
import os
import json
from . import sense, act, granules, memory, pattern_extractor

class EXPAIAgent:
    def __init__(self, sandbox_path=None):
        self.goal = None
        self.sandbox_path = sandbox_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sandbox')
        granules.load_granules()
        memory.load_memory()

    def load_goal(self, goal):
        if isinstance(goal, dict):
            self.goal = goal
        else:
            with open(goal, 'r') as f:
                loaded = json.load(f)
                self.goal = loaded[0] if isinstance(loaded, list) else loaded
        print(f"[AGENT] Loaded goal: {self.goal.get('description')}")

    def run_cycle(self):
        env_before = sense.sense_environment(self.sandbox_path)
        if env_before['status'] != 'success':
            print("[AGENT] Sensing failed.")
            return
        last_env = env_before['environment']
        candidate = self.select_granule(last_env)
        result = None
        reward = 0
        if candidate:
            print(f"[AGENT] Using granule: {candidate.pattern}")
            arg_list = self.get_action_args(candidate, last_env)
            if arg_list:
                for args in arg_list:
                    res = granules.run_action(candidate, *args, sandbox_path=self.sandbox_path)
                    reward = 1 if res.get('status') == 'success' else -1
                    result = res
            else:
                result = {'status': 'noop'}
                reward = 0
        else:
            print("[AGENT] No suitable granule found.")
            result = {'status': 'noop'}
            reward = 0
        env_after = sense.sense_environment(self.sandbox_path)
        episode_data = {
            'env_before': last_env,
            'env_after': env_after['environment'] if env_after['status'] == 'success' else [],
            'action': candidate.action_fn if candidate else 'noop',
            'result': result,
            'reward': reward,
            'goal_description': self.goal.get('description', '') if self.goal else '',
            'granule_pattern': candidate.pattern if candidate else ''
        }
        memory.log_episode(episode_data)

    def select_granule(self, env):
        candidates = granules.get_granules()
        if not candidates or not self.goal:
            return None
        desc = self.goal.get('description', '').lower()
        for g in candidates:
            if g.pattern in desc:
                return g
        return None

    def get_action_args(self, granule, env):
        # Real-time argument extraction for each action type, using full paths
        if not env:
            return None
        if granule.pattern == "move":
            files = [item for item in env if item['type'] == 'file']
            folders = [item for item in env if item['type'] == 'folder']
            if files and folders:
                # Move first file to first folder (not its own parent)
                for file in files:
                    for folder in folders:
                        if not file['path'].startswith(folder['path']):
                            return [[file['path'], folder['path']]]
        elif granule.pattern == "copy":
            files = [item for item in env if item['type'] == 'file']
            folders = [item for item in env if item['type'] == 'folder']
            if files and folders:
                for file in files:
                    for folder in folders:
                        if not file['path'].startswith(folder['path']):
                            return [[file['path'], folder['path']]]
        elif granule.pattern == "delete":
            files = [item for item in env if item['type'] == 'file']
            if files:
                return [[files[0]['path']]]
        elif granule.pattern == "create_file":
            # Propose a new file name at root
            return [["newfile.txt"]]
        elif granule.pattern == "create_folder":
            # Propose a new folder name at root
            return [["NewFolder"]]
        return None 