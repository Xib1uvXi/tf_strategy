from vnpy_ctastrategy.backtesting import BacktestingEngine
from abmacd import ABMACDStrategy
from datetime import datetime

# def print_trade_data(engine: BacktestingEngine):
#     trade_data = engine.get_all_trades()

#     print("================================trade data===============================")
#     for data in trade_data:
#         # print(data)
#         print("order_id: ",data.orderid, "time: ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'), "action: ", print_action(data), "price: ", data.price, "amount: ", data.volume)


# def print_drawdown_trade(trade_data):
#     print("================================亏损交易===============================")
#     tmp = None

#     for data in trade_data:
#         if not tmp:
#             tmp = data
#         else:
#             if print_action(data) == '平空' and tmp.price < data.price:
#                 print("亏损交易！！！ ", "方向： 开空","时间：", tmp.datetime.strftime( '%Y-%m-%d %H-%M-%S'), " - ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'))

#             if print_action(data) == '平多' and tmp.price > data.price:
#                 print("亏损交易！！！ ", "方向： 开多","时间：", tmp.datetime.strftime( '%Y-%m-%d %H-%M-%S'), " - ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'))
            
#             tmp = None



# def print_action(data):
#     if data.offset.value == '开':
#         if data.direction.value == '多':
#             return '开多'
        
#         return '开空'
    
#     if data.direction.value == '多':
#         return '平空'
    
#     return '平多'

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="RU88.SHFE",
    interval="1m",
    start=datetime(2021, 2, 16),
    end=datetime(2022, 2, 16),
    rate=0.3 / 10000,
    slippage=0.2,
    size=30,
    pricetick=0.2,
    capital=1_000_000,
)
engine.add_strategy(ABMACDStrategy, {})

engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
# engine.show_chart()

#########
trade_data = engine.get_all_trades()

for data in trade_data:
     print("order_id: ",data.orderid, "time: ", data.datetime.strftime( '%Y-%m-%d %H-%M-%S'), "action: ", data.offset.value, data.direction.value, "price: ", data.price, "amount: ", data.volume)