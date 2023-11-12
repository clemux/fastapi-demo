import random


def generate_activation_code():
    """Generates a random 4-digit activation code."""
    code = random.randint(1000, 9999)
    return f"{code:04d}"
