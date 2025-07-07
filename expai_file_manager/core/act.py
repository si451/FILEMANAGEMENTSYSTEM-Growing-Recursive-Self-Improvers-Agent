# Minimal EXPAI act.py
import os
import shutil

def move_file(src, dst, sandbox_path=None):
    try:
        src_path = os.path.join(sandbox_path, src)
        dst_path = os.path.join(sandbox_path, dst)
        shutil.move(src_path, dst_path)
        print(f"Moved {src} to {dst}")
        return {'status': 'success'}
    except Exception as e:
        print(f"Move failed: {e}")
        return {'status': 'error', 'error': str(e)}

def copy_file(src, dst, sandbox_path=None):
    try:
        src_path = os.path.join(sandbox_path, src)
        dst_path = os.path.join(sandbox_path, dst)
        shutil.copy(src_path, dst_path)
        print(f"Copied {src} to {dst}")
        return {'status': 'success'}
    except Exception as e:
        print(f"Copy failed: {e}")
        return {'status': 'error', 'error': str(e)}

def delete_file(target, sandbox_path=None):
    try:
        target_path = os.path.join(sandbox_path, target)
        os.remove(target_path)
        print(f"Deleted {target}")
        return {'status': 'success'}
    except Exception as e:
        print(f"Delete failed: {e}")
        return {'status': 'error', 'error': str(e)}

def create_file(filename, sandbox_path=None):
    try:
        file_path = os.path.join(sandbox_path, filename)
        with open(file_path, 'w') as f:
            f.write('')
        print(f"Created file {filename}")
        return {'status': 'success'}
    except Exception as e:
        print(f"Create file failed: {e}")
        return {'status': 'error', 'error': str(e)}

def create_folder(foldername, sandbox_path=None):
    try:
        folder_path = os.path.join(sandbox_path, foldername)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder {foldername}")
        return {'status': 'success'}
    except Exception as e:
        print(f"Create folder failed: {e}")
        return {'status': 'error', 'error': str(e)} 