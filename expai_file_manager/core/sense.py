# Minimal EXPAI sense.py
import os

def sense_environment(sandbox_path):
    try:
        items = []
        for root, dirs, files in os.walk(sandbox_path):
            rel_root = os.path.relpath(root, sandbox_path)
            for d in dirs:
                items.append({'type': 'folder', 'name': d, 'path': os.path.normpath(os.path.join(rel_root, d))})
            for f in files:
                items.append({'type': 'file', 'name': f, 'path': os.path.normpath(os.path.join(rel_root, f))})
        print(f"[SENSE] Found {len(items)} items in sandbox.")
        return {'status': 'success', 'environment': items}
    except Exception as e:
        print(f"[SENSE] Failed: {e}")
        return {'status': 'error', 'environment': []} 