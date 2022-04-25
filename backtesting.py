from datetime import datetime
from typing import Any, Dict
from ru_backtesting_util import new_xbt_from_strategy_setting
from xbacktesting.xvnpy_backtesting import Xbatchbacktesting


def ru_bt(period: Dict[str, Any]):
    strategy_setting = {
        'size': 10,
        'sm_debug': False,
        'macd_lvl': '1h15min',
        'a_fast_window': 22,
        'a_slow_window': 34,
        'a_signal_period': 7,
        'b_fast_window': 13,
        'b_slow_window': 50,
        'b_signal_period': 20,
        'b_ma_window': 42}

    xbt = new_xbt_from_strategy_setting(period, strategy_setting)
    xbt.run_backtesting(output=True)


def ru_bt2(period: Dict[str, Any]):
    strategy_setting = {
        'size': 10,
        'sm_debug': False,
        'macd_lvl': '1h15min',
        'a_fast_window': 22,
        'a_slow_window': 33,
        'a_signal_period': 7,
        'b_fast_window': 3,
        'b_slow_window': 13,
        'b_signal_period': 20}

    xbt = new_xbt_from_strategy_setting(period, strategy_setting)
    xbt.run_backtesting(output=True)


def ru_3y_test():
    sss = [
        {'size': 10,
         'macd_lvl': '1h15min',
         'a_fast_window': 22,
         'a_slow_window': 34,
         'a_signal_period': 7,
         'b_fast_window': 26,
         'b_slow_window': 37,
         'b_signal_period': 20,
         'b_ma_window': 57},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 20, 'b_ma_window': 3},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 20, 'b_ma_window': 4},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 19, 'b_slow_window': 29, 'b_signal_period': 8, 'b_ma_window': 34},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 19, 'b_signal_period': 8, 'b_ma_window': 34},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20, 'b_ma_window': 42},
        # {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20, 'b_ma_window': 43},
    ]

    pc = {"start": datetime(2018, 2, 16), "end": datetime(2022, 2, 16), "period": "3"}

    i = 0
    for s in sss:
        print(i)
        i = i + 1
        xbt = new_xbt_from_strategy_setting(pc, strategy_setting=s)
        xbt.run_backtesting(output=True)


def batch_3y_test():
    batch = Xbatchbacktesting()
    strategy_setting = {
        'size': 10,
        'sm_debug': False,
        'macd_lvl': '1h15min',
        'a_fast_window': 22,
        'a_signal_period': 7,
        'a_slow_window': 33,
        'b_fast_window': 2,
        'b_slow_window': 16,
        'b_signal_period': 19,
        'b_ma_window': 16}

    pcs = [
        {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16), "period": "1"},
        {"start": datetime(2020, 2, 16), "end": datetime(2021, 2, 16), "period": "1"},
        {"start": datetime(2019, 2, 16), "end": datetime(2020, 2, 16), "period": "1"},
        {"start": datetime(2018, 2, 16), "end": datetime(2019, 2, 16), "period": "1"},
        {"start": datetime(2017, 2, 16), "end": datetime(2018, 2, 16), "period": "1"},
    ]

    for pc in pcs:
        xbt = new_xbt_from_strategy_setting(pc, strategy_setting)
        xbt._test_name = f"{pc['start']}_{pc['end']}_{pc['period']}"
        batch.add_backtesting(xbt)

    batch.run_batch_backtesting(show_balance=True)


if __name__ == '__main__':
    batch_3y_test()
