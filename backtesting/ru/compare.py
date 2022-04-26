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
    strategy_setting = {'size': 10, 'macd_lvl': '1h15min', 'sm_debug': True, 'cancel_enable': True, 'mswap_enable': True, 'stoploss_enable': True}
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
    xbt.show_trade_data()


def v0_2_2_rc2_mswap_enable():
    training_dataset_period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    validation_dataset_period_config_1 = {"start": datetime(2021, 1, 1), "end": datetime(2021, 12, 31), "period": "1"}
    validation_dataset_period_config_2 = {"start": datetime(2019, 1, 1), "end": datetime(2019, 12, 31), "period": "1"}
    test_dataset_period_config = {"start": datetime(2022, 1, 1), "end": datetime(2022, 2, 16), "period": "1"}

    strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min', 'mswap_enable': True, 'cancel_enable': True}

    rc2_training_dataset = new_xbt(training_dataset_period_config, strategy_setting, "mswap_enable_training_dataset")
    rc2_validation_dataset_1 = new_xbt(validation_dataset_period_config_1, strategy_setting, "rc2_mswap_enable_validation_dataset_1")
    rc2_validation_dataset_2 = new_xbt(validation_dataset_period_config_2, strategy_setting, "rc2_mswap_enable_validation_dataset_2")
    rc2_test_dataset = new_xbt(test_dataset_period_config, strategy_setting, "rc2_test_dataset")

    training_dataset = new_xbt(training_dataset_period_config, {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_training_dataset")
    validation_dataset_1 = new_xbt(
        validation_dataset_period_config_1, {
            'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_validation_dataset_1")
    validation_dataset_2 = new_xbt(
        validation_dataset_period_config_2, {
            'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_validation_dataset_2")
    test_dataset = new_xbt(test_dataset_period_config, {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_test_dataset")

    xbt_list = [
        rc2_training_dataset,
        rc2_validation_dataset_1,
        rc2_validation_dataset_2,
        rc2_test_dataset,
        training_dataset,
        validation_dataset_1,
        validation_dataset_2,
        test_dataset]

    xbatch = Xbatchbacktesting()

    for xbt in xbt_list:
        xbatch.add_backtesting(xbt)

    xbatch.run_batch_backtesting(show_balance=True, show_phl=True)


def v0_2_2_rc2_mswap_enable_stoploss_enable():
    training_dataset_period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    validation_dataset_period_config_1 = {"start": datetime(2021, 1, 1), "end": datetime(2021, 12, 31), "period": "1"}
    validation_dataset_period_config_2 = {"start": datetime(2019, 1, 1), "end": datetime(2019, 12, 31), "period": "1"}
    test_dataset_period_config = {"start": datetime(2022, 1, 1), "end": datetime(2022, 2, 16), "period": "1"}

    strategy_setting = {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min', 'mswap_enable': True, 'stoploss_enable': True, 'cancel_enable': True}

    rc2_stoploss_enable_training_dataset = new_xbt(training_dataset_period_config, strategy_setting,
                                                   "rc2_mswap_enable_stoploss_enable_training_dataset")
    rc2_stoploss_enable_validation_dataset_1 = new_xbt(
        validation_dataset_period_config_1,
        strategy_setting,
        "rc2_mswap_enable_stoploss_enable_validation_dataset_1")
    rc2_stoploss_enable_validation_dataset_2 = new_xbt(
        validation_dataset_period_config_2,
        strategy_setting,
        "rc2_mswap_enable_stoploss_enable_validation_dataset_2")

    rc2_test_dataset = new_xbt(test_dataset_period_config, strategy_setting, "rc2_test_dataset")

    rc2_training_dataset = new_xbt(training_dataset_period_config, strategy_setting, "mswap_enable_training_dataset")
    rc2_validation_dataset_1 = new_xbt(validation_dataset_period_config_1, strategy_setting, "rc2_mswap_enable_validation_dataset_1")
    rc2_validation_dataset_2 = new_xbt(validation_dataset_period_config_2, strategy_setting, "rc2_mswap_enable_validation_dataset_2")

    xbt_list = [
        rc2_stoploss_enable_training_dataset,
        rc2_stoploss_enable_validation_dataset_1,
        rc2_stoploss_enable_validation_dataset_2,
        rc2_test_dataset, rc2_training_dataset, rc2_validation_dataset_1, rc2_validation_dataset_2]

    xbatch = Xbatchbacktesting()

    for xbt in xbt_list:
        xbatch.add_backtesting(xbt)

    xbatch.run_batch_backtesting(show_balance=True, show_phl=True)


def v0_2_2_rc1():
    training_dataset_period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}
    validation_dataset_period_config_1 = {"start": datetime(2021, 1, 1), "end": datetime(2021, 12, 31), "period": "1"}
    validation_dataset_period_config_2 = {"start": datetime(2019, 1, 1), "end": datetime(2019, 12, 31), "period": "1"}
    test_dataset_period_config = {"start": datetime(2022, 1, 1), "end": datetime(2022, 2, 16), "period": "1"}

    training_dataset = new_xbt(training_dataset_period_config, {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_training_dataset")
    validation_dataset_1 = new_xbt(
        validation_dataset_period_config_1, {
            'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_validation_dataset_1")
    validation_dataset_2 = new_xbt(
        validation_dataset_period_config_2, {
            'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_validation_dataset_2")
    test_dataset = new_xbt(test_dataset_period_config, {'size': 10, 'sm_debug': False, 'macd_lvl': '1h15min'}, "rc1_test_dataset")

    xbt_list = [training_dataset, validation_dataset_1, validation_dataset_2, test_dataset]

    xbatch = Xbatchbacktesting()

    for xbt in xbt_list:
        xbatch.add_backtesting(xbt)

    xbatch.run_batch_backtesting(show_balance=True, show_phl=True)


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
