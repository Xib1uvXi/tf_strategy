from datetime import datetime

from abmacd.abmacd_v2 import ABMACDStrategy
from backtesting_tool import run_backtesting, show_portafolio




tasks = ['1d4h', '1d1h', '1h15min']

logs = []

for task in tasks:
    engine = run_backtesting(
    strategy_class=ABMACDStrategy, 
    setting={'size':10, 'macd_lvl':task, 'sm_debug':False}, 
    vt_symbol="RU88.SHFE",
    interval="1m", 
    start=datetime(2021, 2, 16), 
    end=datetime(2022, 2, 16),
    rate=0.45 / 10000,
    slippage=5,
    size=10,
    pricetick=5,
    capital=5_00_000
    )
    df = engine.calculate_result()
    statistics = engine.calculate_statistics(output=False)
    log = f"{task}\t 年化收益：\t {statistics['annual_return']:,.2f}%\t 百分比最大回撤：\t {statistics['max_ddpercent']:,.2f}%\t 夏普比率：\t {statistics['sharpe_ratio']:,.2f}"

    logs.append(log)
    
print("Strategy: ABMACD")
print("周期： 1年")
for log in logs:
    print(log)

