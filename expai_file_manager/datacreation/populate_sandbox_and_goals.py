import os
import json

BASE = os.path.dirname(os.path.dirname(__file__))
SANDBOX = os.path.join(BASE, 'sandbox')
GOALS_PATH = os.path.join(BASE, 'goals', 'simple_goals.json')

# Minimal set of folders and files
FOLDERS = ['Documents', 'Images', 'Backups']
FILES = [
    ('file1.txt', 'Documents'),
    ('file2.pdf', 'Documents'),
    ('image1.jpg', 'Images'),
    ('backup1.tmp', 'Backups')
]

def setup_sandbox():
    print("Setting up minimal sandbox...")
    for folder in FOLDERS:
        folder_path = os.path.join(SANDBOX, folder)
        os.makedirs(folder_path, exist_ok=True)
    for fname, folder in FILES:
        fpath = os.path.join(SANDBOX, folder, fname)
        if not os.path.exists(fpath):
            with open(fpath, 'w') as f:
                f.write('')
    print("Sandbox setup complete.")

def generate_simple_goals():
    print("Generating simple goals from environment...")
    # Scan sandbox
    env = []
    for root, dirs, files in os.walk(SANDBOX):
        for d in dirs:
            env.append({'type': 'folder', 'name': d, 'path': os.path.relpath(os.path.join(root, d), SANDBOX)})
        for f in files:
            env.append({'type': 'file', 'name': f, 'path': os.path.relpath(os.path.join(root, f), SANDBOX)})
    # Find all files and folders
    files = [item for item in env if item['type'] == 'file']
    folders = [item for item in env if item['type'] == 'folder']
    goals = []
    # Move/copy/delete for each file
    for f in files:
        if folders:
            # Pick a different folder for move/copy
            for folder in folders:
                if not f['path'].startswith(folder['name']):
                    goals.append({
                        "description": f"Move {f['name']} to the '{folder['name']}' folder.",
                        "type": "move"
                    })
                    goals.append({
                        "description": f"Copy {f['name']} to the '{folder['name']}' folder.",
                        "type": "copy"
                    })
        goals.append({
            "description": f"Delete {f['name']} from the sandbox.",
            "type": "delete"
        })
    # Create file goal (for a new file)
    goals.append({
        "description": "Create file newfile.txt in the sandbox.",
        "type": "create_file"
    })
    # Create folder goal (for a new folder)
    goals.append({
        "description": "Create folder 'NewFolder' in the sandbox.",
        "type": "create_folder"
    })
    with open(GOALS_PATH, 'w') as f:
        json.dump(goals, f, indent=2)
    print(f"Saved {len(goals)} simple goals to {GOALS_PATH}")
    return goals

def main():
    setup_sandbox()
    generate_simple_goals()
    print("Minimal sandbox and goals ready.")

if __name__ == "__main__":
    main() 