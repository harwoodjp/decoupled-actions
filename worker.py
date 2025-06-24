#!/usr/bin/env python3
import os
import sys
import time
import importlib.util
from filelock import FileLock

def load_action(action_name):
    """Load an action module from the actions directory."""
    action_path = os.path.join("actions", f"{action_name}.py")
    
    if not os.path.exists(action_path):
        return None
    
    spec = importlib.util.spec_from_file_location(action_name, action_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def process_queue_file(queue_file):
    """Process a single line from the queue file and remove it."""
    lock_file = f"{queue_file}.lock"
    
    with FileLock(lock_file):
        if not os.path.exists(queue_file):
            return False
        
        with open(queue_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return False
        
        # Get the first line and remove it
        first_line = lines[0].strip()
        remaining_lines = lines[1:]
        
        # Write back the remaining lines
        with open(queue_file, 'w') as f:
            f.writelines(remaining_lines)
        
        if not first_line:
            return True
        
        # Parse the line: action_name arg1 arg2 ...
        parts = first_line.split()
        if not parts:
            return True
        
        action_name = parts[0]
        args = parts[1:]
        
        # Load and execute the action
        action_module = load_action(action_name)
        if not action_module:
            print(f"Error: Action '{action_name}' not found")
            return True
        
        if not hasattr(action_module, 'run'):
            print(f"Error: Action '{action_name}' missing run function")
            return True
        
        try:
            result = action_module.run(args)
            print(f"Executed {action_name} {' '.join(args)}: {result}")
        except Exception as e:
            print(f"Error executing {action_name}: {e}")
        
        return True

def main():
    """Main subscriber loop."""
    if len(sys.argv) != 2:
        print("Usage: python subscriber.py <queue_file>")
        return 1
    
    queue_file = sys.argv[1]
    
    print(f"Subscriber started, monitoring {queue_file}")
    
    try:
        while True:
            if process_queue_file(queue_file):
                # Processed something, check immediately for more
                continue
            else:
                # No work, wait a bit
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSubscriber stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())