
from typing import Callable
from abmacd.strategy_model.builder import NewABMacdStrategyModel
from abmacd.strategy_model.signal_model.macd_sm import ABMacdAction
from abmacd.strategy_model.v3_abmacd import ABMacdStrategyModelV3

from vnpy_ctastrategy import (
    TickData,
    BarData,
    ArrayManager,
)

from abmacd.ft_bargenerator import BarGenerator
from vnpy.trader.constant import Interval

class ABMACDStrategyConfig:
    mswap_enable: bool
    # b_ma_window
    b_ma_window: int

    a_fast_window: int
    a_slow_window: int
    a_signal_period: int
    b_fast_window: int
    b_slow_window: int
    b_signal_period: int

    macd_lvl: str

class ABMACDStrategy:
    config: ABMACDStrategyConfig
    sm: ABMacdStrategyModelV3

    action_handler: Callable

    last_tick = None
    last_bar = None

    def __init__(self, config: ABMACDStrategyConfig, action_handler: Callable):
        self.config = config
        
        self.sm = NewABMacdStrategyModel(config.mswap_enable)

        self.am_a = ArrayManager()
        self.am_b = ArrayManager()

        self.init_bar_generator()

        self.action_handler = action_handler

    def init_bar_generator(self):
        if self.config.macd_lvl == "1d4h":
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
            self.bg_b = BarGenerator(
                self.on_bar, 4, self.on_b_level_bar, interval=Interval.HOUR)
        elif self.config.macd_lvl == "1d1h":
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
            self.bg_b = BarGenerator(
                self.on_bar, 1, self.on_b_level_bar, interval=Interval.HOUR)
        else:
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.HOUR)
            self.bg_b = BarGenerator(self.on_bar, 15, self.on_b_level_bar)

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """

        self.last_tick = tick

        self.bg_b.update_tick(tick)
        self.bg_a.update_tick(tick)

    def on_bar(self, bar: BarData):
        self.last_bar = bar

        self.bg_b.update_bar(bar)
        self.bg_a.update_bar(bar)

        action = self.sm.handler(bar.close_price, bar.datetime.month, bar.datetime.day)

        self.action_handler(bar.close_price, action)

    def on_b_level_bar(self, bar: BarData):
        self.am_b.update_bar(bar)
        if not self.am_b.inited:
            return

        dif, dea, hist = self.am_b.macd(
            self.config.b_fast_window, self.config.b_slow_window, self.config.b_signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_macd_signal(fast_macd0, slow_macd0)

        ma_filter = self.am_b.sma(self.config.b_ma_window, True)

        self.sm.update_ma_signal(ma_filter[-1])
    
    def on_a_level_bar(self, bar: BarData):
        self.am_a.update_bar(bar)
        if not self.am_a.inited:
            return

        dif, dea, hist = self.am_a.macd(
            self.config.a_fast_window, self.config.a_slow_window, self.config.a_signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_macd_signal(fast_macd0, slow_macd0, True)