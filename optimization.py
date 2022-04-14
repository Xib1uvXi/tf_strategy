from ru_backtesting_util import cg_target_filter_by_annual_return, gen_opt_b_macd_window_opt_tasks, new_default_optimizer, opt_target_filter_by_annual_return, opt_target_filter_by_annual_return_macd
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


if __name__ == '__main__':
#    run_opt_b_ma_window_annual_retrun()
    run_opt_b_macd_window_by_a_macd_window_annual_retrun()
