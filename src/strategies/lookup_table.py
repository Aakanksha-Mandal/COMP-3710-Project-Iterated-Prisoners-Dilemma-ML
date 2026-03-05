"""
Translates a bitstring (chromosome) into game moves using memory.
Crucial for Genetic Algorithm (Person B) and Machine Learning (Person C).
"""
from .baselines import Strategy

class LookupTableStrategy(Strategy):
    """
    Uses a 64-bit string to decide moves based on the outcomes 
    of the previous 3 rounds.
    """
    def __init__(self, bitstring, name="GA_Strategy", memory_depth=3):
        super().__init__(name)
        self.bitstring = bitstring # A string of '0's (Cooperate) and '1's (Defect)
        self.memory_depth = memory_depth

        expected_len = 4 ** self.memory_depth
        if len(self.bitstring) != expected_len:
            raise ValueError(
                f"Bitstring length must be 4^{self.memory_depth}={expected_len}, got {len(self.bitstring)}"
            )

    def move(self, my_h, opp_h):
        # For early rounds, history is insufficient for configured memory depth.
        # Defaults to 'C' until enough history is accumulated.
        if len(my_h) < self.memory_depth:
            return 'C' 
        
        # Outcome mapping: Maps round results to a base-4 digit
        m = {'CC': 0, 'CD': 1, 'DC': 2, 'DD': 3}
        
        # Convert last `memory_depth` outcomes into a base-4 index.
        # Example for depth=3: [r1,r2,r3] -> r1*4^2 + r2*4^1 + r3*4^0
        index = 0
        for i in range(self.memory_depth):
            outcome = my_h[-self.memory_depth + i] + opp_h[-self.memory_depth + i]
            index = (index * 4) + m[outcome]
        
        # Return move based on the bit value at that index position
        return 'C' if self.bitstring[index] == '0' else 'D'