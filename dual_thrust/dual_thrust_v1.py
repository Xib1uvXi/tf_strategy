from dataclasses import dataclass
from typing import Callable

from dual_thrust.ft_bargenerator import BarGenerator
from vnpy.trader.constant import Interval

from vnpy_ctastrategy import (
    ArrayManager,
    BarData,
    TickData
)
from dual_thrust.strategy_model.signal_model.dual_thrust_sm import DualThrustSignalModel

from dual_thrust.strategy_model.v1_dual_thrust import DualThrustStrategyModel

@dataclass
class DualThrustStrategyConfig:
    n: int = 5
    k1: float = 0.2
    k2: float = 0.2


class DualThrustStrategy:
    config: DualThrustStrategyConfig
    action_handler: Callable
    last_bar = None

    def __init__(self, config: DualThrustStrategyConfig, action_handler: Callable):
        self.action_handler = action_handler
        self.config = config
        self.sm = DualThrustStrategyModel(DualThrustSignalModel(self.config.k1, self.config.k2))
        self.init_bar_generator()

    def init_bar_generator(self):
        self.bg = BarGenerator(self.on_bar)
        self.bg_1day = BarGenerator(
                self.on_bar, 1, self.on_bar_1day, interval=Interval.DAILY)
        
        self.am = ArrayManager(self.config.n)
    
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)
        self.bg_1day.update_tick(tick)

    def on_bar(self, bar: BarData):
        self.bg_1day.update_bar(bar)

        if self.last_bar is None:
            self.last_bar = bar

        open_price: float = 0
        if self.bg_1day.hour_bar is None:
            open_price = bar.open_price
        else:
            open_price = self.bg_1day.hour_bar.open_price

        self.sm.update_open_price(open_price)
       
        self.last_bar = bar

        action = self.sm.handler(bar.datetime.time(), bar.close_price)

        self.action_handler(action, bar.close_price)

    
    def on_bar_1day(self, bar: BarData):
        self.am.update_bar(bar)

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.sm.update_signal_value(self.am.high_array.max(), self.am.low_array.min(),self.am.close_array.max(), self.am.close_array.min())