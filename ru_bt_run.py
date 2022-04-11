from abmacd.abmacd_v2 import ABMACDStrategy
from xvnpy_backtesting import Xbacktesting, Xbatchbacktesting


ru88_param_config = {
    "vt_symbol": "RU88.SHFE",
    "interval": "1m",
    "rate": 0.45/10000,
    "slippage": 5,
    "size": 10,
    "pricetick": 5,
    "capital": 5_00_000,
}

test_strategy = ABMACDStrategy


def new_1_year_backtesting(output: bool = False):
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'sm_debug': False}
    xbt = Xbacktesting(strategy_class=test_strategy, param_config=ru88_param_config,
                       period=1, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
    xbt.run_backtesting(output)
    # xbt.show_balance_chart()
    # xbt.show_phl_chart()


def new_batch_1_year_3_level_backtesting(show_balance: bool = False, show_phl: bool = False):
    size = 10
    sm_debug = False

    tasks = ['1d4h', '1d1h', '1h15min']

    batch = Xbatchbacktesting()
    for task in tasks:
        strategy_setting = {'size': size,
                            'macd_lvl': task, 'sm_debug': sm_debug}
        xbt = Xbacktesting(strategy_class=test_strategy, param_config=ru88_param_config,
                           period=1, strategy_setting=strategy_setting, test_name=strategy_setting['macd_lvl'])
        batch.add_backtesting(xbt)

    batch.run_batch_backtesting(show_balance=show_balance, show_phl=show_phl)


# new_1_year_backtesting(output=True)
# new_batch_1_year_3_level_backtesting()