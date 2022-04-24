from abmacd.strategy_model.mswap_helper import MswapHelper
from abmacd.strategy_model.signal_model.macd_sm import ABMacdAction, ABMacdSignalModel
from abmacd.strategy_model.signal_model.ma_filter_sm import MaFilterSignalModel
from abmacd.strategy_model.stoploss_helper import StoplossHelper
from abmacd.strategy_model.trader_model.v2_tm import V2Trader

class ABMacdStrategyModelV3:
    # signal model
    abmacd_sm: ABMacdSignalModel
    b_ma_filter: MaFilterSignalModel
    # helper
    mswap: MswapHelper

    def __init__(self, abmacd_sm: ABMacdSignalModel, b_ma_filter: MaFilterSignalModel, mswap_helper: MswapHelper):
        self.abmacd_sm = abmacd_sm
        self.b_ma_filter = b_ma_filter
        self.mswap = mswap_helper

    def update_macd_signal(self, fast_macd0: float, slow_macd0: float, big_level=False):
        if big_level:
            self.abmacd_sm.update_a_signal_value(fast_macd0, slow_macd0)
            return
        
        self.abmacd_sm.update_b_signal_value(fast_macd0, slow_macd0)

    def update_ma_signal(self, ma: float):
        self.b_ma_filter.update_ma(ma)

        
    def handler(self, price: float, bar_month: int, bar_day: int) -> ABMacdAction:
        self.b_ma_filter.update_price(price)
        action = self.abmacd_sm.exec()
        self.last_action = action

        # print("raw action: ", action)
        if action is None:
            print(self.abmacd_sm.a_sv_init, self.abmacd_sm.b_sv_init, self.abmacd_sm.direction)

        
        if self.mswap.is_swap_month(bar_month):
            if self.mswap.is_only_close_day(bar_day):
                return self._close_handler(action)
            
            if self.mswap.is_must_close_day(bar_day):
                return ABMacdAction.MUSTCLOSE
        
        return self._ma_filter_handler(action)


    def _close_handler(self, action: ABMacdAction) -> ABMacdAction:
        valid_action = [
            ABMacdAction.EMPTY, 
            ABMacdAction.B_CLOSE_LONG, 
            ABMacdAction.B_CLOSE_SHORT, 
            ABMacdAction.A_RB_LONG, 
            ABMacdAction.A_RB_SHORT, 
            ABMacdAction.A_CLOSE_SHORT
        ]
        
        if action not in valid_action:
            return ABMacdAction.EMPTY
        
        return action
    
    def _ma_filter_handler(self, action: ABMacdAction) -> ABMacdAction:
        if action is ABMacdAction.B_OPEN_LONG_A:
            if self.b_ma_filter.filter_long():
                return action
            else:
                return ABMacdAction.EMPTY
        
        if action is ABMacdAction.B_OPEN_LONG:
            if self.b_ma_filter.filter_long():
                return action
            else:
                return ABMacdAction.EMPTY
        
        if action is ABMacdAction.B_OPEN_SHORT_A:
            if self.b_ma_filter.filter_short():
                return action
            else:
                return ABMacdAction.EMPTY
        
        return action

