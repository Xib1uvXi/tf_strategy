
from typing import Callable
from macd_sm import ABMacdAction


class MacdDecision:
    # open
    buy: Callable
    short: Callable
    
    # close
    sell: Callable
    cover: Callable
    

    def __init__(self, buy: Callable, short: Callable, sell: Callable, cover: Callable):
        self.buy = buy
        self.short = short
        self.sell = sell
        self.cover = cover
    

    def dt(self, pos: int, action: ABMacdAction, price: float, size: float):
        if action is ABMacdAction.EMPTY:
            return

        # print(action.value)

        if action is ABMacdAction.A_OPEN_LONG:
            if abs(pos) > 0:
                #print("================= 已经有仓位，还要进行开仓动作 LONG=================")
                return
            
            self.buy(price, size)
            return
        
        if action is ABMacdAction.A_OPEN_SHORT:
            if abs(pos) > 0:
                #print("================= 已经有仓位，还要进行开仓动作 LONG=================")
                return
            
            self.short(price, size)
            return
        
        if action is ABMacdAction.B_CLOSE_LONG:
            if pos <= 0:
                #print("================= 无开多仓位，无法执行 B平多=================")
                return
            
            # TODO 这里需要考虑 多回&做多的仓位管理
            self.sell(price, abs(pos))
            return
        
        if action is ABMacdAction.B_CLOSE_SHORT:
            if pos >= 0:
                #print("================= 无开空仓位，无法执行 B平空=================")
                return
            
            self.cover(price, abs(pos))
            return
        
        if action is ABMacdAction.B_OPEN_LONG:
            # TODO 做多加仓，后续需要处理

            self.buy(price, size)
            return
        
        if action is ABMacdAction.B_OPEN_LONG_A:
            if pos > 0:
                #print("================= 已有做多仓位，无法执行 B多回=================")
                return
            
            # TODO 这里需要考虑 多回&做多的仓位管理
            self.buy(price, size)
            return
        
        
        if action is ABMacdAction.B_OPEN_SHORT_A:
            if pos < 0:
                #print("================= 已有做空仓位，无法执行 B空回=================")
                return
            
            self.short(price, size)
            return
        
        if action is ABMacdAction.A_RB_LONG:
            if pos == 0:
                #print("================== 空仓，直接做多===============")
                self.buy(price, size)
                return
            
            if pos < 0:
                self.cover(price, abs(pos))
            
            self.buy(price, size)
            return

        if action is ABMacdAction.A_RB_SHORT:
            if pos == 0:
                #print("================== 空仓，直接做空===============")
                self.short(price, size)
                return
            
            if pos > 0:
                self.sell(price, abs(pos))

            self.short(price, size)
            return
