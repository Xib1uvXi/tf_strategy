from vnpy_ctastrategy.backtesting import BacktestingEngine
from datetime import datetime

from abmacd.abmacd_v2 import ABMACDStrategy
from abmacd.single_macd import SingleMACDStrategy

from vnpy.trader.constant import Offset, Direction

def print_trade_data(engine: BacktestingEngine):
    trade_data = engine.get_all_trades()

    print("================================trade data===============================")
    for data in trade_data:
        print("order_id: ",data.orderid, "time: ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'), "action: ", data.offset.value, data.direction.value, "price: ", data.price, "amount: ", data.volume)
        # print(data)



def trade_analyze(engine: BacktestingEngine):
    trade_data = engine.get_all_trades()

    print(f"交易笔数: {len(trade_data)}")

    initd = False
    dirc: int = 0
    open_time: datetime = None
    close_time: datetime = None
    volume: float = 0 
    close_volume: float = 0 
    open_price: float = 0
    close_price: float = 0
    no_calu_nel = 0
    win = 0
    count = 0
    total_nel = 0

    for data in trade_data:
        if not initd:
            if data.offset is Offset.OPEN:
                initd = True
                open_time = data.datetime
                open_price = data.price
                volume = data.volume
                if data.direction is Direction.LONG:
                    dirc = 1
                else:
                    dirc = -1
                
                continue
        
        if initd:
            if dirc != 0:
                # add pos
                if data.offset is Offset.OPEN:
                    if (dirc == 1 and data.direction is Direction.LONG) or (dirc == -1 and data.direction is Direction.SHORT):
                        tmp_v = volume
                        volume = volume + data.volume
                        open_price = (open_price*tmp_v + data.price*data.volume)/volume
                        continue
                    else:
                        print("error")
                        exit()
                
                # close pos
                if data.offset is Offset.CLOSE:
                    close_price = data.price
                    close_volume = data.volume

                    if close_volume != volume:
                        print("error  close_volume != volume")
                        print(volume)
                        print(data)
                        exit()

                    if (dirc == 1 and data.direction is Direction.SHORT):
                        no_calu_nel = close_price*close_volume - open_price*volume

                        if no_calu_nel > 0:
                            win = 1
                        
                        count = count + 1
                        total_nel = total_nel + no_calu_nel
                        print(f"做多\t开仓时间: {open_time}\t开仓价格: {open_price}\t平仓时间: {close_time}\t平仓价格: {close_price}\t平仓手数: {close_volume}\t收益: {no_calu_nel}\t是否胜利: {win}")
                    
                    elif (dirc == -1 and data.direction is Direction.LONG):
                        no_calu_nel = open_price*volume - close_price*close_volume

                        if no_calu_nel > 0:
                            win = 1
                        
                        count = count + 1
                        total_nel = total_nel + no_calu_nel
                        print(f"做空\t开仓时间: {open_time}\t开仓价格: {open_price}\t平仓时间: {close_time}\t平仓价格: {close_price}\t平仓手数: {close_volume}\t收益: {no_calu_nel}\t是否胜利: {win}")

                    dirc = 0
                    open_time = None
                    close_time = None
                    volume = 0 
                    close_volume = 0 
                    open_price = 0
                    close_price = 0
                    no_calu_nel = 0
                    win = 0
                    initd = False

    print(f"策略执行数: {count}\t 收益：{total_nel}")

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

    # result = engine.get_all_daily_results()
    # result.reverse()
    
    # for obj in result:
    #     print(obj.net_pnl)


    # print_trade_data(engine)
    return df

# def show_portafolio(df):
#     engine = BacktestingEngine()
#     engine.calculate_statistics(df)
#     # engine.show_chart(df)

# RU88
ru88_1_year = run_backtesting(
    strategy_class=ABMACDStrategy, 
    setting={'size':10, 'macd_lvl':'1h15min', 'sm_debug':False}, 
    vt_symbol="RU88.SHFE",
    interval="1m", 
    start=datetime(2021, 2, 16), 
    end=datetime(2022, 2, 16),
    rate=0.45 / 10000,
    slippage=5,
    size=10,
    pricetick=5,
    capital=5_00_000,
)
