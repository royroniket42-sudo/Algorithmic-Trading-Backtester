import pandas as pd

class MovingAverageCrossover:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []

    def generate_signal(self, current_price):
        self.prices.append(current_price)
        
        if len(self.prices) < self.long_window:
            return 0 # Not enough data, hold
            
        short_ma = sum(self.prices[-self.short_window:]) / self.short_window
        long_ma = sum(self.prices[-self.long_window:]) / self.long_window
        
        # Current logic: If short MA is above long MA, be long (Buy). Otherwise, sell.
        if short_ma > long_ma:
            return 1
        elif short_ma < long_ma:
            return -1
        
        return 0