from typing import Protocol
from abmacd.strategy_model.signal_model.macd_sm import MacdSignalModel
from abmacd.strategy_model.trader_model.v2_tm import V2Trader


class ProxyCallable(Protocol):
    def __call__(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        net: bool = False,
    ): ...


class SingleMacdStrategyModel:
    macd_signal_model: MacdSignalModel
    trader: V2Trader
    current_cross_state = 0

    def __init__(
            self,
            buy: ProxyCallable,
            short: ProxyCallable,
            sell: ProxyCallable,
            cover: ProxyCallable,
            fixed_size: float,
            pricetick: float,
            debug: bool = False,
    ):
        self.trader = V2Trader(fixed_size, pricetick, buy, short, sell, cover, debug)
        self.macd_signal_model = MacdSignalModel("Single")

    def update_macd_signal(self, fast_macd0: float, slow_macd0: float):
        self.macd_signal_model.update(fast_macd0, slow_macd0)
        if self.current_cross_state == 0:
            if self.macd_signal_model.cross_over():
                self.current_cross_state = 1

            if self.macd_signal_model.cross_below():
                self.current_cross_state = -1

        # cross over -> cross below
        if self.current_cross_state == 1 and self.macd_signal_model.cross_below():
            self.current_cross_state = -1

        # cross below -> cross over
        if self.current_cross_state == -1 and self.macd_signal_model.cross_over():
            self.current_cross_state = 1

    def update_pos(self, pos: int):
        self.trader.update_pos(pos)

    def handler(self, price: float):
        # OPEN
        if self.trader.pos == 0:
            if self.macd_signal_model.macd_gt_zero():
                if self.macd_signal_model.cross_below():
                    self.trader._short(price, self.trader.fixed_size, "A_OPEN_SHORT")

                if self.macd_signal_model.cross_over():
                    self.trader._buy(price, self.trader.fixed_size, "A_OPEN_LONG")
                return

        # ClOSE - SHORT
        if self.trader.pos < 0:
            if self.current_cross_state == 1:
                self.trader._cover(price, "A_CLOSE_SHORT")
                return

            if self.macd_signal_model.macd_gt_zero() and self.macd_signal_model.cross_over():
                self.trader._cover(price, "A_RB_LONG")
                self.trader._buy(price, self.trader.fixed_size, "A_RB_LONG")

        # ClOSE - LONG
        if self.trader.pos > 0:
            if self.macd_signal_model.macd_gt_zero() and self.macd_signal_model.cross_below():
                self.trader._sell(price, "A_RB_SHORT")
                self.trader._short(price, self.trader.fixed_size, "A_RB_SHORT")
