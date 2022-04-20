from abmacd.abmacd_v2 import ABMACDStrategy
from xbacktesting.x_optimizer import optimizer
from xbacktesting.xvnpy_backtesting import Xbacktesting, Xbatchbacktesting
from vnpy.trader.optimize import OptimizationSetting
from datetime import datetime

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



def new_xbt_from_strategy_setting(period: dict, strategy_setting: dict):
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                       period_config=period, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
    return xbt

def new_default_optimizer():
    opt = optimizer(default_bt_strategy, default_ru88_param_config, {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16), "period": "1"})
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


def gen_opt_macd_window_b_ma_opt_tasks(a_f,a_s,a_p, b_f,b_s,b_p):
    opt = optimizer(default_bt_strategy, default_ru88_param_config, {"start": datetime(2012, 2, 16), "end": datetime(2022, 2, 16), "period": "10"})
    opt_setting = OptimizationSetting()
    opt_setting.set_target('annual_return')
    opt_setting.params['macd_lvl'] = ['1h15min']
    opt_setting.params['a_fast_window'] = [a_f]
    opt_setting.params['a_slow_window'] = [a_s]
    opt_setting.params['a_signal_period'] = [a_p]
    opt_setting.params['b_fast_window'] = [b_f]
    opt_setting.params['b_slow_window'] = [b_s]
    opt_setting.params['b_signal_period'] = [b_p]
    opt_setting.add_parameter('b_ma_window', 3, 66, 1) 
    opt.set_optimization_setting(opt_setting, opt_target_filter_by_annual_return_20)
    opt.set_cg_setting({"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16), "period": "1"}, cg_target_filter_by_annual_return_15)
    return opt


def gen_opt_b_macd_window_opt_tasks(f,s,p):
    opt = optimizer(default_bt_strategy, default_ru88_param_config, {"start": datetime(2012, 2, 16), "end": datetime(2022, 2, 16), "period": "10"})
    opt_setting = OptimizationSetting()
    opt_setting.set_target('annual_return')
    opt_setting.params['macd_lvl'] = ['1h15min']
    opt_setting.params['a_fast_window'] = [f]
    opt_setting.params['a_slow_window'] = [s]
    opt_setting.params['a_signal_period'] = [p]
    opt_setting.add_parameter('b_fast_window', 3, 30, 1)
    opt_setting.add_parameter('b_slow_window', 13, 50, 1)
    opt_setting.add_parameter('b_signal_period', 5, 20, 1)
    opt.set_optimization_setting(opt_setting, opt_target_filter_by_annual_return_20)
    opt.set_cg_setting({"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16), "period": "1"}, cg_target_filter_by_annual_return_15)
    return opt

def opt_target_filter_by_annual_return_20(raw_opt_results: list):
    filter_result = []
    for opt_result in raw_opt_results:
        if macd_param_check_skip(opt_result[0]):
            continue

        if opt_result[1] > 20:
            filter_result.append(opt_result)
    
    return filter_result

def cg_target_filter_by_annual_return_15(cg_bt_statistics: dict):
    if cg_bt_statistics['annual_return'] > 15:
        return True
    
    return False