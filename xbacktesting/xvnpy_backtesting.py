from typing import Any, Dict, List
from pandas import DataFrame
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy.trader.optimize import OptimizationSetting
import plotly.graph_objects as go


class Xbacktesting:
    engine: BacktestingEngine
    strategy_class: type
    param_config: Dict[str, Any]
    period_config: Dict[str, Any]
    strategy_setting: Dict[str, Any]
    _df: DataFrame
    _statistics: Dict[str, Any]
    _test_name: str
    _xrecord: List[Dict[str, Any]]

    def __init__(
            self,
            strategy_class: type,
            param_config: Dict[str, Any],
            period_config: Dict[str, Any],
            strategy_setting: Dict[str, Any],
            test_name: str,
    ):
        self.engine = BacktestingEngine()
        self.strategy_class = strategy_class
        self.param_config = param_config
        self._test_name = test_name
        self.period_config = period_config
        self.strategy_setting = strategy_setting

        self._xrecord = []

        self._init_param()

    def _init_param(self):

        self.engine.set_parameters(
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

    def run_bf_optimization(self, optimization_setting: OptimizationSetting, output: bool = False):
        self.engine.add_strategy(self.strategy_class, {})
        results = self.engine.run_bf_optimization(optimization_setting, output=False)

        if output:
            for result in results:
                msg: str = f"参数：{result[0]}, 目标：{result[1]}"
                print(msg)

        return results

    def run_backtesting(self, output: bool = False):
        self.engine.add_strategy(
            strategy_class=self.strategy_class,
            setting=self.strategy_setting
        )
        self.engine.load_data()
        self.engine.run_backtesting()
        self._df = self.engine.calculate_result()
        self._statistics = self.engine.calculate_statistics(output=output)

    def show_trade_data(self):
        trade_data = self.engine.get_all_trades()
        print("================================trade data===============================")
        for data in trade_data:
            print("order_id: ", data.orderid, "time: ", data.datetime.strftime('%Y-%m-%d %H-%M-%S'), "action: ",
                  data.offset.value, data.direction.value, "price: ", data.price, "amount: ", data.volume)

    def unsafe_calculate_statistics(self):
        trade_data = self.engine.get_all_trades()

        trader = self.engine.strategy.trader
        if trader is None:
            print("trader is None")
            return

        for order in trader.orders:
            for id in order['order_id']:
                find = False
                for data in trade_data:
                    if id == data.vt_orderid:
                        find = True
                        record = {
                            "action": order['action'],
                            "direction": order['direction'],
                            "time": data.datetime.strftime('%Y-%m-%d %H-%M-%S'),
                            "order_price": order['price'],
                            "traded_price": data.price,
                            "amount": data.volume,
                            "order_id": data.vt_orderid,
                            "status": "traded"}
                        self._xrecord.append(record)
                        break

                if not find:
                    record = {
                        "action": order['action'],
                        "direction": order['direction'],
                        "time": "",
                        "order_price": order['price'],
                        "traded_price": "",
                        "amount": order['size'],
                        "order_id": id,
                        "status": "canceled"}
                    self._xrecord.append(record)

    def show_xrecord(self):
        if len(self._xrecord) == 0:
            self.unsafe_calculate_statistics()

        print("================================record===============================")
        for record in self._xrecord:
            if record['status'] == 'traded':
                print(f"order_id: {record['order_id']}\t action: {record['action']}\t status: {record['status']}\t direction: {record['direction']}\t amount: {record['amount']}\t order_price: {record['order_price']}\t time: {record['time']}\t traded_price: {record['traded_price']}")
            else:
                print(f"order_id: {record['order_id']}\t action: {record['action']}\t status: {record['status']}\t direction: {record['direction']}\t amount: {record['amount']}\t order_price: {record['order_price']}")

    def show_balance_chart(self):
        balance_line = go.Scatter(
            x=self._df.index,
            y=self._df["balance"],
            mode="lines",
            name=f"Blance - {self._test_name}",
        )

        fig = go.Figure(data=balance_line)

        fig.update_layout(title_text="资金曲线", xaxis_title="时间", yaxis_title="资金")
        fig.show()

    def show_phl_chart(self):
        phl_line = go.Scatter(
            x=self._df.index,
            y=self._df["net_pnl"],
            mode="lines",
            name=f"Daily Pnl - {self._test_name}",
        )
        fig = go.Figure(data=phl_line)

        fig.update_layout(title_text="收益曲线", xaxis_title="时间", yaxis_title="收益")
        fig.show()


class Xbatchbacktesting:
    engines: List[Xbacktesting] = []
    statistics_logs: List[str] = []
    dfs: List[Dict[str, Any]] = []

    def __init__(self):
        return

    def add_backtesting(self, engine: Xbacktesting):
        self.engines.append(engine)

    def run_batch_backtesting(self, show_balance: bool = False, show_phl: bool = False):
        for engine in self.engines:
            engine.run_backtesting()
            self.dfs.append({'df': engine._df, 'task': engine._test_name})
            log = f"周期：{engine.period_config['period']}年\t{engine._test_name}\t 年化收益：{engine._statistics['annual_return']:,.2f}%\t 百分比最大回撤： {engine._statistics['max_ddpercent']:,.2f}%\t 夏普比率：{engine._statistics['sharpe_ratio']:,.2f}"
            self.statistics_logs.append(log)

        for log in self.statistics_logs:
            print(log)

        if show_balance:
            self.balance_chart()

        if show_phl:
            self.phl_chart()

    def balance_chart(self):
        balance_data = []

        for i in self.dfs:
            df = i['df']
            balance_line = go.Scatter(
                x=df.index,
                y=df["balance"],
                mode="lines",
                name=f"Blance - {i['task']}",
            )

            balance_data.append(balance_line)

        fig = go.Figure(data=balance_data)

        fig.update_layout(title_text="资金曲线", xaxis_title="时间", yaxis_title="资金")
        fig.show()

    def phl_chart(self):
        data = []

        for i in self.dfs:
            df = i['df']
            pnl_line = go.Scatter(
                x=df.index,
                y=df["net_pnl"],
                mode="lines",
                name=f"Daily Pnl - {i['task']}",
            )

            data.append(pnl_line)

        fig = go.Figure(data=data)

        fig.update_layout(title_text="收益曲线", xaxis_title="时间", yaxis_title="收益")
        fig.show()
