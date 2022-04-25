import sys  # nopep8
import os  # nopep8
root_path = os.getcwd()  # nopep8
sys.path.append(root_path)  # nopep8
from typing import Any
from vnpy_ctastrategy.strategies.multi_timeframe_strategy import MultiTimeframeStrategy
from vnpy_ctastrategy.strategies.boll_channel_strategy import BollChannelStrategy
from util import gen_test_name
from xbacktesting.xvnpy_backtesting import Xbacktesting, Xbatchbacktesting
from datetime import datetime
from config import default_ru88_param_config
from abmacd import vnpy_backtesting_current_strategy


def new_xbt(period_config: dict[str, Any], ss: dict[str, Any], msg: str) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=vnpy_backtesting_current_strategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting=ss,
        test_name=gen_test_name(
            period_config,
            msg))


def get_abmacd_with_default_strategy_setting_xbt(period_config: dict[str, Any]) -> Xbacktesting:
    default_strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}
    return new_xbt(period_config, default_strategy_setting, 'abmacd_default_ss')


def get_abmacd_with_enable_mswap_xbt(period_config: dict[str, Any]) -> Xbacktesting:
    enable_mswap_strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min', 'mswap_enable': True}
    return new_xbt(period_config, enable_mswap_strategy_setting, 'abmacd_enable_mswap')


def get_vnpy_boll_channel_xbt(period_config: dict[str, Any]) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=BollChannelStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size': 10},
        test_name=gen_test_name(
            period_config,
            'vnpy_boll_channel'))


def get_vnpy_multi_timeframe_xbt(period_config: dict[str, Any]) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=MultiTimeframeStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size': 10},
        test_name=gen_test_name(
            period_config,
            'vnpy_multi_timeframe'))


def nongsiabao():
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'mswap_enable': True, 'stoploss_enable': True}
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    xbt = Xbacktesting(
        strategy_class=vnpy_backtesting_current_strategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting=strategy_setting,
        test_name=gen_test_name(
            period_config,
            "nongsiabao"))
    xbt.run_backtesting(output=True)


def compare():
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}

    xbatch = Xbatchbacktesting()

    # abmacd
    default_xbt = get_abmacd_with_default_strategy_setting_xbt(period_config)
    enable_mswap = get_abmacd_with_enable_mswap_xbt(period_config)

    # vnpy
    vnpy_boll_channel_xbt = get_vnpy_boll_channel_xbt(period_config)
    vnpy_multi_timeframe_xbt = get_vnpy_multi_timeframe_xbt(period_config)

    xbatch.add_backtesting(default_xbt)
    xbatch.add_backtesting(enable_mswap)
    xbatch.add_backtesting(vnpy_boll_channel_xbt)
    xbatch.add_backtesting(vnpy_multi_timeframe_xbt)

    xbatch.run_batch_backtesting()


if __name__ == '__main__':
    nongsiabao()
    compare()
