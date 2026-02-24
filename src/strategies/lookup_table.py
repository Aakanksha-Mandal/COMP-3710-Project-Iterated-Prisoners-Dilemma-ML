from strategies.baselines import Strategy

class LookupTableStrategy(Strategy):
    def __init__(self, bitstring, name="GA_Strategy"):
        super().__init__(name)
        self.bitstring = bitstring # String of 64 or 70 chars

    def move(self, my_h, opp_h):
        t = len(my_h)
        # Handle first 3 rounds where history is incomplete
        if t < 3:
            return 'C'
        
        # Mapping: CC=0, CD=1, DC=2, DD=3
        m = {'CC': 0, 'CD': 1, 'DC': 2, 'DD': 3}
        # Get last 3 rounds
        r1 = m[my_h[-3] + opp_h[-3]]
        r2 = m[my_h[-2] + opp_h[-2]]
        r3 = m[my_h[-1] + opp_h[-1]]
        
        # Convert base-4 sequence to base-10 index (0-63)
        index = (r1 * 16) + (r2 * 4) + r3
        return 'C' if self.bitstring[index] == '0' else 'D'