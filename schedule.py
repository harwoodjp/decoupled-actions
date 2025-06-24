#!/usr/bin/env python3
import os
import sys
import time
import importlib.util

INTERVAL_SECONDS = 10

def load_action(action_name):
    """Load an action module from the actions directory."""
    action_path = os.path.join("actions", f"{action_name}.py")
    
    if not os.path.exists(action_path):
        return None
    
    spec = importlib.util.spec_from_file_location(action_name, action_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def main():
    """Run an action at regular intervals."""
    if len(sys.argv) < 2:
        print("Usage: python schedule.py <action> [args...]")
        return 1
    
    action_name = sys.argv[1]
    args = sys.argv[2:]
    
    action_module = load_action(action_name)
    if not action_module:
        print(f"Error: Action '{action_name}' not found")
        return 1
    
    if not hasattr(action_module, 'run'):
        print(f"Error: Action '{action_name}' missing run function")
        return 1
    
    print(f"Scheduling {action_name} every {INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            try:
                result = action_module.run(args)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {action_name}: {result}")
            except Exception as e:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Error executing {action_name}: {e}")
            
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nScheduler stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())