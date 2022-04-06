from vnpy_ctastrategy.backtesting import BacktestingEngine

def print_trade_data(engine: BacktestingEngine):
    trade_data = engine.get_all_trades()

    print("================================trade data===============================")
    for data in trade_data:
        print("order_id: ",data.orderid, "time: ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'), "action: ", data.offset.value, data.direction.value, "price: ", data.price, "amount: ", data.volume)


def run_backtesting(strategy_class, setting, vt_symbol, interval, start, end, rate, slippage, size, pricetick, capital, show_trade_data=False):
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
    # engine.calculate_statistics()

    if show_trade_data:
        print_trade_data(engine)
    
    return engine

def show_portafolio(df):
    engine = BacktestingEngine()
    engine.calculate_statistics(df)
    engine.show_chart(df)