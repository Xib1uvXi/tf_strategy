from ru_backtesting_util import cg_target_filter_by_annual_return, gen_opt_b_macd_window_opt_tasks, gen_opt_macd_window_b_ma_opt_tasks, new_default_optimizer, opt_target_filter_by_annual_return, opt_target_filter_by_annual_return_macd
from vnpy.trader.optimize import OptimizationSetting


def run_opt_b_ma_window_annual_retrun():
    lvls = ['1h15min', '1d1h', '1d4h']

    for lvl in lvls:
        opt = new_default_optimizer()
        opt_setting = OptimizationSetting()
        opt_setting.set_target('annual_return')
        opt_setting.params['macd_lvl'] = [lvl]
        opt_setting.add_parameter('b_ma_window', 3, 66, 1)        
        opt.set_optimization_setting(opt_setting, opt_target_filter_by_annual_return)
        opt.set_cg_setting(10, cg_target_filter_by_annual_return)
        opt.run_opt()

def run_opt_a_macd_window_annual_retrun():
    lvls = ['1h15min', '1d4h']

    for lvl in lvls:
        opt = new_default_optimizer()
        opt_setting = OptimizationSetting()
        opt_setting.set_target('annual_return')
        opt_setting.params['macd_lvl'] = [lvl]
        opt_setting.add_parameter('a_fast_window', 10, 30, 1)
        opt_setting.add_parameter('a_slow_window', 20, 50, 1)
        opt_setting.add_parameter('a_signal_period', 5, 20, 1)
        opt.set_optimization_setting(opt_setting, opt_target_filter_by_annual_return_macd)
        opt.set_cg_setting(10, cg_target_filter_by_annual_return)
        opt.run_opt()

def run_opt_b_macd_window_by_a_macd_window_19_29_12_annual_retrun():
    opt = gen_opt_b_macd_window_opt_tasks(19, 29, 12)
    opt.run_opt()

def run_opt_b_macd_window_by_a_macd_window_annual_retrun():
    tasks = [
        {"f": 22, "s": 34, "p": 7},
        {"f": 23, "s": 34, "p": 6},
        {"f": 22, "s": 34, "p": 6},
        {"f": 16, "s": 31, "p": 14},
        {"f": 14, "s": 49, "p": 11},
        {"f": 23, "s": 33, "p": 6},
        {"f": 12, "s": 50, "p": 9},
    ]

    for task in tasks:
        opt = gen_opt_b_macd_window_opt_tasks(task["f"], task["s"], task["p"])
        opt.run_opt()

def run_opt_b_ma_window_by_eq_a_macd_window_annual_retrun():
    tasks = [
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 23, 'a_slow_window': 34, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 19, 'a_slow_window': 29, 'a_signal_period': 12},
        {'macd_lvl': '1h15min', 'a_fast_window': 19, 'a_slow_window': 29, 'a_signal_period': 15},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 16, 'a_slow_window': 31, 'a_signal_period': 14},
        {'macd_lvl': '1h15min', 'a_fast_window': 13, 'a_slow_window': 50, 'a_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 23, 'a_slow_window': 33, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 14, 'a_slow_window': 49, 'a_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 30, 'a_signal_period': 16},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 31, 'a_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 26, 'a_slow_window': 36, 'a_signal_period': 5},
        {'macd_lvl': '1h15min', 'a_fast_window': 21, 'a_slow_window': 36, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 18, 'a_slow_window': 30, 'a_signal_period': 15},
        {'macd_lvl': '1h15min', 'a_fast_window': 14, 'a_slow_window': 49, 'a_signal_period': 11},
        {'macd_lvl': '1h15min', 'a_fast_window': 12, 'a_slow_window': 50, 'a_signal_period': 9},
        {'macd_lvl': '1h15min', 'a_fast_window': 13, 'a_slow_window': 49, 'a_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 16, 'a_slow_window': 31, 'a_signal_period': 15},
        {'macd_lvl': '1h15min', 'a_fast_window': 13, 'a_slow_window': 50, 'a_signal_period': 9},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 31, 'a_signal_period': 14},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 33, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 47, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 31, 'a_signal_period': 16},
        {'macd_lvl': '1h15min', 'a_fast_window': 18, 'a_slow_window': 45, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 21, 'a_slow_window': 37, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 13, 'a_slow_window': 49, 'a_signal_period': 9},
        {'macd_lvl': '1h15min', 'a_fast_window': 13, 'a_slow_window': 50, 'a_signal_period': 10},
        {'macd_lvl': '1h15min', 'a_fast_window': 23, 'a_slow_window': 33, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 27, 'a_slow_window': 49, 'a_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 20, 'a_slow_window': 38, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 17, 'a_slow_window': 30, 'a_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 15, 'a_slow_window': 49, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 16, 'a_slow_window': 31, 'a_signal_period': 17},
        {'macd_lvl': '1h15min', 'a_fast_window': 30, 'a_slow_window': 47, 'a_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 12, 'a_slow_window': 38, 'a_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 23, 'a_slow_window': 34, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 20, 'a_slow_window': 37, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 18, 'a_slow_window': 46, 'a_signal_period': 6},
        {'macd_lvl': '1h15min', 'a_fast_window': 15, 'a_slow_window': 33, 'a_signal_period': 14},
        {'macd_lvl': '1h15min', 'a_fast_window': 14, 'a_slow_window': 49, 'a_signal_period': 7},
        {'macd_lvl': '1h15min', 'a_fast_window': 23, 'a_slow_window': 34, 'a_signal_period': 5},
    ]

    for task in tasks:
        opt = gen_opt_macd_window_b_ma_opt_tasks(task["a_fast_window"], task["a_slow_window"], task["a_signal_period"], task["a_fast_window"], task["a_slow_window"], task["a_signal_period"])
        opt.run_opt()

def run_opt_b_ma_window_by_no_eq_a_macd_window_annual_retrun():
    tasks = [
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 26, 'b_slow_window': 37, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 26, 'b_slow_window': 37, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 19, 'b_slow_window': 29, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 19, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 38, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 36, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 36, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 23, 'b_slow_window': 40, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 28, 'b_slow_window': 35, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 20, 'b_slow_window': 27, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 20, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 33, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 16, 'b_slow_window': 31, 'b_signal_period': 9},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 30, 'b_slow_window': 33, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 19, 'b_slow_window': 29, 'b_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 19, 'b_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 20, 'b_slow_window': 27, 'b_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 20, 'b_signal_period': 13},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 14, 'b_slow_window': 49, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 35, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 33, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 34, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 26, 'b_slow_window': 36, 'b_signal_period': 5},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 20, 'b_slow_window': 44, 'b_signal_period': 12},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 36, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 30, 'b_slow_window': 33, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 17},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 39, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 35, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 28, 'b_slow_window': 35, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 14, 'b_slow_window': 49, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 27, 'b_slow_window': 35, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 20, 'b_slow_window': 44, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 20, 'b_slow_window': 44, 'b_signal_period': 11},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 28, 'b_slow_window': 34, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 25, 'b_slow_window': 39, 'b_signal_period': 19},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 15, 'b_slow_window': 47, 'b_signal_period': 14},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 18, 'b_slow_window': 30, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 30, 'b_slow_window': 18, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 13, 'b_slow_window': 50, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 15, 'b_slow_window': 49, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 29, 'b_slow_window': 34, 'b_signal_period': 18},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 28, 'b_slow_window': 34, 'b_signal_period': 20},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 21, 'b_slow_window': 26, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 26, 'b_slow_window': 21, 'b_signal_period': 8},
        {'macd_lvl': '1h15min', 'a_fast_window': 22, 'a_slow_window': 34, 'a_signal_period': 7, 'b_fast_window': 14, 'b_slow_window': 49, 'b_signal_period': 18},
    ]

    for task in tasks:
        opt = gen_opt_macd_window_b_ma_opt_tasks(task["a_fast_window"], task["a_slow_window"], task["a_signal_period"], task["b_fast_window"], task["b_slow_window"], task["b_signal_period"])
        opt.run_opt()


if __name__ == '__main__':
#    run_opt_b_ma_window_annual_retrun()
    run_opt_b_ma_window_by_no_eq_a_macd_window_annual_retrun()
