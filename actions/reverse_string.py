def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def run(args):
    """Entry point for the reverse_string action."""
    if not args:
        return "Error: No text provided to reverse"
    
    text = " ".join(args)
    result = reverse_string(text)
    return f"Reversed: {result}"