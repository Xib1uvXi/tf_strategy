class Stoploss:
    direction: int = 0
    pos: float = 0
    holding_avg_price: float = 0

    stoploss: float

    def __init__(self, direction: int, stoploss: float):
        self.stoploss = stoploss
        self.direction = direction

    def need_close(self, current_price: float) -> bool:
        if self.pos == 0:
            return False

        sl = self._stopless_price()
        if sl == 0:
            print("============================ error stoploss price is zero ==============================")
            return False

        if self.direction == 1:
            return current_price <= sl

        else:
            return current_price >= sl

    def open(self, direction: int, open_price: float, amount: float):
        if self.direction != direction:
            print("============================ error stoploss open self.direction != direction ==============================")
            return

        self._add_pos(open_price, amount)

    def close(self, direction: int):
        if self.direction != direction:
            print("============================ error stoploss close self.direction != direction ==============================")
            return

        self._clear_pos()

    def _add_pos(self, open_price: float, amount: float):
        if self.pos == 0:
            self.holding_avg_price = open_price
            self.pos = amount
        else:
            self.holding_avg_price = (self.holding_avg_price * self.pos + open_price * amount) / (self.pos + amount)
            self.pos = self.pos + amount

    def _clear_pos(self):
        self.pos = 0
        self.holding_avg_price = 0

    def _stopless_price(self) -> float:
        if self.direction == 1:
            return self.holding_avg_price * (1 - self.stoploss)

        if self.direction == -1:
            return self.holding_avg_price * (1 + self.stoploss)

        return 0
