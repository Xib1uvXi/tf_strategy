from re import A
from typing import Any, Callable

class BaseTraderModel:
    debug: bool = False

    # order
    fixed_size: float = 1.0

    # position
    pos: int

    # open
    buy_proxy: Callable
    short_proxy: Callable

    # close
    sell_proxy: Callable
    cover_proxy: Callable

    def __init__(self, buy: Callable, short: Callable, sell: Callable, cover: Callable, fixed_size: float, debug: bool = False):
        self.fixed_size = fixed_size
        self.pos = None
        self.buy_proxy = buy
        self.short_proxy = short
        self.sell_proxy = sell
        self.cover_proxy = cover
        self.debug = debug
 
    def update_pos(self, pos: int):
        self.pos = pos

    def _buy(self, price: float, size: float, msg: Any):
        ids = self.buy_proxy(price, size)
        self._log("buy", price, size, ids, msg)
        return ids

    def _short(self, price: float, size: float, msg: Any):
        ids = self.short_proxy(price, size)
        self._log("short", price, size, ids, msg)
        return ids

    def _sell(self, price: float, msg: Any):
        ids = self.sell_proxy(price, abs(self.pos))
        self._log("sell", price, abs(self.pos), ids, msg)
        return ids

    def _cover(self, price: float, msg: Any):
        ids = self.cover_proxy(price, abs(self.pos))
        self._log("cover", price, abs(self.pos), ids, msg)
        return ids

    def _log(self, direction: str, price: float, size: float, ids, msg):
        if self.debug:
            print("direction: %s, price: %s, amout: %s, ids: %s, msg: %s" % (direction, price, size, ids, msg))