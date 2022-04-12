from xmlrpc.client import Boolean
from abmacd.abmacd_v2 import ABMACDStrategy
from xbacktesting.x_optimizer import optimizer
from xbacktesting.xvnpy_backtesting import Xbacktesting, Xbatchbacktesting
from vnpy.trader.optimize import OptimizationSetting

default_ru88_param_config = {
    "vt_symbol": "RU88.SHFE",
    "interval": "1m",
    "rate": 0.45/10000,
    "slippage": 5,
    "size": 10,
    "pricetick": 5,
    "capital": 5_00_000,
}

default_bt_strategy = ABMACDStrategy


def new_default_xbt(period: int):
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min',
                        'sm_debug': False, 'b_ma_window': 10}
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                       period=period, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])

    return xbt


def new_xbt_from_strategy_setting(period: int, strategy_setting: dict):
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                       period=period, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
    return xbt

def new_default_optimizer():
    opt = optimizer(default_bt_strategy, default_ru88_param_config, 1)
    return opt


def opt_target_filter_by_annual_return(raw_opt_results: list):
    filter_result = []
    for opt_result in raw_opt_results:
        if opt_result[1] > 15:
            filter_result.append(opt_result)
    
    return filter_result

def macd_param_check_skip(raw_param: str) -> bool:
    param = eval(raw_param)
    _a_slow_window = param["a_slow_window"]
    _a_fast_window = param["a_fast_window"]
    if _a_slow_window - _a_fast_window < 10:
        return True

    return False


def opt_target_filter_by_annual_return_macd(raw_opt_results: list):
    filter_result = []
    for opt_result in raw_opt_results:
        if macd_param_check_skip(opt_result[0]):
            continue

        if opt_result[1] > 15:
            filter_result.append(opt_result)
    
    return filter_result


def cg_target_filter_by_annual_return(cg_bt_statistics: dict):
    if cg_bt_statistics['annual_return'] > 3:
        return True
    
    return False