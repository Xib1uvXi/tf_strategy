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
from abmacd_strategy_model import ABMacdStrategyModel

from barg import MACDBarGenerator

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

    size = 0.0
    
    tick_add = 0.0
    last_tick = None
    last_bar = None

    parameters = ["fast_window", "slow_window", "signal_period", "size", "tick_add"]

    variables = ["a_fast_macd0", "a_fast_macd1", "a_slow_macd0", "a_slow_macd1", 
    "b_fast_macd0", "b_fast_macd1", "b_slow_macd0", "b_slow_macd1", "a_open_init"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.init_1h15min()

        self.sm = ABMacdStrategyModel(self.buy, self.short, self.sell, self.cover, self.size, self.get_pricetick())
    
    def init_1h15min(self):
        # A level 
        self.bg_a = MACDBarGenerator(self.on_bar, 1, self.on_a_level_bar, interval=Interval.HOUR)
        self.am_a = ArrayManager()

        # B level
        self.bg_b = BarGenerator(self.on_bar, 15, self.on_b_level_bar)
        self.am_b = ArrayManager()
    
    def init_1d1h(self):
        # A level 
        self.bg_a = BarGenerator(self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
        self.am_a = ArrayManager()

        # B level
        self.bg_b = MACDBarGenerator(self.on_bar, 1, self.on_b_level_bar, interval=Interval.HOUR)
        self.am_b = ArrayManager()
    
    def init_1d4h(self):
        # A level 
        self.bg_a = BarGenerator(self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
        self.am_a = ArrayManager()

        # B level
        self.bg_b = MACDBarGenerator(self.on_bar, 4, self.on_b_level_bar, interval=Interval.HOUR)
        self.am_b = ArrayManager()
    
    # ---------------------------------
    def init_1dx(self):
        # A level 
        self.bg_a = BarGenerator(self.on_bar, 1, self.on_a_level_bar, interval=Interval.DAILY)
        self.am_a = ArrayManager()

        # B level
        # self.bg_b = MACDBarGenerator(self.on_bar, 1, self.on_b_level_bar, interval=Interval.HOUR)
        self.bg_b = BarGenerator(self.on_bar, 50, self.on_b_level_bar)
        self.am_b = ArrayManager()
    
    # ---------------------------------
    def init_xhxm(self):
        # A level 
        self.bg_a = BarGenerator(self.on_bar, 2, self.on_a_level_bar, interval=Interval.HOUR)
        self.am_a = ArrayManager()

        # B level
        self.bg_b = BarGenerator(self.on_bar, 30, self.on_b_level_bar)
        self.am_b = ArrayManager()


    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        # TODO need fix
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
        self.sm.exec(bar.close_price)
    
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

        self.sm.update_signal(fast_macd0, slow_macd0)


    def on_a_level_bar(self, bar: BarData):
        # self.cancel_all()

        self.am_a.update_bar(bar)
        if not self.am_a.inited:
            return

        dif, dea, hist = self.am_a.macd(self.fast_window, self.slow_window, self.signal_period, True)
        fast_macd0 = dif[-1]
        slow_macd0 = dea[-1]

        #print(bar.datetime, fast_macd0, slow_macd0)

        self.sm.update_signal(fast_macd0, slow_macd0, True)
