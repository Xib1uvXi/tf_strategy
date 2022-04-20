
from ru_backtesting_util import new_xbt_from_strategy_setting


def ru_bt(period: int):
    strategy_setting = {'size': 10,'sm_debug': False,
    'macd_lvl': '1h15min', 
    'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20, 'b_ma_window': 42}

    xbt = new_xbt_from_strategy_setting(period, strategy_setting)
    xbt.run_backtesting(output=True)

def ru_bt2(period: int):
    strategy_setting = {'size': 10,'sm_debug': False,
    'macd_lvl': '1h15min', 
    'a_fast_window': 22, 'a_slow_window': 33, 'a_signal_period': 7, 'b_fast_window': 3, 'b_slow_window': 13, 'b_signal_period': 20}

    xbt = new_xbt_from_strategy_setting(period, strategy_setting)
    xbt.run_backtesting(output=True)

def ru_3y_test():
    sss = [
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 26, 'b_slow_window': 37, 'b_signal_period': 20, 'b_ma_window': 57},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 20, 'b_ma_window': 3},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 20, 'b_ma_window': 4},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 19, 'b_slow_window': 29, 'b_signal_period': 8, 'b_ma_window': 34},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 19, 'b_signal_period': 8, 'b_ma_window': 34},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20, 'b_ma_window': 42},
        {'size': 10, 'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20, 'b_ma_window': 43},
    ]

    i = 0
    for s in sss:
        print(i)
        i = i + 1
        xbt = new_xbt_from_strategy_setting(4, strategy_setting=s)
        xbt.run_backtesting(output=True)

if __name__ == '__main__':
    ru_3y_test()

    