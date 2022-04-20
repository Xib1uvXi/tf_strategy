from abmacd.abmacd_v2 import ABMACDStrategy
from xbacktesting.x_optimizer import optimizer
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

def macd_param_check_skip(raw_param: str) -> bool:
    param = eval(raw_param)
    _a_slow_window = param["a_slow_window"]
    _a_fast_window = param["a_fast_window"]
    if _a_slow_window - _a_fast_window < 10:
        return True

    return False


def opt_target_filter(raw_opt_results: list):
    filter_result = []
    for opt_result in raw_opt_results:
        # if macd_param_check_skip(opt_result[0]):
        #     continue

        if opt_result[1] > 20:
            filter_result.append(opt_result)
    
    return filter_result

def cg_target_filter(cg_bt_statistics: dict):
    if cg_bt_statistics['annual_return'] > 15:
        return True
    
    return False

def gen_opt_tasks_33():

    _b_ma_gen_opt_tasks_33()
    # opt = optimizer(default_bt_strategy, default_ru88_param_config, 3)
    # opt_setting = OptimizationSetting()
    # opt_setting.set_target('annual_return')
    # opt_setting.params['macd_lvl'] = ['1h15min']

    # opt_setting.params['a_fast_window'] = [22]
    # opt_setting.params['a_signal_period'] = [7]
    # opt_setting.params['a_slow_window'] = [33]

    # opt_setting.add_parameter('b_fast_window', 2, 15, 1)
    # opt_setting.add_parameter('b_slow_window', 12, 50, 1)
    # opt_setting.add_parameter('b_signal_period', 5, 20, 1)
    # opt.set_optimization_setting(opt_setting, opt_target_filter)
    # opt.set_cg_setting(4, cg_target_filter)
    # opt.run_opt()

def _b_ma_gen_opt_tasks_33():
    ts = [{'s':3, 'e':5}, {'s':6, 'e':8}, {'s':9, 'e':11}, {'s':12, 'e':14}, {'s':15, 'e':17}, {'s':18, 'e':20}]

    for t in ts:
        opt = optimizer(default_bt_strategy, default_ru88_param_config, 3)
        opt_setting = OptimizationSetting()
        opt_setting.set_target('annual_return')
        opt_setting.params['macd_lvl'] = ['1h15min']

        opt_setting.params['a_fast_window'] = [22]
        opt_setting.params['a_signal_period'] = [7]
        opt_setting.params['a_slow_window'] = [33]

        opt_setting.add_parameter('b_fast_window', 2, 15, 1)
        opt_setting.add_parameter('b_slow_window', 12, 50, 1)
        opt_setting.add_parameter('b_signal_period', 5, 20, 1)
        opt_setting.add_parameter('b_ma_window', t['s'], t['e'], 1)
        opt.set_optimization_setting(opt_setting, opt_target_filter)
        opt.set_cg_setting(4, cg_target_filter)
        opt.run_opt()

def gen_opt_tasks_34():
    ts = [{'s':3, 'e':5}, {'s':6, 'e':8}, {'s':9, 'e':11}, {'s':12, 'e':14}, {'s':15, 'e':17}, {'s':18, 'e':20}]

    for t in ts:
        opt = optimizer(default_bt_strategy, default_ru88_param_config, 3)
        opt_setting = OptimizationSetting()
        opt_setting.set_target('annual_return')
        opt_setting.params['macd_lvl'] = ['1h15min']

        opt_setting.params['a_fast_window'] = [22]
        opt_setting.params['a_signal_period'] = [7]
        opt_setting.params['a_slow_window'] = [34]

        opt_setting.add_parameter('b_fast_window', 2, 15, 1)
        opt_setting.add_parameter('b_slow_window', 12, 50, 1)
        opt_setting.add_parameter('b_signal_period', 5, 20, 1)
        opt_setting.add_parameter('b_ma_window', t['s'], t['e'], 1)
        opt.set_optimization_setting(opt_setting, opt_target_filter)
        opt.set_cg_setting(4, cg_target_filter)
        opt.run_opt()
