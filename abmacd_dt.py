
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

        if action is ABMacdAction.A_OPEN_LONG:
            if abs(pos) > 0:
                return
            
            id = self.buy(price, size)
            #print(id, action.value, "buy")
            return
        
        if action is ABMacdAction.A_OPEN_SHORT:
            if abs(pos) > 0:
                return
            
            id = self.short(price, size)
            #print(id, action.value, "short")
            return
        
        if action is ABMacdAction.B_CLOSE_LONG:
            if pos <= 0:
                return
            
            # TODO 这里需要考虑 多回&做多的仓位管理
            id = self.sell(price, abs(pos))
            #print(id, action.value, "sell")
            return
        
        if action is ABMacdAction.B_CLOSE_SHORT:
            if pos >= 0:
                return
            
            id = self.cover(price, abs(pos))
            #print(id, action.value, "cover")
            return
        
        if action is ABMacdAction.B_OPEN_LONG:
            # TODO 做多加仓，后续需要处理

            if pos >= 0:
                id = self.buy(price, size)
                #print(id, action.value, "buy")
            
            return
        
        if action is ABMacdAction.B_OPEN_LONG_A:
            if pos > 0:
                return
            
            # TODO 这里需要考虑 多回&做多的仓位管理

            if pos == 0:
                id = self.buy(price, size)
                #print(id, action.value, "buy")
            
            return
        
        
        if action is ABMacdAction.B_OPEN_SHORT_A:
            if pos < 0:
                return
            
            if pos == 0:
                id = self.short(price, size)
                #print(id, action.value, "short")
            return
        
        if action is ABMacdAction.A_RB_LONG:
            if pos > 0:
                return
            
            if pos == 0:
                id = self.buy(price, size)
                #print(id, action.value, "buy")
                return
            
            if pos < 0:
                id = self.cover(price, abs(pos))
                #print(id, action.value, "conver")
            
            id = self.buy(price, size)
            #print(id, action.value, "buy")
            return

        if action is ABMacdAction.A_RB_SHORT:
            if pos < 0:
                return

            if pos == 0:
                id = self.short(price, size)
                #print(id, action.value, "short")
                return
            
            if pos > 0:
                id = self.sell(price, abs(pos))
                #print(id, action.value, "sell")

            id = self.short(price, size)
            #print(id, action.value, "short")
            return
