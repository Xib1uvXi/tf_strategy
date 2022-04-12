from curses import raw
import re
from typing import Callable
from unittest import result
from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime
from vnpy.trader.optimize import OptimizationSetting

from xbacktesting.xvnpy_backtesting import Xbacktesting

time_period_config = {
    "1": {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16)},
    "10": {"start": datetime(2012, 2, 16), "end": datetime(2022, 2, 16)},
}


class optimizer:
    opt_engine: BacktestingEngine
    param_config: dict
    strategy_class: type
    period: int
    opt_target_filter: Callable = None
    cg_target_filter: Callable = None
    cg_period: int = 0

    def __init__(self, strategy_class: type, param_config: dict, period: int):
        self.opt_engine = BacktestingEngine()
        self.strategy_class = strategy_class
        self.param_config = param_config
        self.period = period
        self._init_param(self.period)
        self.opt_engine.add_strategy(self.strategy_class, {})

        self._raw_opt_results = []
        self._filter_opt_results = []
        self.opt_results = []
        self.optimization_setting: OptimizationSetting = None

    def _init_param(self, period: int):
        start_date = time_period_config["1"]["start"]
        end_date = time_period_config["1"]["end"]

        if period == 10:
            start_date = time_period_config["10"]["start"]
            end_date = time_period_config["10"]["end"]

        self.opt_engine.set_parameters(
            vt_symbol=self.param_config["vt_symbol"],
            interval=self.param_config["interval"],
            start=start_date,
            end=end_date,
            rate=self.param_config["rate"],
            slippage=self.param_config["slippage"],
            size=self.param_config["size"],
            pricetick=self.param_config["pricetick"],
            capital=self.param_config["capital"]
        )

    def set_optimization_setting(self, optimization_setting: OptimizationSetting, opt_target_filter: Callable):
        self.optimization_setting = optimization_setting
        self.opt_target_filter = opt_target_filter
    
    def set_cg_setting(self, period: int, cg_target_filter: Callable):
        self.cg_period = period
        self.cg_target_filter = cg_target_filter

    def run_opt(self):
        if self.optimization_setting is None:
            print("请先设置优化参数")
            exit()

        if self.opt_target_filter is None:
            print("请先设置优化目标过滤器")
            exit()
        
        if self.cg_target_filter is None:
            print("请先设置cg目标过滤器")
            exit()

        if self.cg_period == 0:
            print("请先设置cg回测周期")
            exit()

        self._run_optimization()
        if len(self._filter_opt_results) > 0:
            for fr in self._filter_opt_results:
                self._cg_bt(fr)
        
        print("优化完成")

        self._show_opt_result()

    def _show_opt_result(self):

        if len(self.opt_results) == 0:
            print("没有优化结果")
            return

        for result in self.opt_results:
            self._sc_out_v1(result)

    
    def _sc_out_v1(self, result):
        opt_msg = f"周期:{self.period}\t 参数:{result['strategy_setting']}\t 年化收益:{result['opt_result']['annual_return']:,.2f}%\t 最大百分比回撤:{result['opt_result']['max_ddpercent']:,.2f}%\t 夏普率:{result['opt_result']['sharpe_ratio']:,.2f}\t 交易笔数:{result['opt_result']['total_trade_count']}"
        print(opt_msg)
        cg_msg = f"周期:{self.cg_period}\t 参数:{result['strategy_setting']}\t 年化收益:{result['cg_result']['annual_return']:,.2f}%\t 最大百分比回撤:{result['cg_result']['max_ddpercent']:,.2f}%\t 夏普率:{result['cg_result']['sharpe_ratio']:,.2f}\t 交易笔数:{result['cg_result']['total_trade_count']}"
        print(cg_msg)
        print('              ')

    def _run_optimization(self, output: bool = False):
        results = self.opt_engine.run_bf_optimization(
            self.optimization_setting, output)
        self._raw_opt_results = results

        filter_results = self.opt_target_filter(results)
        if filter_results is None:
            print("优化目标过滤器返回空值")
            exit()

        self._filter_opt_results = filter_results

    def _cg_bt(self, filter_result):
        strategy_setting = self._gen_cg_strategy_setting(filter_result[0])
        cg_xbt = Xbacktesting(
            self.strategy_class, self.param_config, self.cg_period, strategy_setting, '')

        cg_xbt.run_backtesting()

        if self._check_cg_bt_statistics(cg_xbt._statistics):
            result = {"strategy_setting": filter_result[0], "opt_result": filter_result[2], "cg_result": cg_xbt._statistics}
            self.opt_results.append(result)

    def _check_cg_bt_statistics(self, cg_bt_statistics: dict):
        if cg_bt_statistics is None:
            print("cg bt 回测结果为空")
            return False

        if self.cg_target_filter(cg_bt_statistics):
            return True

        return False

    def _gen_cg_strategy_setting(self, raw_setting: str):
        setting = eval(raw_setting)
        return setting

    def show_filter_opt_result(self):
        for result in self._filter_opt_results:
            msg: str = f"参数：{result[0]}, 目标：{result[1]}"
            print(msg)
