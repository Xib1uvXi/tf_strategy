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
from dual_thrust.dual_thrust_v1 import DualThrustStrategyConfig, DualThrustStrategy

from dual_thrust.ft_bargenerator import BarGenerator
from dual_thrust.strategy_model.signal_model.dual_thrust_sm import DualThrustSignalModel
from dual_thrust.strategy_model.v1_dual_thrust import DualThrustAction, DualThrustStrategyModel


class DualThrustStrategyByVN(CtaTemplate):
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

        config = DualThrustStrategyConfig(n=self.n, k1=self.k1, k2=self.k2)

        self.sm = DualThrustStrategy(config, self.action_handler)

        self.bg = BarGenerator(self.on_bar)

        self.cancel_bg = BarGenerator(self.on_bar, 5, self.on_15min_bar)
    
    def on_15min_bar(self, bar: BarData):
        """
        Callback of new 15 min bar data update.
        """
        self.cancel_all()

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

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        
        self.sm.on_bar(bar)

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
