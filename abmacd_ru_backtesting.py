from datetime import datetime

from abmacd.abmacd_v3_vnpys import ABMACDStrategyByVN
from dual_thrust.dual_thrust_vnpys import DualThrustStrategy
from ru_backtesting_util import default_ru88_param_config, default_bt_strategy
from xbacktesting.xvnpy_backtesting import Xbacktesting
from vnpy_ctastrategy.strategies.dual_thrust_strategy import DualThrustStrategy as VNDT 

def gen_test_name(pc, msg):
    return f"{pc['start'].strftime('%Y%m%d')}_{pc['end'].strftime('%Y%m%d')}_{pc['period']}_{msg}"


def _run_bt(period_config, strategy_setting, msg):
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,period_config=period_config,strategy_setting=strategy_setting, test_name=gen_test_name(period_config, msg))
    xbt.run_backtesting(output=True)
    if strategy_setting['sm_debug']:
        xbt.show_trade_data()
    # xbt.show_phl_chart()
    # xbt.show_balance_chart()


def default_train_bt():
    strategy_setting = {'size': 10,'sm_debug': False, 'macd_lvl': '1h15min', 'mswap_enable':False, 'a_fast_window': 22, 'a_signal_period': 7, 'a_slow_window': 33, 'b_fast_window': 2, 'b_slow_window': 16, 'b_signal_period': 19, 'b_ma_window': 16}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    _run_bt(period_config, strategy_setting, "default_train_bt")

def default_enable_stoploss_2_bt():
    strategy_setting = {'size': 10,'sm_debug': False, 'macd_lvl': '1h15min','mswap_enable':True, 'stoploss_enable':True}
    # strategy_setting = {'size': 10,'sm_debug': True, 'macd_lvl': '1h15min', 'stoploss_enable': True, 'a_fast_window': 22, 'a_signal_period': 7, 'a_slow_window': 33, 'b_fast_window': 2, 'b_slow_window': 16, 'b_signal_period': 19, 'b_ma_window': 16}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    _run_bt(period_config, strategy_setting, "default_enable_stoploss_1_bt")

def nongsiabao():
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'mswap_enable':True, 'stoploss_enable':True}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    xbt = Xbacktesting(strategy_class=ABMACDStrategyByVN, param_config=default_ru88_param_config,period_config=period_config,strategy_setting=strategy_setting, test_name=gen_test_name(period_config, "nongsiabao"))
    xbt.run_backtesting(output=True)

def dt_no_limit_exec():
    strategy_setting = {'n':5}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    xbt = Xbacktesting(strategy_class=DualThrustStrategy, param_config=default_ru88_param_config,period_config=period_config,strategy_setting=strategy_setting, test_name=gen_test_name(period_config, "nongsiabao"))
    xbt.run_backtesting(output=True)

def dt_by_vnpy():
    strategy_setting = {'k1':0.2, 'k2':0.2, 'fixed_size':10}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    xbt = Xbacktesting(strategy_class=VNDT, param_config=default_ru88_param_config,period_config=period_config,strategy_setting=strategy_setting, test_name=gen_test_name(period_config, "nongsiabao"))
    xbt.run_backtesting(output=True)

if __name__ == '__main__':
    # default_train_bt()
    # default_enable_stoploss_2_bt()
    # nongsiabao()
    # dt_by_vnpy()
    dt_no_limit_exec()