from datetime import datetime

from abmacd.abmacd_v2 import ABMACDStrategy
from ru_backtesting_util import default_ru88_param_config, default_bt_strategy
from xbacktesting.xvnpy_backtesting import Xbacktesting

def gen_test_name(pc, msg):
    return f"{pc['start'].strftime('%Y%m%d')}_{pc['end'].strftime('%Y%m%d')}_{pc['period']}_{msg}"


def _run_bt(period_config, strategy_setting, msg):
    xbt = Xbacktesting(strategy_class=default_bt_strategy, param_config=default_ru88_param_config,period_config=period_config,strategy_setting=strategy_setting, test_name=gen_test_name(period_config, msg))
    xbt.run_backtesting(output=True)
    if strategy_setting['sm_debug']:
        xbt.show_trade_data()


def default_train_bt():
    """
    2022-04-20 16:12:08.934345      首个交易日：    2020-01-07
    2022-04-20 16:12:08.934353      最后交易日：    2020-12-30
    2022-04-20 16:12:08.934400      总收益率：      -27.97%
    2022-04-20 16:12:08.934407      年化收益：      -28.09%
    2022-04-20 16:12:08.934424      百分比最大回撤: -81.15%
    2022-04-20 16:12:08.934430      最长回撤天数:   238
    2022-04-20 16:12:08.934472      总成交笔数：    176
    2022-04-20 16:12:08.934527      收益标准差：    5.91%
    2022-04-20 16:12:08.934535      Sharpe Ratio：  -0.36
    2022-04-20 16:12:08.934542      收益回撤比：    -0.34
    """

    strategy_setting = {'size': 10,'sm_debug': False, 'macd_lvl': '1h15min'}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    _run_bt(period_config, strategy_setting, "default_train_bt")

def default_enable_stoploss_2_bt():
    """
    2022-04-20 16:23:12.701486      首个交易日：    2020-01-07
    2022-04-20 16:23:12.701494      最后交易日：    2020-12-30
    2022-04-20 16:23:12.701547      总收益率：      -25.77%
    2022-04-20 16:23:12.701554      年化收益：      -25.88%
    2022-04-20 16:23:12.701569      百分比最大回撤: -79.96%
    2022-04-20 16:23:12.701576      最长回撤天数:   238
    2022-04-20 16:23:12.701613      总成交笔数：    177
    2022-04-20 16:23:12.701665      收益标准差：    5.74%
    2022-04-20 16:23:12.701671      Sharpe Ratio：  -0.34
    2022-04-20 16:23:12.701678      收益回撤比：    -0.32
    """
    strategy_setting = {'size': 10,'sm_debug': False, 'macd_lvl': '1h15min', 'stoploss_enable': True}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    _run_bt(period_config, strategy_setting, "default_enable_stoploss_1_bt")

if __name__ == '__main__':
    default_train_bt()