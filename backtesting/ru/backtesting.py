import sys
import os
root_path = os.getcwd()
sys.path.append(root_path)
from datetime import datetime
from xbacktesting.xvnpy_backtesting import Xbacktesting
from abmacd import vnpy_backtesting_current_strategy, vnpy_backtesting_current_strategy_setting
from config import default_ru88_param_config
from util import gen_test_name


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
