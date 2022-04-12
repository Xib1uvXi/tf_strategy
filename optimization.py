from ru_backtesting_util import cg_target_filter_by_annual_return, new_default_optimizer, opt_target_filter_by_annual_return
from vnpy.trader.optimize import OptimizationSetting


def run_opt_b_ma_window_annual_retrun():
    lvls = ['1h15min', '1d1h', '1d4h']

    for lvl in lvls:
        opt = new_default_optimizer()
        opt_setting = OptimizationSetting()
        opt_setting.set_target('annual_return')
        opt_setting.params['macd_lvl'] = [lvl]
        opt_setting.add_parameter('b_ma_window', 3, 5, 1)        
        opt.set_optimization_setting(opt_setting, opt_target_filter_by_annual_return)
        opt.set_cg_setting(10, cg_target_filter_by_annual_return)
        opt.run_opt()


if __name__ == '__main__':
    run_opt_b_ma_window_annual_retrun()