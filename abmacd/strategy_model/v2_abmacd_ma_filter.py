
from abmacd.strategy_model.riskctl_model.stop_loss import Stoploss
from abmacd.strategy_model.signal_model.macd_sm import ABMacdAction, ABMacdSignalModel
from abmacd.strategy_model.signal_model.ma_filter_sm import MaFilterSignalModel
from typing import Callable

from abmacd.strategy_model.trader_model.v2_tm import V2Trader

class ABMacdStrategyModel:
    abmacd_sm: ABMacdSignalModel
    b_ma_filter: MaFilterSignalModel
    trader: V2Trader
    stoploss_enabled: bool
    long_stoploss: Stoploss
    short_stoploss: Stoploss

    last_action: ABMacdAction

    def __init__(self, buy: Callable, short: Callable, sell: Callable, cover: Callable, fixed_size: float, pricetick: float, stoploss_enable: bool = False, debug: bool = False):
        self.trader = V2Trader(fixed_size, pricetick, buy, short, sell, cover, debug)
        self.abmacd_sm = ABMacdSignalModel()
        self.b_ma_filter = MaFilterSignalModel()
        self.stoploss_enabled = stoploss_enable
        self.long_stoploss = Stoploss(1, 0.02)
        self.short_stoploss = Stoploss(-1, 0.02)

    def update_pos(self, pos: int):
        self.trader.update_pos(pos)
    
    def update_macd_signal(self, fast_macd0: float, slow_macd0: float, big_level=False):
        if big_level:
            self.abmacd_sm.update_a_signal_value(fast_macd0, slow_macd0)
            return
        
        self.abmacd_sm.update_b_signal_value(fast_macd0, slow_macd0)

    def update_ma_signal(self, ma: float):
        self.b_ma_filter.update_ma(ma)
    
    def _handle_stoploss(self, price: float):
        if self.long_stoploss.need_close(price):
            self.trader._sell(price, "做多止损")
        if self.short_stoploss.need_close(price):
            self.trader._cover(price, "做空止损")

    def only_close_handler(self, price: float):
        if self.stoploss_enabled:
            self._handle_stoploss(price)

        action = self.abmacd_sm.exec()
        self.b_ma_filter.update_price(price)

        # filter EMPTY ACTION
        if action is ABMacdAction.EMPTY:
            self.last_action = action
            return
        
        # other filter??
        if action is ABMacdAction.B_CLOSE_LONG:
            self.trader._close_long(price, action, is_blvl=True)

        elif action is ABMacdAction.B_CLOSE_SHORT:
            self.trader._close_short(price, action)
        
        # elif action is ABMacdAction.B_CLOSE_SHORT_V2:
        #     self.trader._close_short(price, action)

        elif action is ABMacdAction.A_RB_LONG:
            self.trader._close_short(price, action)

        elif action is ABMacdAction.A_RB_SHORT:
            self.trader._rollback_long_to_short(price, action)
        
        elif action is ABMacdAction.A_CLOSE_SHORT:
            self.trader._close_long(price, action, is_blvl=False)
        
        self.last_action = action
        return


    def handler(self, price: float):
        if self.stoploss_enabled:
            self._handle_stoploss(price)

        action = self.abmacd_sm.exec()
        self.b_ma_filter.update_price(price)

        # filter EMPTY ACTION
        if action is ABMacdAction.EMPTY:
            self.last_action = action
            return
        
        # other filter??
        if action is ABMacdAction.A_OPEN_LONG:
            self.trader._open_long(price, action)

        elif action is ABMacdAction.A_OPEN_SHORT:
            self.trader._open_short(price, action)

        elif action is ABMacdAction.B_CLOSE_LONG:
            self.trader._close_long(price, action, is_blvl=True)

        elif action is ABMacdAction.B_CLOSE_SHORT:
            self.trader._close_short(price, action)
        
        # elif action is ABMacdAction.B_CLOSE_SHORT_V2:
        #     self.trader._close_short(price, action)

        elif action is ABMacdAction.B_OPEN_LONG_A:
            if self.b_ma_filter.filter_long():
                self.trader._open_long(price, action, is_back=True)

        elif action is ABMacdAction.B_OPEN_SHORT_A:
            if self.b_ma_filter.filter_short():
                self.trader._open_short(price, action, is_back=True)

        elif action is ABMacdAction.B_OPEN_LONG:
            if self.b_ma_filter.filter_long():
                self.trader._open_long(price, action, is_blvl=True)

        elif action is ABMacdAction.A_RB_LONG:
            self.trader._rollback_short_to_long(price, action)

        elif action is ABMacdAction.A_RB_SHORT:
            self.trader._rollback_long_to_short(price, action)
        
        elif action is ABMacdAction.A_CLOSE_SHORT:
            self.trader._close_short(price, action)
        
        self.last_action = action
        return


