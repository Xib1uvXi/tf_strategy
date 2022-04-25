from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
)
from vnpy.trader.object import (
    TickData,
    BarData,
    TradeData,
    OrderData,
)
from vnpy.trader.constant import Direction, Offset, Status

from abmacd.abmacd_v3 import ABMACDStrategy, ABMACDStrategyConfig
from abmacd.strategy_model.riskctl_model.stop_loss import Stoploss
from abmacd.strategy_model.signal_model.macd_sm import ABMacdAction

from abmacd.ft_bargenerator import BarGenerator
from abmacd.strategy_model.trader_model.v2_tm import V2Trader


class ABMACDStrategyByVN(CtaTemplate):
    """"""
    author = "Xib"

    mswap_enable = False
    stoploss_enable = False

    sm_debug = False

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
                  "b_signal_period", "size", "macd_lvl", "b_ma_window", 
                  "mswap_enable", "stoploss_enable", "sm_debug"
                ]

    variables = ["a_fast_macd0", "a_fast_macd1", "a_slow_macd0", "a_slow_macd1",
                 "b_fast_macd0", "b_fast_macd1", "b_slow_macd0", "b_slow_macd1", "size", "macd_lvl"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.write_log(strategy_name)
        self.write_log(setting)

        config = ABMACDStrategyConfig(self.mswap_enable, self.b_ma_window, self.a_fast_window, self.a_slow_window,
                                      self.a_signal_period, self.b_fast_window, self.b_slow_window, self.b_signal_period, self.macd_lvl)

        self.sm = ABMACDStrategy(config, self.mock_action_handler)

        self.cancel_bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)

        self.long_stoploss = Stoploss(1, 0.02)

        self.short_stoploss = Stoploss(-1, 0.02)

        self.trader = V2Trader(self.size, self.get_pricetick(), self.buy, self.short, self.sell, self.cover, self.sm_debug)

    def on_15min_bar(self, bar: BarData):
        """
        Callback of new 15 min bar data update.
        """
        self.cancel_all()

    def mock_action_handler(self, price, action):
        if action is ABMacdAction.EMPTY:
            return

        if action is ABMacdAction.A_OPEN_LONG:
            self.trader._open_long(price, action)

        elif action is ABMacdAction.A_OPEN_SHORT:
            self.trader._open_short(price, action)

        elif action is ABMacdAction.B_CLOSE_LONG:
            self.trader._close_long(price, action, is_blvl=True)

        elif action is ABMacdAction.B_CLOSE_SHORT:
            self.trader._close_short(price, action)

        elif action is ABMacdAction.B_OPEN_LONG_A:
            self.trader._open_long(price, action, is_back=True)

        elif action is ABMacdAction.B_OPEN_SHORT_A:
            self.trader._open_short(price, action, is_back=True)

        elif action is ABMacdAction.B_OPEN_LONG:
            self.trader._open_long(price, action, is_blvl=True)

        elif action is ABMacdAction.A_RB_LONG:
            self.trader._rollback_short_to_long(price, action)

        elif action is ABMacdAction.A_RB_SHORT:
            self.trader._rollback_long_to_short(price, action)

        elif action is ABMacdAction.A_CLOSE_SHORT:
            self.trader._close_short(price, action)

        elif action is ABMacdAction.MS_CLOSE_SHORT:
             self.trader._close_short(price, action)

        elif action is ABMacdAction.MS_CLOSE_LONG:
            self.trader._close_long(price, action)

        elif action is ABMacdAction.MUST_CLOSE:
            if self.pos != 0:
                assert self.last_bar
                if self.pos > 0:
                    self.trader._close_long(price, action)

                if self.pos < 0:
                    self.trader._close_short(price, action)

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

        self.trader.update_pos(self.pos)

        if self.stoploss_enable:
            if self.long_stoploss.need_close(bar.close_price):
                self.sell(bar.close_price, abs(self.pos))
            if self.short_stoploss.need_close(bar.close_price):
                self.cover(bar.close_price, abs(self.pos))

        self.sm.on_bar(bar)

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        if order.status == Status.CANCELLED:
            if order.offset == Offset.CLOSE:
                assert self.last_bar
                if order.direction == Direction.LONG:
                    self.cover(self.last_bar.close_price, order.volume)

                if order.direction == Direction.SHORT:
                    self.sell(self.last_bar.close_price, order.volume)

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        if self.stoploss_enable:
            self._update_stoploss_by_trade(trade)

    def _update_stoploss_by_trade(self, trade: TradeData):
        if trade.direction is Direction.LONG and trade.offset is Offset.OPEN:
            self.long_stoploss.open(1, trade.price, trade.volume)

        if trade.direction is Direction.SHORT and trade.offset is Offset.OPEN:
            self.short_stoploss.open(-1, trade.price, trade.volume)

        if trade.direction is Direction.LONG and trade.offset is Offset.CLOSE:
            self.short_stoploss.close(-1)

        if trade.direction is Direction.SHORT and trade.offset is Offset.CLOSE:
            self.long_stoploss.close(1)

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
