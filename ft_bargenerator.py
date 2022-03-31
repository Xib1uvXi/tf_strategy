from datetime import time
from vnpy_ctastrategy import (
    BarData,
    TickData,
)
from typing import Callable,Optional
from vnpy.trader.constant import Interval
from vnpy.trader.constant import Exchange


class BarGenerator:
    """
    For:
    1. generating 1 minute bar data from tick data
    2. generating x minute bar/x hour bar data from 1 minute data

    Notice:
    1. for x minute bar, x must be able to divide 60: 2, 3, 5, 6, 10, 15, 20, 30
    2. for x hour bar, x can be any number
    """

    def __init__(
        self,
        on_bar: Callable,
        window: int = 0,
        on_window_bar: Callable = None,
        interval: Interval = Interval.MINUTE
    ):
        """Constructor"""
        self.bar: BarData = None
        self.on_bar: Callable = on_bar

        self.interval: Interval = interval
        self.interval_count: int = 0

        self.hour_bar: BarData = None

        self.window: int = window
        self.window_bar: BarData = None
        self.on_window_bar: Callable = on_window_bar

        self.last_tick: TickData = None

    def update_tick(self, tick: TickData) -> None:
        """
        Update new tick data into generator.
        """
        new_minute = False

        # Filter tick data with 0 last price
        if not tick.last_price:
            return

        # Filter tick data with older timestamp
        if self.last_tick and tick.datetime < self.last_tick.datetime:
            return

        if not self.bar:
            new_minute = True
        elif (
            (self.bar.datetime.minute != tick.datetime.minute)
            or (self.bar.datetime.hour != tick.datetime.hour)
        ):
            self.bar.datetime = self.bar.datetime.replace(
                second=0, microsecond=0
            )
            self.on_bar(self.bar)

            new_minute = True

        if new_minute:
            self.bar = BarData(
                symbol=tick.symbol,
                exchange=tick.exchange,
                interval=Interval.MINUTE,
                datetime=tick.datetime,
                gateway_name=tick.gateway_name,
                open_price=tick.last_price,
                high_price=tick.last_price,
                low_price=tick.last_price,
                close_price=tick.last_price,
                open_interest=tick.open_interest
            )
        else:
            self.bar.high_price = max(self.bar.high_price, tick.last_price)
            if tick.high_price > self.last_tick.high_price:
                self.bar.high_price = max(self.bar.high_price, tick.high_price)

            self.bar.low_price = min(self.bar.low_price, tick.last_price)
            if tick.low_price < self.last_tick.low_price:
                self.bar.low_price = min(self.bar.low_price, tick.low_price)

            self.bar.close_price = tick.last_price
            self.bar.open_interest = tick.open_interest
            self.bar.datetime = tick.datetime

        if self.last_tick:
            volume_change = tick.volume - self.last_tick.volume
            self.bar.volume += max(volume_change, 0)

            turnover_change = tick.turnover - self.last_tick.turnover
            self.bar.turnover += max(turnover_change, 0)

        self.last_tick = tick

    def update_bar(self, bar: BarData) -> None:
        """
        Update 1 minute bar into generator
        """
        if self.interval == Interval.MINUTE:
            self.update_bar_minute_window(bar)
        elif self.interval == Interval.HOUR:
            if bar.exchange in [Exchange.SHFE, Exchange.DCE, Exchange.CZCE]:
                self.fe_update_bar_hour_window(bar)
            else:
                self.update_bar_hour_window(bar)
        elif self.interval == Interval.DAILY:
            if bar.exchange in [Exchange.SHFE, Exchange.DCE, Exchange.CZCE]:
                self.update_bar_daily_window(bar)
        else:
            self.update_bar_hour_window(bar)

    def update_bar_minute_window(self, bar: BarData) -> None:
        """"""
        # If not inited, create window bar object
        if not self.window_bar:
            dt = bar.datetime.replace(second=0, microsecond=0)
            self.window_bar = BarData(
                symbol=bar.symbol,
                exchange=bar.exchange,
                datetime=dt,
                gateway_name=bar.gateway_name,
                open_price=bar.open_price,
                high_price=bar.high_price,
                low_price=bar.low_price
            )
        # Otherwise, update high/low price into window bar
        else:
            self.window_bar.high_price = max(
                self.window_bar.high_price,
                bar.high_price
            )
            self.window_bar.low_price = min(
                self.window_bar.low_price,
                bar.low_price
            )

        # Update close price/volume/turnover into window bar
        self.window_bar.close_price = bar.close_price
        self.window_bar.volume += bar.volume
        self.window_bar.turnover += bar.turnover
        self.window_bar.open_interest = bar.open_interest

        # Check if window bar completed
        if not (bar.datetime.minute + 1) % self.window:
            self.on_window_bar(self.window_bar)
            self.window_bar = None

        elif (bar.datetime.time() == time(10, 14) and bar.exchange in [Exchange.SHFE, Exchange.DCE, Exchange.CZCE]):
            self.on_window_bar(self.window_bar)
            self.window_bar = None

    def fe_update_bar_hour_window(self, bar: BarData) -> None:
        if not self.hour_bar:
            self.new_1h_bar(bar)
            return
        
        # 9：00 - 10：00
        # 21：00 - 22：00
        # 22：00 - 23：00
        if bar.datetime.hour < 10 or bar.datetime.hour >= 21:
            self.update_bar_hour_window(bar)
            return
        
        finished_bar = None

        # If minute is ending, update minute bar into window bar and push. 11：15、14：15、15：00
        if bar.datetime.time() == time(11, 14) or bar.datetime.time == time(14, 14) or bar.datetime.time == time(14, 59):
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

            finished_bar = self.hour_bar
            self.hour_bar = None

        # If minute bar of new hour, then push existing window bar
        elif (
                (self.hour_bar.datetime.time() < time(11, 14) and bar.datetime.time() > time(11, 14)) 
            or 
                (self.hour_bar.datetime.time() < time(14, 14) and bar.datetime.time() > time(14, 14))
            or 
                (self.hour_bar.datetime.time() < time(14, 59) and bar.datetime.time() > time(15, 00))
            ):
            finished_bar = self.hour_bar
            self.new_1h_bar(bar)
        
        # Otherwise only update minute bar
        else:
            self.merge_bar(bar)
        
        # Push finished window bar
        if finished_bar:
            self.on_hour_bar(finished_bar)

    def merge_bar(self, bar: BarData):
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

    def new_1h_bar(self, bar: BarData):
        dt = None
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

    def update_bar_hour_window(self, bar: BarData) -> None:
        """"""
        # If not inited, create window bar object
        if not self.hour_bar:
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

        finished_bar = None

        # If minute is 59, update minute bar into window bar and push
        if bar.datetime.minute == 59:
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

            finished_bar = self.hour_bar
            self.hour_bar = None

        # If minute bar of new hour, then push existing window bar
        elif bar.datetime.hour != self.hour_bar.datetime.hour:
            finished_bar = self.hour_bar

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
        # Otherwise only update minute bar
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

    def on_hour_bar(self, bar: BarData) -> None:
        """"""
        if self.window == 1:
            self.on_window_bar(bar)
        else:
            if not self.window_bar:
                self.window_bar = BarData(
                    symbol=bar.symbol,
                    exchange=bar.exchange,
                    datetime=bar.datetime,
                    gateway_name=bar.gateway_name,
                    open_price=bar.open_price,
                    high_price=bar.high_price,
                    low_price=bar.low_price
                )
            else:
                self.window_bar.high_price = max(
                    self.window_bar.high_price,
                    bar.high_price
                )
                self.window_bar.low_price = min(
                    self.window_bar.low_price,
                    bar.low_price
                )

            self.window_bar.close_price = bar.close_price
            self.window_bar.volume += bar.volume
            self.window_bar.turnover += bar.turnover
            self.window_bar.open_interest = bar.open_interest

            self.interval_count += 1
            if not self.interval_count % self.window:
                self.interval_count = 0
                self.on_window_bar(self.window_bar)
                self.window_bar = None
        
    def update_bar_daily_window(self, bar: BarData) -> None:
        # If not inited, create window bar object
        if not self.hour_bar:
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

        finished_bar = None

        if bar.datetime.time() == time(14,59):
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

            finished_bar = self.hour_bar
            self.hour_bar = None
        elif self.hour_bar.datetime.date() != bar.datetime.date():
            dif_day = (bar.datetime - self.hour_bar.datetime).days
            # next day?
            if dif_day < 3 and bar.datetime.time() >= time(9,0) and bar.datetime.time() < time(15,0):
                self.merge_bar(bar)
            else:
                finished_bar = self.hour_bar
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
            
        # Otherwise only update minute bar
        else:
            self.merge_bar(bar)

        # Push finished window bar
        if finished_bar:
            self.on_hour_bar(finished_bar)


    def generate(self) -> Optional[BarData]:
        """
        Generate the bar data and call callback immediately.
        """
        bar = self.bar

        if self.bar:
            bar.datetime = bar.datetime.replace(second=0, microsecond=0)
            self.on_bar(bar)

        self.bar = None
        return bar
