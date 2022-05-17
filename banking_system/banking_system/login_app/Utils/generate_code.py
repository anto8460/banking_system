from random import randint


def generate_code() -> str:
    # Generate random code
    return str(randint(100_000, 999_999))
