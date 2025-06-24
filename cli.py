#!/usr/bin/env python3
import sys
import os
import importlib.util

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
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <action> [args...]")
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
    
    try:
        result = action_module.run(args)
        print(result)
        return 0
    except Exception as e:
        print(f"Error running action '{action_name}': {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())