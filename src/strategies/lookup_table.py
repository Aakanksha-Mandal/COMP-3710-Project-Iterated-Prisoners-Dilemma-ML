import random

def random_strategy(length=64):
    """
    Generates a random bitstring strategy.
    0 = Cooperate
    1 = Defect
    """
    return ''.join(random.choice(['0', '1']) for _ in range(length))

# Each round you have 4 possible configurations (CC, CD, DC, DD)
# History of 3 rounds (memory depth =3)
# 4^3 = 64 moves