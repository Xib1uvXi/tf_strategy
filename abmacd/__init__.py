from abmacd.abmacd_v3_vnpys import ABMACDStrategyByVN


name = "abmacd"

vnpy_backtesting_current_strategy = ABMACDStrategyByVN
vnpy_backtesting_current_strategy_setting = {
    'size': 10,
    'sm_debug': False,
    'macd_lvl': '1h15min',
    'mswap_enable': True,
    'stoploss_enable': True,
    'cancel_enable': True,
    'a_fast_window': 22,
    'a_signal_period': 7,
    'a_slow_window': 33,
    'b_fast_window': 2,
    'b_slow_window': 16,
    'b_signal_period': 19,
    'b_ma_window': 16}
