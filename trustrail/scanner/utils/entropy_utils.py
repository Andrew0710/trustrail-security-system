import math

def calculate_entropy(string):
    """Calculate Shannon entropy of a string."""
    if not string:
        return 0
    entropy = 0
    length = len(string)
    char_count = {}
    for char in string:
        char_count[char] = char_count.get(char, 0) + 1
    for count in char_count.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def is_high_entropy(string, threshold=4.0):
    """Check if string has high entropy."""
    return calculate_entropy(string) > threshold