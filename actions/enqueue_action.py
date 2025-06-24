import os
from filelock import FileLock

def enqueue_action(action_name, args, queue_file="queue.txt"):
    """Add an action with args to the queue file."""
    lock_file = f"{queue_file}.lock"
    
    # Format the line: action_name arg1 arg2 ...
    line = f"{action_name} {' '.join(args)}\n"
    
    with FileLock(lock_file):
        with open(queue_file, 'a') as f:
            f.write(line)
    
    return f"Enqueued: {action_name} {' '.join(args)}"

def run(args):
    """Entry point for the enqueue_action action."""
    if len(args) < 1:
        return "Error: No action name provided. Usage: enqueue_action <action_name> [args...]"
    
    action_name = args[0]
    action_args = args[1:]
    
    try:
        result = enqueue_action(action_name, action_args)
        return result
    except Exception as e:
        return f"Error enqueueing action: {e}"