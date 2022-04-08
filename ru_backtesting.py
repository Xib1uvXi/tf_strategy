from datetime import datetime

from abmacd.abmacd_v2 import ABMACDStrategy
from backtesting_tool import chart, phl_chart, run_backtesting, show_portafolio

one_year = {"start": datetime(2021, 2, 16),
            "end": datetime(2022, 2, 16), "period": 1}
ten_year = {"start": datetime(2012, 2, 16), "end": datetime(
    2022, 2, 16), "period": 10}

tasks = ['1d4h', '1d1h', '1h15min']
logs = []
dfs = []


def run(period: int, tasks):
    tm = one_year
    if period == 10:
        tm = ten_year

    for task in tasks:
        engine = run_backtesting(
            strategy_class=ABMACDStrategy,
            setting={'size': 10, 'macd_lvl': task, 'sm_debug': False},
            vt_symbol="RU88.SHFE",
            interval="1m",
            start=tm["start"],
            end=tm["end"],
            rate=0.45 / 10000,
            slippage=5,
            size=10,
            pricetick=5,
            capital=5_00_000
        )
        df = engine.calculate_result()
        dfs.append({'df': df, 'task': task})
        
        statistics = engine.calculate_statistics(output=False)
        log = f"周期：{tm['period']}年\t{task}\t 年化收益：\t {statistics['annual_return']:,.2f}%\t 百分比最大回撤：\t {statistics['max_ddpercent']:,.2f}%\t 夏普比率：\t {statistics['sharpe_ratio']:,.2f}"

        # engine.show_chart(df)
        logs.append(log)


run(1, tasks)
# run(10, tasks)

print("Strategy: ABMACD")
for log in logs:
    print(log)


chart(dfs)
phl_chart(dfs)
