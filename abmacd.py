from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)

from vnpy.trader.constant import Interval
from vnpy.trader.constant import Status
from vnpy_ctastrategy.base import EngineType
from abmacd_dt import MacdDecision

from barg import MACDBarGenerator
from macd_sm import ABMacdSignalModel

class ABMACDStrategy(CtaTemplate):
    """"""
    author = "Xib"

    fast_window = 12
    slow_window = 26
    signal_period = 9

    a_fast_macd0 = 0.0
    a_fast_macd1 = 0.0
    a_slow_macd0 = 0.0
    a_slow_macd1 = 0.0
    b_fast_macd0 = 0.0
    b_fast_macd1 = 0.0
    b_slow_macd0 = 0.0
    b_slow_macd1 = 0.0

    size = 1.0
    
    tick_add = 0.0
    last_tick = None
    last_bar = None

    parameters = ["fast_window", "slow_window", "signal_period", "size", "tick_add"]

    variables = ["a_fast_macd0", "a_fast_macd1", "a_slow_macd0", "a_slow_macd1", 
    "b_fast_macd0", "b_fast_macd1", "b_slow_macd0", "b_slow_macd1", "a_open_init"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # A level 
        self.bg_a = MACDBarGenerator(self.on_bar, 1, self.on_a_level_bar, interval=Interval.HOUR)
        self.am_a = ArrayManager()

        # B level
        self.bg_b = BarGenerator(self.on_bar, 15, self.on_b_level_bar)
        self.am_b = ArrayManager()

        self.sm = ABMacdSignalModel()
        self.dt = MacdDecision(self.buy, self.short, self.sell, self.cover)


    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(20)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """

        self.last_tick = tick

        self.bg_b.update_tick(tick)
        self.bg_a.update_tick(tick)


    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        self.last_bar = bar

        self.bg_b.update_bar(bar)
        self.bg_a.update_bar(bar)

        action = self.sm.exec()
        self.dt.dt(self.pos, action, bar.close_price, self.size)
    
    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass

    def on_b_level_bar(self, bar: BarData):
        # self.cancel_all()

        self.am_b.update_bar(bar)
        if not self.am_b.inited:
            return

        dif, dea, hist = self.am_b.macd(self.fast_window, self.slow_window, self.signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_b_signal_value(fast_macd0, slow_macd0)


    def on_a_level_bar(self, bar: BarData):
        # self.cancel_all()

        self.am_a.update_bar(bar)
        if not self.am_a.inited:
            return

        dif, dea, hist = self.am_a.macd(self.fast_window, self.slow_window, self.signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_a_signal_value(fast_macd0, slow_macd0)
