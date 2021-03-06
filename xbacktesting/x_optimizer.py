from typing import Any, Callable, Dict, List, Optional, Tuple
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy.trader.optimize import OptimizationSetting

from xbacktesting.xvnpy_backtesting import Xbacktesting


class optimizer:
    opt_engine: BacktestingEngine
    param_config: Dict[str, Any]
    strategy_class: type
    period_config: Dict[str, Any]
    opt_target_filter: Optional[Callable[[List[Tuple[Any, ...]]], List[Tuple[Any, ...]]]] = None
    cg_target_filter: Optional[Callable[[Dict[str, Any]], bool]] = None
    cg_period_config: Dict[str, Any]

    def __init__(self, strategy_class: type, param_config: Dict[str, Any], period_config: Dict[str, Any]):
        self.opt_engine = BacktestingEngine()
        self.strategy_class = strategy_class
        self.param_config = param_config
        self.period_config = period_config
        self._init_param()
        self.opt_engine.add_strategy(self.strategy_class, {})

        self._raw_opt_results: Optional[List[Tuple[Any, ...]]] = []
        self.opt_results: List[Dict[str, Any]] = []
        self.optimization_setting: OptimizationSetting = None

    def _init_param(self):

        self.opt_engine.set_parameters(
            vt_symbol=self.param_config["vt_symbol"],
            interval=self.param_config["interval"],
            start=self.period_config["start"],
            end=self.period_config["end"],
            rate=self.param_config["rate"],
            slippage=self.param_config["slippage"],
            size=self.param_config["size"],
            pricetick=self.param_config["pricetick"],
            capital=self.param_config["capital"]
        )

    def set_optimization_setting(self, optimization_setting: OptimizationSetting,
                                 opt_target_filter: Callable[[List[Tuple[Any, ...]]], List[Tuple[Any, ...]]]):
        self.optimization_setting = optimization_setting
        self.opt_target_filter = opt_target_filter

    def set_cg_setting(self, cg_period_config: Dict[str, Any], cg_target_filter: Callable[[Dict[str, Any]], bool]):
        self.cg_period_config = cg_period_config
        self.cg_target_filter = cg_target_filter

    def run_opt(self):
        if self.optimization_setting is None:
            print("????????????????????????")
            exit()

        if self.opt_target_filter is None:
            print("?????????????????????????????????")
            exit()

        if self.cg_target_filter is None:
            print("????????????cg???????????????")
            exit()

        if self.cg_period_config is None:
            print("????????????cg????????????")
            exit()

        results = self._run_optimization()

        for fr in results:
            self._cg_bt(fr)

        print("????????????")

        self._show_opt_result()

    def _show_opt_result(self):

        if len(self.opt_results) == 0:
            print("??????????????????")
            return

        for result in self.opt_results:
            self._sc_out_v1(result)

    def _sc_out_v1(self, result):
        opt_msg = f"??????:{self.period_config['period']}\t ??????:{result['strategy_setting']}\t ????????????:{result['opt_result']['annual_return']:,.2f}%\t ?????????????????????:{result['opt_result']['max_ddpercent']:,.2f}%\t ?????????:{result['opt_result']['sharpe_ratio']:,.2f}\t ????????????:{result['opt_result']['total_trade_count']}"
        print(opt_msg)
        cg_msg = f"??????:cg{self.cg_period_config['period']}\t ??????:{result['strategy_setting']}\t ????????????:{result['cg_result']['annual_return']:,.2f}%\t ?????????????????????:{result['cg_result']['max_ddpercent']:,.2f}%\t ?????????:{result['cg_result']['sharpe_ratio']:,.2f}\t ????????????:{result['cg_result']['total_trade_count']}"
        print(cg_msg)
        # print('              ')

    def _run_optimization(self, output: bool = False) -> List[Tuple[Any, ...]]:
        results = self.opt_engine.run_bf_optimization(
            self.optimization_setting, output)
        self._raw_opt_results = results

        filter_results: Optional[List[Tuple[Any, ...]]] = self.opt_target_filter(results) if self.opt_target_filter else results
        if filter_results is None:
            print("?????????????????????????????????")
            exit()

        return filter_results

    def _cg_bt(self, filter_result):
        strategy_setting = self._gen_cg_strategy_setting(filter_result[0])
        cg_xbt = Xbacktesting(
            self.strategy_class, self.param_config, self.cg_period_config, strategy_setting, '')

        cg_xbt.run_backtesting()

        if self._check_cg_bt_statistics(cg_xbt._statistics):
            result = {
                "strategy_setting": filter_result[0],
                "opt_result": filter_result[2],
                "cg_result": cg_xbt._statistics,
            }
            self.opt_results.append(result)

    def _check_cg_bt_statistics(self, cg_bt_statistics: Dict[str, Any]):
        if cg_bt_statistics is None:
            print("cg bt ??????????????????")
            return False

        if self.cg_target_filter and self.cg_target_filter(cg_bt_statistics):
            return True

        return False

    def _gen_cg_strategy_setting(self, raw_setting: str):
        setting = eval(raw_setting)
        return setting
