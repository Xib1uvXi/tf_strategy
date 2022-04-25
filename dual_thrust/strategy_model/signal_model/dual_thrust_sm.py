
class DualThrustSignalModel:
    k1: float
    k2: float

    day_open: float

    max_high: float = 0.0
    min_low: float = 0.0
    max_close: float = 0.0
    min_close: float = 0.0

    day_range: float

    long_entry: float
    short_entry: float


    def __init__(self, k1: float, k2: float):
        self.k1 = k1
        self.k2 = k2

        self.day_open = 0.0


    def update_signal_value(self, max_high: float, min_low: float, max_close: float, min_close: float):
        self.max_high = max_high
        self.min_low = min_low
        self.max_close = max_close
        self.min_close = min_close

    def update_open_price(self, open_price: float):
        self.day_open = open_price
        self.day_range = max(self.max_high - self.min_close, self.max_close - self.min_low)
        self.long_entry = self.day_open + self.day_range * self.k1
        self.short_entry = self.day_open - self.day_range * self.k2
