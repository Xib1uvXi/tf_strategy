from .signal_model.dual_thrust_sm import DualThrustSignalModel
from datetime import time

from enum import Enum


class DualThrustAction(Enum):
    EXITTIME_CLOSE = "日内平仓"
    EMPTY = "EMPTY"

    TO_LONG = "多"
    TO_SHORT = "空"


class DualThrustStrategyModel:
    open_price_init: bool
    signal_value_init: bool

    dual_thrust_sm: DualThrustSignalModel

    exit_time = time(hour=14, minute=55)

    def __init__(self, sm: DualThrustSignalModel):
        self.dual_thrust_sm = sm
        self.open_price_init = False
        self.signal_value_init = False

    def update_signal_value(self, max_high: float, min_low: float, max_close: float, min_close: float):
        self.dual_thrust_sm.update_signal_value(max_high, min_low, max_close, min_close)
        if not self.signal_value_init:
            self.signal_value_init = True

    def update_open_price(self, open_price: float):
        self.dual_thrust_sm.update_open_price(open_price)
        if not self.open_price_init:
            self.open_price_init = True

    def handler(self, bar_time: time, bar_close_price: float) -> DualThrustAction:

        if not self.open_price_init or not self.signal_value_init:
            return DualThrustAction.EMPTY

        if bar_time < self.exit_time:
            if bar_close_price > self.dual_thrust_sm.long_entry:
                return DualThrustAction.TO_LONG

            if bar_close_price < self.dual_thrust_sm.short_entry:
                return DualThrustAction.TO_SHORT

            return DualThrustAction.EMPTY
        else:
            return DualThrustAction.EXITTIME_CLOSE
