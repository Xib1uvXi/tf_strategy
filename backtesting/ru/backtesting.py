import sys  # nopep8
import os  # nopep8
root_path = os.getcwd()  # nopep8
sys.path.append(root_path)  # nopep8
from util import gen_test_name
from config import default_ru88_param_config
from abmacd import vnpy_backtesting_current_strategy, vnpy_backtesting_current_strategy_setting
from xbacktesting.xvnpy_backtesting import Xbacktesting
from datetime import datetime


if __name__ == '__main__':
    period_config = {"start": datetime(2020, 1, 1), "end": datetime(2020, 12, 31), "period": "1"}

    xbt = Xbacktesting(
        strategy_class=vnpy_backtesting_current_strategy,
        param_config=default_ru88_param_config,
        period_config=period_config,
        strategy_setting=vnpy_backtesting_current_strategy_setting,
        test_name=gen_test_name(
            period_config,
            "backtesting"))
    xbt.run_backtesting(output=True)
