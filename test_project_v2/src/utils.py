"""
Utility functions for the application.
This file is intentionally clean - no secrets should be detected here.
"""

def calculate_total(items):
    """Calculate the total price of items."""
    return sum(item['price'] * item['quantity'] for item in items)


def format_currency(amount):
    """Format amount as currency string."""
    return f"${amount:.2f}"


def validate_email(email):
    """Simple email validation."""
    return '@' in email and '.' in email.split('@')[-1]


def generate_id():
    """Generate a random ID (not a secret)."""
    import uuid
    return str(uuid.uuid4())


def capitalize_words(text):
    """Capitalize each word in text."""
    return ' '.join(word.capitalize() for word in text.split())


if __name__ == "__main__":
    # Test functions
    test_items = [{'price': 10.0, 'quantity': 2}, {'price': 5.0, 'quantity': 3}]
    print(f"Total: {calculate_total(test_items)}")
    print(f"Formatted: {format_currency(25.5)}")
    print(f"Email valid: {validate_email('test@example.com')}")