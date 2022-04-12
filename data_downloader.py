# import re
# from vnpy.trader.database import BaseDatabase, get_database
# from vnpy.trader.constant import Exchange, Interval
# from vnpy.trader.object import HistoryRequest
# from vnpy.trader.datafeed import BaseDatafeed, get_datafeed
# from datetime import datetime

# symbols = {    
#     "SHFE": ["cu", "al", "zn", "pb", "ni", "sn", "au", "ag", "rb", "wr", "hc", "ss", "bu", "ru", "nr", "sp", "sc", "lu", "fu"],    
#     "DCE": ["c", "cs", "a", "b", "m", "y", "p", "fb","bb", "jd", "rr", "l", "v", "pp", "j", "jm", "i", "eg", "eb", "pg"],    
#     "CZCE": ["SR", "CF", "CY", "PM","WH", "RI", "LR", "AP","JR","OI", "RS", "RM", "TA", "MA", "FG", "SF", "ZC", "SM", "UR", "SA", "CL"],    
#     "CFFEX": ["IH","IC","IF", "TF","T", "TS"]}

# symbol_type = "88"

# database: BaseDatabase = get_database()
# datafeed: BaseDatafeed = get_datafeed()

# def download_data(req):
#     data = datafeed.query_bar_history(req)
#     if data:
#         database.save_bar_data(data)
#         return(len(data))

#     return 0

# start_date=datetime(2022, 1, 1)
# end_date=datetime(2022, 3, 31)
# interval=Interval.MINUTE,



# for exchange, symbols_list in symbols.items():
#     for s in symbols_list:
#         req = HistoryRequest(            
#             symbol=s+symbol_type,            
#             exchange=Exchange(exchange),            
#             start=start_date,            
#             interval=interval,            
#             end=end_date,        
#         )

#         s = download_data(req)
#         print(f"{req.symbol}历史数据下载完成", "数量：", s)




import re
from vnpy.trader.database import BaseDatabase, get_database
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import HistoryRequest
from vnpy.trader.datafeed import BaseDatafeed, get_datafeed
from datetime import datetime

symbols = {
    "SHFE": ["CU", "AL", "ZN", "PB", "NI", "SN", "AU", "AG", "RB", "WR", "HC", "SS", "BU", "RU", "NR", "SP", "SC", "LU", "FU"],
    "DCE": ["C", "CS", "A", "B", "M", "Y", "P", "FB","BB", "JD", "RR", "L", "V", "PP", "J", "JM", "I", "EG", "EB", "PG"],
    "CZCE": ["SR", "CF", "CY", "PM","WH", "RI", "LR", "AP","JR","OI", "RS", "RM", "TA", "MA", "FG", "SF", "ZC", "SM", "UR", "SA", "CL"],
    "CFFEX": ["IH","IC","IF", "TF","T", "TS"]
}

symbol_type = "88"

database: BaseDatabase = get_database()
datafeed: BaseDatafeed = get_datafeed()

def download_data(req):
    data = datafeed.query_bar_history(req)
    if data:
        database.save_bar_data(data)
        return(len(data))

    return 0

# shfe = ["CU", "AL", "ZN", "PB", "NI", "SN", "AU", "AG", "RB", "WR", "HC", "SS", "BU", "RU", "NR", "SP", "SC", "LU", "FU"]
# dec = ["C", "CS", "A", "B", "M", "Y", "P", "FB","BB", "JD", "RR", "L", "V", "PP", "J", "JM", "I", "EG", "EB", "PG"]
# czce = ["SR", "CF", "CY", "PM","WH", "RI", "LR", "AP","JR","OI", "RS", "RM", "TA", "MA", "FG", "SF", "ZC", "SM", "UR", "SA"]
# cffex = ["IH","IC","IF", "TF","T", "TS"]

# for na in  shfe:
#     req = HistoryRequest(
#         symbol=na+symbol_type,
#         exchange=Exchange.CZCE,
#         start=datetime(2012, 1, 1),
#         interval=Interval.MINUTE,
#         end=datetime(2022, 3, 31),
#     )

#     s = download_data(req)
#     print(f"{req.symbol}历史数据下载完成", "数量：", s)

req = HistoryRequest(
    symbol='RU88',
    exchange=Exchange.SHFE,
    start=datetime(2022, 1, 1),
    interval=Interval.TICK,
    end=datetime(2022, 3, 31),
)

s = download_data(req)
print(f"{req.symbol}历史数据下载完成", "数量：", s)