from abmacd.abmacd_v2 import ABMACDStrategy
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

def new_1_year_backtesting(output: bool = False, show_chart: bool = False):
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'sm_debug': False, 'b_ma_window':10}
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                       period=1, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
    xbt.run_backtesting(output)

    if show_chart:
        xbt.show_balance_chart()
        xbt.show_phl_chart()

def new_batch_1_year_3_level_backtesting(show_balance: bool = False, show_phl: bool = False):
    size = 10
    sm_debug = False

    tasks = ['1d4h', '1d1h', '1h15min']

    batch = Xbatchbacktesting()
    for task in tasks:
        strategy_setting = {'size': size,
                            'macd_lvl': task, 'sm_debug': sm_debug}
        xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                           period=1, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
        batch.add_backtesting(xbt)

    batch.run_batch_backtesting(show_balance=show_balance, show_phl=show_phl)

# TODO: need to add optimization
def b_level_ma_bf_opt():
    strategy_setting = {}
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,
                       period=1, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
    target = "total_return"
    optimization_setting = OptimizationSetting()
    optimization_setting.set_target(target)
    optimization_setting.add_parameter("b_ma_window", 3, 66, 1)

    retults = xbt.run_bf_optimization(optimization_setting)
    # print(f"best result\t 参数：{retults[0][0]}, 结果：{target}: {retults[0][1]}")