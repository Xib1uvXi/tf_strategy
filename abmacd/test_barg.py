from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    ArrayManager,
)

from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime

from ft_bargenerator import BarGenerator
from vnpy.trader.constant import Interval

class DoubleMaStrategy(CtaTemplate):
    author = "用Python的交易员"


    parameters = []
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg15 = BarGenerator(self.on_bar, 15, self.on_15min_bar, interval=Interval.MINUTE)
        # self.bg15 = BarGenerator(self.on_bar, 1, self.on_15min_bar, interval=Interval.HOUR)
        self.am15 = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(1)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """

        pass

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        self.bg15.update_bar(bar)

        self.put_event()


    def on_15min_bar(self, bar: BarData):
        """"""
        self.am15.update_bar(bar)
        if not self.am15.inited:
            return

        print(bar.datetime, bar.close_price)

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

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="RU88.SHFE",
    interval="1m",
    start=datetime(2021, 1, 1),
    end=datetime(2022, 3, 15),
    rate=0.3 / 10000,
    slippage=0.2,
    size=30,
    pricetick=0.2,
    capital=1_000_000,
)
engine.add_strategy(DoubleMaStrategy, {})

engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()