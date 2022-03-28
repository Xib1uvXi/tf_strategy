from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime

from abmacd_v2 import ABMACDStrategy

def print_trade_data(engine: BacktestingEngine):
    trade_data = engine.get_all_trades()

    print("================================trade data===============================")
    for data in trade_data:
        print("order_id: ",data.orderid, "time: ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'), "action: ", data.offset.value, data.direction.value, "price: ", data.price, "amount: ", data.volume)


#########


def run_backtesting(strategy_class, setting, vt_symbol, interval, start, end, rate, slippage, size, pricetick, capital):
    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=interval,
        start=start,
        end=end,
        rate=rate,
        slippage=slippage,
        size=size,
        pricetick=pricetick,
        capital=capital    
    )
    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
    # print_trade_data(engine)
    return df

# def show_portafolio(df):
#     engine = BacktestingEngine()
#     engine.calculate_statistics(df)
#     # engine.show_chart(df)

# RU88
ru88_1_year = run_backtesting(
    strategy_class=ABMACDStrategy, 
    setting={'size':10}, 
    vt_symbol="RU88.SHFE",
    interval="1m", 
    start=datetime(2021, 4, 1), 
    end=datetime(2022, 1, 30),
    rate=0.45 / 10000,
    slippage=5,
    size=10,
    pricetick=5,
    capital=5_00_000,
)