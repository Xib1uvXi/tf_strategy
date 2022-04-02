
from mimetypes import init

class MaFilterSignalModel:
    name = ""
    init: int

    # signal value
    price0 = 0.0
    ma0 = 0.0

    def __init__(self, name: str):
        self.init = 0
        self.name = name

    def update(self, price: float, ma: float):
        if self.init <= 1:
            self.init = self.init + 1

        # swap
        self.ma0 = ma
        self.price0 = price
    
    def filter_long(self) -> bool:
        if self.init <= 1:
            return False

        return self.price0 > self.ma0

    def filter_short(self) -> bool:
        if self.init <= 1:
            return False
        
        return self.price0 < self.ma0
    