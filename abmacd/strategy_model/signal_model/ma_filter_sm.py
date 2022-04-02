
from mimetypes import init

class MaFilterSignalModel:
    init: int

    # signal value
    price0 = 0.0
    ma0 = 0.0

    def __init__(self):
        self.init = 0

    def update_price(self, price: float):
        self.price0 = price

    def update_ma(self, ma: float):
        if self.init <= 1:
            self.init = self.init + 1

        # swap
        self.ma0 = ma
        
    
    def filter_long(self) -> bool:
        if self.init <= 1:
            return False

        return self.price0 > self.ma0

    def filter_short(self) -> bool:
        if self.init <= 1:
            return False
        
        return self.price0 < self.ma0
    