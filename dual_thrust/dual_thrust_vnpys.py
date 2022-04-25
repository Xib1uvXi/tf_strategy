from datetime import time
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

from dual_thrust.ft_bargenerator import BarGenerator
from dual_thrust.strategy_model.signal_model.dual_thrust_sm import DualThrustSignalModel
from dual_thrust.strategy_model.v1_dual_thrust import DualThrustAction, DualThrustStrategyModel


class DualThrustStrategy(CtaTemplate):
    """"""
    author = "Xib"

    n = 2
    k1: float = 0.2
    k2: float = 0.2

    size = 10.0

    exit_time = time(hour=14, minute=55)

    last_bar = None

    parameters = ['n', 'k1', 'k2', 'size']
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar)

        self.bg_1day = BarGenerator(
                self.on_bar, 1, self.on_bar_1day, interval=Interval.DAILY)
        self.am = ArrayManager(self.n)

        self.sm = DualThrustStrategyModel(DualThrustSignalModel(self.k1, self.k2))

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

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
        self.bg.update_tick(tick)

    def on_bar_1day(self, bar: BarData):
        self.am.update_bar(bar)

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.sm.update_signal_value(self.am.high_array.max(), self.am.low_array.min(),self.am.close_array.max(), self.am.close_array.min())

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.cancel_all()

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

    def action_handler(self,action: DualThrustAction, price: float):
        if action is DualThrustAction.EMPTY:
            return
        
        elif action is DualThrustAction.EXITTIME_CLOSE:
            if self.pos > 0:
                self.sell(price * 0.99, abs(self.pos))
            
            elif self.pos < 0:
                self.cover(price * 1.01, abs(self.pos))
            
            return
        
        elif action is DualThrustAction.TO_LONG:
            if self.pos == 0:
                self.buy(price, self.size)
                return
            
            if self.pos > 0:
                return
            
            if self.pos < 0:
                self.cover(price, abs(self.pos))
                self.buy(price, self.size)
                return
        
        elif action is DualThrustAction.TO_SHORT:
            if self.pos == 0:
                self.short(price, self.size)
                return
            
            if self.pos < 0:
                return
            
            if self.pos > 0:
                self.sell(price, abs(self.pos))
                self.short(price, self.size)
                return

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
