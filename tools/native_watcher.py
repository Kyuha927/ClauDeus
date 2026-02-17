import os
import time
import sys

def wait_for_change(directory='prompts'):
    """Waits for any .md file in the directory to be modified and prints its name."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)
        
    # Initial state
    last_mtimes = {}
    for f in os.listdir(directory):
        if f.endswith('.md'):
            path = os.path.join(directory, f)
            last_mtimes[path] = os.path.getmtime(path)

    # print(f"Native Watcher: Monitoring '{directory}' for changes...")
    while True:
        time.sleep(0.5)
        current_files = [f for f in os.listdir(directory) if f.endswith('.md')]
        
        for f in current_files:
            path = os.path.join(directory, f)
            try:
                current_mtime = os.path.getmtime(path)
                if path not in last_mtimes:
                    # New file detected
                    print(path)
                    sys.exit(0)
                elif current_mtime > last_mtimes[path]:
                    # Modification detected
                    print(path)
                    sys.exit(0)
            except Exception:
                continue
                
        # Handle deleted files
        for path in list(last_mtimes.keys()):
            if not os.path.exists(path):
                del last_mtimes[path]

if __name__ == "__main__":
    wait_for_change()
