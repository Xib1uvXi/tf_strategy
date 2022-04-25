import sys
import os
root_path = os.getcwd()
sys.path.append(root_path)
from abmacd import vnpy_backtesting_current_strategy
from config import default_ru88_param_config
from datetime import datetime
from xbacktesting.xvnpy_backtesting import Xbacktesting, Xbatchbacktesting
from util import gen_test_name
from vnpy_ctastrategy.strategies.boll_channel_strategy import BollChannelStrategy
from vnpy_ctastrategy.strategies.turtle_signal_strategy import TurtleSignalStrategy
from vnpy_ctastrategy.strategies.multi_timeframe_strategy import MultiTimeframeStrategy
from vnpy_ctastrategy.strategies.atr_rsi_strategy import AtrRsiStrategy


def new_xbt(period_config: dict, ss: dict, msg: str) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=vnpy_backtesting_current_strategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting=ss,
        test_name=gen_test_name(
            period_config,
            msg))


def get_abmacd_with_default_strategy_setting_xbt(period_config: dict) -> Xbacktesting:
    default_strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}
    return new_xbt(period_config, default_strategy_setting, 'abmacd_default_ss')


def get_abmacd_with_enable_mswap_xbt(period_config: dict) -> Xbacktesting:
    enable_mswap_strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min', 'mswap_enable': True}
    return new_xbt(period_config, enable_mswap_strategy_setting, 'abmacd_enable_mswap')


def get_vnpy_boll_channel_xbt(period_config: dict) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=BollChannelStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size':10},
        test_name=gen_test_name(
            period_config,
            'vnpy_boll_channel'))


def get_vnpy_turtle_signal_xbt(period_config: dict) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=TurtleSignalStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size':10},
        test_name=gen_test_name(
            period_config,
            'vnpy_turtle_signal'))


def get_vnpy_multi_timeframe_xbt(period_config: dict) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=MultiTimeframeStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size':10},
        test_name=gen_test_name(
            period_config,
            'vnpy_multi_timeframe'))


def get_vnpy_atr_rsi_xbt(period_config: dict) -> Xbacktesting:
    return Xbacktesting(
        strategy_class=AtrRsiStrategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting={'fixed_size':10},
        test_name=gen_test_name(
            period_config,
            'vnpy_atr_rsi'))


def compare():
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}

    xbatch = Xbatchbacktesting()

    # abmacd
    default_xbt = get_abmacd_with_default_strategy_setting_xbt(period_config)
    enable_mswap = get_abmacd_with_enable_mswap_xbt(period_config)
    
    #vnpy
    vnpy_boll_channel_xbt = get_vnpy_boll_channel_xbt(period_config)
    vnpy_turtle_signal_xbt = get_vnpy_turtle_signal_xbt(period_config)
    vnpy_multi_timeframe_xbt = get_vnpy_multi_timeframe_xbt(period_config)
    vnpy_vnpy_atr_rsi_xbt = get_vnpy_atr_rsi_xbt(period_config)

    xbatch.add_backtesting(default_xbt)
    xbatch.add_backtesting(enable_mswap)
    xbatch.add_backtesting(vnpy_boll_channel_xbt)
    xbatch.add_backtesting(vnpy_turtle_signal_xbt)
    xbatch.add_backtesting(vnpy_multi_timeframe_xbt)
    xbatch.add_backtesting(vnpy_vnpy_atr_rsi_xbt)

    xbatch.run_batch_backtesting()

if __name__ == '__main__':
    compare()