
from xbacktesting.ru_bt import new_xbt_from_strategy_setting


if __name__ == '__main__':
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'sm_debug': False, 'b_ma_window':10}
    xbt = new_xbt_from_strategy_setting(period=1,strategy_setting=strategy_setting)

    xbt.run_backtesting(output=True)

    