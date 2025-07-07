# Minimal EXPAI memory.py
import json
import os
from datetime import datetime

memory_buffer = []
MEMORY_PATH = os.path.join(os.path.dirname(__file__), '../memory.json')

def log_episode(episode_dict, path=MEMORY_PATH):
    episode = episode_dict.copy()
    episode['timestamp'] = datetime.utcnow().isoformat()
    memory_buffer.append(episode)
    save_memory(path)

def save_memory(path=MEMORY_PATH):
    with open(path, 'w') as f:
        json.dump(memory_buffer, f, indent=2)

def load_memory(path=MEMORY_PATH):
    global memory_buffer
    if not os.path.exists(path):
        memory_buffer = []
        return memory_buffer
    with open(path, 'r') as f:
        memory_buffer = json.load(f)
    return memory_buffer

def get_recent_episodes(n=10):
    return memory_buffer[-n:] 
