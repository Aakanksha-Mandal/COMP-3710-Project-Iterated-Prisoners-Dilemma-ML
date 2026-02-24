import random

class Strategy:
    def __init__(self, name): self.name = name
    def reset(self): pass
    def move(self, my_history, opp_history): pass

class ALLC(Strategy):
    def move(self, my_h, opp_h): return 'C'

class ALLD(Strategy):
    def move(self, my_h, opp_h): return 'D'

class RAND(Strategy):
    def move(self, my_h, opp_h): return random.choice(['C', 'D'])

class TFT(Strategy):
    def move(self, my_h, opp_h):
        return 'C' if not opp_h else opp_h[-1]

class TF2T(Strategy):
    def move(self, my_h, opp_h):
        if len(opp_h) < 2: return 'C'
        return 'D' if opp_h[-1] == 'D' and opp_h[-2] == 'D' else 'C'

class STFT(Strategy):
    def move(self, my_h, opp_h):
        return 'D' if not opp_h else opp_h[-1]