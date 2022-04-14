from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    ArrayManager,
)

from vnpy.trader.constant import Interval
from abmacd.strategy_model.v2_abmacd_ma_filter import ABMacdStrategyModel
from abmacd.ft_bargenerator import BarGenerator


class ABMACDStrategy(CtaTemplate):
    """"""
    author = "Xib"

    b_ma_window = 10

    a_fast_window = 12
    a_slow_window = 26
    a_signal_period = 9

    b_fast_window = 12
    b_slow_window = 26
    b_signal_period = 9

    a_fast_macd0 = 0.0
    a_fast_macd1 = 0.0
    a_slow_macd0 = 0.0
    a_slow_macd1 = 0.0
    b_fast_macd0 = 0.0
    b_fast_macd1 = 0.0
    b_slow_macd0 = 0.0
    b_slow_macd1 = 0.0

    macd_lvl = ""
    size = 10.0
    sm_debug = False

    last_tick = None
    last_bar = None

    parameters = ["a_fast_window", "a_slow_window",
                  "a_signal_period", "b_fast_window", "b_slow_window",
                  "b_signal_period", "size", "macd_lvl", "sm_debug", "b_ma_window"]

    variables = ["a_fast_macd0", "a_fast_macd1", "a_slow_macd0", "a_slow_macd1",
                 "b_fast_macd0", "b_fast_macd1", "b_slow_macd0", "b_slow_macd1", "size", "macd_lvl"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.write_log(strategy_name)
        self.write_log(setting)

        self.sm = ABMacdStrategyModel(
            self.buy, self.short, self.sell, self.cover, self.size, self.get_pricetick(), self.sm_debug)

        self.init_bar_generator(self.macd_lvl)

        self.am_a = ArrayManager()
        self.am_b = ArrayManager()

    def init_bar_generator(self, level):
        if level == "1d4h":
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
            self.bg_b = BarGenerator(
                self.on_bar, 4, self.on_b_level_bar, interval=Interval.HOUR)
        elif level == "1d1h":
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
            self.bg_b = BarGenerator(
                self.on_bar, 1, self.on_b_level_bar, interval=Interval.HOUR)
        elif level == "15min5min":
            self.bg_a = BarGenerator(self.on_bar, 15, self.on_a_level_bar)
            self.bg_b = BarGenerator(self.on_bar, 5, self.on_b_level_bar)
        else:
            self.bg_a = BarGenerator(
                self.on_bar, 1, self.on_a_level_bar, interval=Interval.HOUR)
            self.bg_b = BarGenerator(self.on_bar, 15, self.on_b_level_bar)

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(3)

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

        self.sm.update_pos(self.pos)
        self.sm.handler(bar.close_price)

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
        self.am_b.update_bar(bar)
        if not self.am_b.inited:
            return

        dif, dea, hist = self.am_b.macd(
            self.b_fast_window, self.b_slow_window, self.b_signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_macd_signal(fast_macd0, slow_macd0)

        ma_filter = self.am_b.sma(self.b_ma_window, True)

        self.sm.update_ma_signal(ma_filter[-1])

    def on_a_level_bar(self, bar: BarData):
        self.am_a.update_bar(bar)
        if not self.am_a.inited:
            return

        dif, dea, hist = self.am_a.macd(
            self.a_fast_window, self.a_slow_window, self.a_signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        self.sm.update_macd_signal(fast_macd0, slow_macd0, True)
