from calendar import month
from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
)

from vnpy.trader.constant import Interval, Direction, Offset, Status

from abmacd.abmacd_v3 import ABMACDStrategy, ABMACDStrategyConfig
from abmacd.strategy_model.signal_model.macd_sm import ABMacdAction

from abmacd.ft_bargenerator import BarGenerator

class ABMACDStrategyByVN(CtaTemplate):
    """"""
    author = "Xib"

    mswap_enable = False

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

    last_tick = None
    last_bar = None
    target_pos: float = 0


    parameters = ["a_fast_window", "a_slow_window",
                  "a_signal_period", "b_fast_window", "b_slow_window",
                  "b_signal_period", "size", "macd_lvl",  "b_ma_window", "mswap_enable"]

    variables = ["a_fast_macd0", "a_fast_macd1", "a_slow_macd0", "a_slow_macd1",
                 "b_fast_macd0", "b_fast_macd1", "b_slow_macd0", "b_slow_macd1", "size", "macd_lvl"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.write_log(strategy_name)
        self.write_log(setting)

        config = ABMACDStrategyConfig()
        config.a_fast_window = self.a_fast_window
        config.a_slow_window = self.a_slow_window
        config.a_signal_period = self.a_signal_period
        config.b_fast_window = self.b_fast_window
        config.b_slow_window = self.b_slow_window
        config.b_signal_period = self.b_signal_period
        config.b_ma_window = self.b_ma_window
        config.macd_lvl = self.macd_lvl
        config.mswap_enable = self.mswap_enable

        self.sm = ABMACDStrategy(config, self.mock_action_handler)

        self.cancel_bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)

    def on_15min_bar(self, bar: BarData):
        """
        Callback of new 15 min bar data update.
        """
        self.cancel_all()

    def mock_action_handler(self, price, action):
        if action is ABMacdAction.EMPTY:
            return

        if action is ABMacdAction.A_OPEN_LONG:
            self._open_long(price)
        elif action is ABMacdAction.A_OPEN_SHORT:
            self._open_short(price)
        elif action is ABMacdAction.B_CLOSE_LONG:
            self._close_long(price, is_blvl=True)

        elif action is ABMacdAction.B_CLOSE_SHORT:
            self._close_short(price)       

        elif action is ABMacdAction.B_OPEN_LONG_A:
            self._open_long(price, is_back=True)

        elif action is ABMacdAction.B_OPEN_SHORT_A:
            self._open_short(price, is_back=True)

        elif action is ABMacdAction.B_OPEN_LONG:
            self._open_long(price, is_blvl=True)

        elif action is ABMacdAction.A_RB_LONG:
            self._rollback_short_to_long(price)

        elif action is ABMacdAction.A_RB_SHORT:
            self._rollback_long_to_short(price)
        
        elif action is ABMacdAction.A_CLOSE_SHORT:
            self._close_short(price)

        elif action is ABMacdAction.MUSTCLOSE:
            if self.pos != 0:
                if self.pos > 0:
                    self.sell(self.last_bar.close_price, abs(self.pos))
                
                if self.pos < 0:
                    self.cover(self.last_bar.close_price, abs(self.pos))

        return

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
        pass

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        self.last_bar = bar

        self.cancel_bg.update_bar(bar)

        self.sm.on_bar(bar)

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        if order.status == Status.CANCELLED:
            if order.offset == Offset.CLOSE:
                if order.direction == Direction.LONG:
                    self.cover(self.last_bar.close_price, order.volume)
                
                if order.direction == Direction.SHORT:
                    self.sell(self.last_bar.close_price, order.volume)

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        pass


    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass

    def _open_long(self, price: float, is_back: bool = False, is_blvl: bool = False):
        if self.pos < 0:
            return
        
        if (not is_blvl) and abs(self.pos) != 0:
            return

        if is_back:
            self.buy(price, self._target_pos())
            self._reset_target_pos()
        else:
            self.buy(price, self.size)
    
    def _open_short(self, price: float, is_back: bool = False):
        if abs(self.pos) != 0:
            return

        if is_back:
            self.short(price, self.size)
        else:
            self.short(price, self.size)
    
    def _close_long(self, price: float, is_blvl: bool = False):
        if abs(self.pos) == 0:
            return

        if self.pos > 0:
            if is_blvl:
                self._update_target_pos(self.pos)

            self.sell(price, abs(self.pos))

    def _close_short(self, price: float):
        if abs(self.pos) == 0:
            return

        if self.pos < 0:
            self.cover(price, abs(self.pos))

    def _rollback_short_to_long(self, price: float):
        if self.pos > 0:
            return
        
        if self.pos == 0:
            self.buy(price, self.size)
            return
        
        if self.pos < 0:
            self.cover(price, abs(self.pos))
            self.buy(price, self.size)
    
    def _rollback_long_to_short(self, price: float):
        if self.pos < 0:
            return

        if self.pos == 0:
            self.short(price, self.size)
            return
        
        if self.pos > 0:
            self.sell(price, abs(self.pos))
            self.short(price, self.size)

    def _target_pos(self) -> float:
        if self.target_pos == 0:
            return self.size

        return abs(self.target_pos)

    def _reset_target_pos(self) -> None:
        self.target_pos = 0

    def _update_target_pos(self, pos: int) -> None:
        self.target_pos = pos