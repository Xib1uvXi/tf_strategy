from vnpy_ctastrategy import (
    BarData,
    BarGenerator,
)
from typing import Callable, Dict, Tuple, Union, Optional
from vnpy.trader.constant import Interval

class MACDBarGenerator(BarGenerator):
    def __init__(
        self,
        on_bar: Callable,
        window: int = 0,
        on_window_bar: Callable = None,
        interval: Interval = Interval.MINUTE
    ):  
        super().__init__(on_bar,window,on_window_bar,interval)
    
    def update_bar_hour_window(self, bar: BarData) -> None:
        if not self.hour_bar:
            self.init_bar(bar)
            return
        
        finished_bar = None

        # 9：00 - 10：00
        # 21：00 - 22：00
        # 22：00 - 23：00
        if self.hour_bar.datetime.hour < 10 or self.hour_bar.datetime.hour >= 21:
            super().update_bar_hour_window(bar)
            return


        # update minute bar into window bar and push
        # 14：15 or 11：15 or 15:00
        if ((bar.datetime.hour == 11 or bar.datetime.hour == 14) and bar.datetime.minute == 14) or (bar.datetime.hour == 14 and bar.datetime.minute == 59):
            self.hour_bar.high_price = max(self.hour_bar.high_price, bar.high_price)
            self.hour_bar.low_price = min(self.hour_bar.low_price, bar.low_price)
            self.hour_bar.close_price = bar.close_price
            self.hour_bar.volume += bar.volume
            self.hour_bar.turnover += bar.turnover
            self.hour_bar.open_interest = bar.open_interest
            finished_bar = self.hour_bar
            self.hour_bar = None
        
        # 10：00 - 11：15
        # 11：15 - 14：15
        # 14：15 - 15：00
        elif (self.hour_bar.datetime.hour == 11 and self.hour_bar.datetime.minute < 15) or (self.hour_bar.datetime.hour == 10):
            if (bar.datetime.hour == 11 and bar.datetime.minute > 15) or bar.datetime.hour > 11:
                finished_bar = self.hour_bar
                self.init_bar(bar)
        
        elif (self.hour_bar.datetime.hour == 11 and self.hour_bar.datetime.minute  == 15) or (self.hour_bar.datetime.hour == 14 and self.hour_bar.datetime.minute < 15):
            if (bar.datetime.hour == 14 and bar.datetime.minute > 15) or bar.datetime.hour > 14:
                finished_bar = self.hour_bar
                self.init_bar(bar)
        
        elif (self.hour_bar.datetime.hour == 14 and self.hour_bar.datetime.minute  == 15):
            if bar.datetime.hour > 15:
                finished_bar = self.hour_bar
                self.init_bar(bar)
        
        else:
            self.hour_bar.high_price = max(
                self.hour_bar.high_price,
                bar.high_price
            )
            self.hour_bar.low_price = min(
                self.hour_bar.low_price,
                bar.low_price
            )

            self.hour_bar.close_price = bar.close_price
            self.hour_bar.volume += bar.volume
            self.hour_bar.turnover += bar.turnover
            self.hour_bar.open_interest = bar.open_interest
        

        # Push finished window bar
        if finished_bar:
            self.on_hour_bar(finished_bar)

    def init_bar(self, bar: BarData):
        dt = None
        
        # 特殊时间段构建
        if bar.datetime.hour >= 11 and bar.datetime.hour < 15:
            if bar.datetime.hour == 11 and bar.datetime.minute >= 15:
               dt = bar.datetime.replace(minute=15, second=0, microsecond=0)
            
            if bar.datetime.hour == 14 and bar.datetime.minute >= 15:
                dt = bar.datetime.replace(minute=15, second=0, microsecond=0)

        else:
            dt = bar.datetime.replace(minute=0, second=0, microsecond=0)
       
        self.hour_bar = BarData(
            symbol=bar.symbol,
            exchange=bar.exchange,
            datetime=dt,
            gateway_name=bar.gateway_name,
            open_price=bar.open_price,
            high_price=bar.high_price,
            low_price=bar.low_price,
            close_price=bar.close_price,
            volume=bar.volume,
            turnover=bar.turnover,
            open_interest=bar.open_interest
        )
        return
