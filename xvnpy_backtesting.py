from pandas import DataFrame
from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime
import plotly.graph_objects as go

time_period_config = {
    "1": {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16)},
    "10": {"start": datetime(2012, 2, 16), "end": datetime(2022, 2, 16)},
}



class Xbacktesting:
    engine: BacktestingEngine
    strategy_class: type
    param_config: dict
    period: int
    strategy_setting: dict
    _df: DataFrame
    _statistics: dict
    _test_name: str

    def __init__(self, strategy_class: type, param_config: dict, period: int, strategy_setting: dict, test_name: str):
        self.engine = BacktestingEngine()
        self.strategy_class = strategy_class
        self.param_config = param_config
        self._test_name = test_name
        self.period = period
        self.strategy_setting = strategy_setting

    def _init_param(self, period: int):
        start_date = time_period_config["1"]["start"]
        end_date = time_period_config["1"]["end"]
        
        if period == 10:
            start_date = time_period_config["10"]["start"]
            end_date = time_period_config["10"]["end"]
        
        self.engine.set_parameters(
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
    
    def run_backtesting(self, output: bool = False):
        self._init_param(self.period)
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
    engines = []
    statistics_logs = []
    dfs = []

    def __init__(self):
        return
    
    def add_backtesting(self, engine: Xbacktesting):
        self.engines.append(engine)

    def run_batch_backtesting(self, show_balance: bool = False, show_phl: bool = False):
        for engine in self.engines:
            engine.run_backtesting()
            self.dfs.append({'df': engine._df, 'task': engine._test_name})
            log = f"周期：{engine.period}年\t{engine._test_name}\t 年化收益：\t {engine._statistics['annual_return']:,.2f}%\t 百分比最大回撤：\t {engine._statistics['max_ddpercent']:,.2f}%\t 夏普比率：\t {engine._statistics['sharpe_ratio']:,.2f}"
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
