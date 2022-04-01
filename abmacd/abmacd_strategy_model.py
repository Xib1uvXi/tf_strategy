from abmacd.signal_model.macd_sm import ABMacdAction, ABMacdSignalModel
from typing import Callable


class ABMacdStrategyModel:
    fixed_size: float
    pricetick: float
    
    # position
    pos: int
    target_pos: float #long_back & short_back

    signal_model: ABMacdSignalModel

    ma10filter: float

    last_action: ABMacdAction

    # open
    buy: Callable
    short: Callable
    
    # close
    sell: Callable
    cover: Callable
    
    def __init__(self, buy: Callable, short: Callable, sell: Callable, cover: Callable, fixed_size: float, pricetick: float):
        self.fixed_size = fixed_size
        self.pricetick = pricetick
        
        self.pos = 0
        self.target_pos = 0
        self.signal_model = ABMacdSignalModel()

        self.buy = buy
        self.short = short
        self.sell = sell
        self.cover = cover

    # update position
    def update_pos(self, pos: int):
        self.pos = pos
    
    def update_signal(self, fast_macd0: float, slow_macd0: float, big_level=False):
        if big_level:
            self.signal_model.update_a_signal_value(fast_macd0, slow_macd0)
            return
        
        self.signal_model.update_b_signal_value(fast_macd0, slow_macd0)

    def update_ma10filter(self, ma10: float):
        self.ma10filter = ma10
    
    def ma_filter(self, price: float, is_long: bool) -> bool:
        if self.ma10filter is None:
            return False

        if is_long:
            return price > self.ma10filter
        else:
            return price < self.ma10filter


    def exec(self, price: float):
        action = self.signal_model.exec()

        # filter EMPTY ACTION
        if action is ABMacdAction.EMPTY:
            self.last_action = action
            return
        
        # other filter??

        if action is ABMacdAction.A_OPEN_LONG:
            self._handle_open_long(price, action)
        elif action is ABMacdAction.A_OPEN_SHORT:
            self._handle_open_short(price, action)
        elif action is ABMacdAction.B_CLOSE_LONG:
            self._handle_close_long(price, action)
        elif action is ABMacdAction.B_CLOSE_SHORT:
            self._handle_close_short(price, action)
        elif action is ABMacdAction.B_OPEN_LONG_A:
            self._handle_b_long_back(price, action)
        elif action is ABMacdAction.B_OPEN_SHORT_A:
            self._handle_b_short_back(price, action)
        elif action is ABMacdAction.B_OPEN_LONG:
            self._handle_b_long(price, action)
        elif action is ABMacdAction.A_RB_LONG:
            self._handle_a_short_to_long(price, action)
        elif action is ABMacdAction.A_RB_SHORT:
            self._handle_a_long_to_short(price, action)
        elif action is ABMacdAction.A_CLOSE_SHORT:
            self._handle_a_close_short(price, action)
        
        self.last_action = action
        return


    # ------------------------------------LONG------------------------------

    # ABMacdAction.A_OPEN_LONG
    def _handle_open_long(self, price: float, action):
        if abs(self.pos) != 0:
            return
        
        vt_ids = self.buy(price, self.fixed_size)
        self._handle_debug(action, vt_ids, "buy")

    # ABMacdAction.B_CLOSE_LONG
    def _handle_close_long(self, price: float, action):
        if self.pos <= 0:
            return
        
        self.target_pos = self.target_pos + self.pos
        vt_ids = self.sell(price, abs(self.pos))
        self._handle_debug(action, vt_ids, "sell")
    
    # ABMacdAction.B_OPEN_LONG_A
    def _handle_b_long_back(self, price: float, action):
        if self.pos != 0:
            return

        if not self.ma_filter(price, True):
            return

        tmp_size = self.fixed_size

        if self.target_pos > 0:
            tmp_size = self.target_pos

        vt_ids = self.buy(price, tmp_size)
        self.target_pos = 0
        self._handle_debug(action, vt_ids, "buy_back")
    
    # ABMacdAction.B_OPEN_LONG_A
    def _handle_b_long(self, price: float, action):
        if self.pos < 0:
            return

        if not self.ma_filter(price, True):
            return
        
        vt_ids = self.buy(price, self.fixed_size)
        self._handle_debug(action, vt_ids, "b_buy")

    # -------------------------------------SHORT-----------------------------

    # ABMacdAction.A_OPEN_SHORT
    def _handle_open_short(self, price: float, action):
        if abs(self.pos) != 0:
            return
        
        vt_ids = self.short(price, self.fixed_size)
        self._handle_debug(action, vt_ids, "short")
    
    # ABMacdAction.B_CLOSE_SHORT
    def _handle_close_short(self, price: float, action):
        if self.pos >= 0:
            return
        
        self.target_pos = self.target_pos + self.pos
        vt_ids = self.cover(price, abs(self.pos))
        self._handle_debug(action, vt_ids, "cover")
    
    # ABMacdAction.AA_CLOSE_SHORT
    def _handle_a_close_short(self, price: float, action):
        if self.pos >= 0:
            return
        vt_ids = self.cover(price, abs(self.pos))
        self._handle_debug(action, vt_ids, "a_cover")
    
    # ABMacdAction.B_OPEN_SHORT_A
    def _handle_b_short_back(self, price: float, action):
        if self.pos != 0:
            return

        if not self.ma_filter(price, False):
            return
        
        tmp_size = self.fixed_size

        if self.target_pos < 0:
            tmp_size = self.target_pos
        
        vt_ids = self.short(price, abs(tmp_size))
        self.target_pos = 0
        self._handle_debug(action, vt_ids, "short_back")
    
    # -------------------------------------Rollback-----------------------------

    # ABMacdAction.A_RB_LONG
    def _handle_a_short_to_long(self, price: float, action):
        if self.pos > 0:
            return
        
        if self.pos == 0:
            vt_ids = self.buy(price, self.fixed_size)
            self._handle_debug(action, vt_ids, "buy")
            return
        
        if self.pos < 0:
            vt_ids1 = self.cover(self._rollback_cover_price(price), abs(self.pos))
            self.target_pos = 0
            self._handle_debug(action, vt_ids1, "cover")

            vt_ids2 = self.buy(price, self.fixed_size)
            self._handle_debug(action, vt_ids2, "buy")
    
    # ABMacdAction.A_RB_SHORT
    def _handle_a_long_to_short(self, price: float, action):
        if self.pos < 0:
            return
        
        if self.pos == 0:
            vt_ids = self.short(price, self.fixed_size)
            self._handle_debug(action, vt_ids, "short")
            return
        
        if self.pos > 0:
            vt_ids1 = self.sell(self._rollback_sell_price(price), abs(self.pos))
            self.target_pos = 0
            self._handle_debug(action, vt_ids1, "sell")

            vt_ids2 = self.short(price, self.fixed_size)
            self._handle_debug(action, vt_ids2, "short")



    def _handle_debug(self, action, vt_ids, trade):
        print(vt_ids, action.value, trade)
        return

    def _rollback_cover_price(self, price: float) -> float:
        return price + self.pricetick
    
    def _rollback_sell_price(self, price: float) -> float:
        if price - self.pricetick <= 0:
            return price
        
        return price - self.pricetick