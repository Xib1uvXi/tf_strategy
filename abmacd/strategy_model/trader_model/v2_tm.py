from abmacd.strategy_model.trader_model.base_trader_model import BaseTraderModel

from typing import Any, Protocol


class ProxyCallable(Protocol):
    def __call__(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False,
    ): ...


class V2Trader(BaseTraderModel):
    target_pos: float  # long_back & short_back
    pricetick: float

    def __init__(
            self,
            fixed_size: float,
            pricetick: float,
            buy: ProxyCallable,
            short: ProxyCallable,
            sell: ProxyCallable,
            cover: ProxyCallable,
            debug: bool = False,
    ):
        super().__init__(buy, short, sell, cover, fixed_size, debug)

        self.pricetick = pricetick
        self.target_pos = 0

    def _open_long(self, price: float, action: Any, is_back: bool = False, is_blvl: bool = False):
        if self.pos < 0:
            return

        if (not is_blvl) and abs(self.pos) != 0:
            return

        if is_back:
            self._buy(price, self._target_pos(), action)
            self._reset_target_pos()
        else:
            self._buy(price, self.fixed_size, action)

    def _open_short(self, price: float, action: Any, is_back: bool = False):
        if abs(self.pos) != 0:
            return

        if is_back:
            self._short(price, self.fixed_size, action)
        else:
            self._short(price, self.fixed_size, action)

    # TODO: 必须成交
    def _close_long(self, price: float, action: Any, is_blvl: bool = False):
        if abs(self.pos) == 0:
            return

        if self.pos > 0:
            if is_blvl:
                self._update_target_pos(self.pos)

            self._sell(price, action)

    # TODO: 必须成交
    def _close_short(self, price: float, action: Any):
        if abs(self.pos) == 0:
            return

        if self.pos < 0:
            self._cover(price, action)

    # TODO: 必须成交
    def _rollback_short_to_long(self, price: float, action: Any):
        if self.pos > 0:
            return

        if self.pos == 0:
            self._buy(price, self.fixed_size, action)
            return

        if self.pos < 0:
            self._cover(price, action)
            self._buy(price, self.fixed_size, action)

    # TODO: 必须成交
    def _rollback_long_to_short(self, price: float, action: Any):
        if self.pos < 0:
            return

        if self.pos == 0:
            self._short(price, self.fixed_size, action)
            return

        if self.pos > 0:
            self._sell(price, action)
            self._short(price, self.fixed_size, action)

    # long back & short back target pos
    def _target_pos(self) -> float:
        if self.target_pos == 0:
            return self.fixed_size

        return abs(self.target_pos)

    def _reset_target_pos(self) -> None:
        self.target_pos = 0

    def _update_target_pos(self, pos: int) -> None:
        self.target_pos = pos

    # pricetick

    def _cover_price(self, price: float) -> float:
        return price + self.pricetick

    def _sell_price(self, price: float) -> float:
        if price - self.pricetick <= 0:
            return price

        return price - self.pricetick
