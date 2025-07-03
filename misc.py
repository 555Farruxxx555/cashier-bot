import random

def generate_exact_amount(amount: int) -> int:
    cents = random.randint(1, 99)
    return amount + cents


