# Utility functions
def calculate_total(items):
    return sum(item['price'] * item['quantity'] for item in items)

def format_date(date):
    return date.strftime('%Y-%m-%d')
