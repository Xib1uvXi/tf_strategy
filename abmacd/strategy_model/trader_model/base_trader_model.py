from typing import Any, List, Protocol


class ProxyCallable(Protocol):
    def __call__(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False,
    ): ...


class BaseTraderModel:
    debug: bool = False

    # order
    fixed_size: float = 1.0

    # position
    pos: int

    # open
    buy_proxy: ProxyCallable
    short_proxy: ProxyCallable

    # close
    sell_proxy: ProxyCallable
    cover_proxy: ProxyCallable
    orders: List[Any]

    def __init__(
            self,
            buy: ProxyCallable,
            short: ProxyCallable,
            sell: ProxyCallable,
            cover: ProxyCallable,
            fixed_size: float,
            debug: bool = False,
    ):
        self.fixed_size = fixed_size
        self.pos = 0
        self.buy_proxy = buy
        self.short_proxy = short
        self.sell_proxy = sell
        self.cover_proxy = cover
        self.debug = debug
        self.orders = []

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

    def _sell_with_amount(self, price: float, amount: float, msg: Any):
        ids = self.sell_proxy(price, abs(amount))
        self._log("sell", price,  abs(amount), ids, msg)
        return ids

    def _cover_with_amount(self, price: float, amount: float, msg: Any):
        ids = self.cover_proxy(price, abs(amount))
        self._log("cover", price, abs(amount), ids, msg)
        return ids

    def _log(self, direction: str, price: float, size: float, ids, msg):

        order = {"order_id": ids, "action": msg, "direction": direction, "price": price, "size": size}
        self.orders.append(order)

        if self.debug:
            print("direction: %s, price: %s, amout: %s, ids: %s, msg: %s" % (direction, price, size, ids, msg))
