# Minimal EXPAI pattern_extractor.py
def extract_patterns(goal_desc):
    # Very basic pattern extraction from goal description
    print(f"[PATTERN] Extracting from: {goal_desc}")
    if 'move' in goal_desc:
        return 'move_file'
    if 'copy' in goal_desc:
        return 'copy_file'
    if 'delete' in goal_desc:
        return 'delete_file'
    if 'create file' in goal_desc:
        return 'create_file'
    if 'create folder' in goal_desc:
        return 'create_folder'
    return 'noop' 