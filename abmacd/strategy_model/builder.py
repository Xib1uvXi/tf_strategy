
from abmacd.strategy_model.mswap_helper import MswapHelper
from abmacd.strategy_model.signal_model.ma_filter_sm import MaFilterSignalModel
from abmacd.strategy_model.signal_model.macd_sm import ABMacdSignalModel
from abmacd.strategy_model.v3_abmacd import ABMacdStrategyModelV3


def NewABMacdStrategyModel(mswap_enable: bool = False) -> ABMacdStrategyModelV3:
    abmacd_sm = ABMacdSignalModel()
    b_ma_filter = MaFilterSignalModel()
    # TODO fixme
    mswap = MswapHelper(mswap_enable)

    return ABMacdStrategyModelV3(abmacd_sm, b_ma_filter, mswap)
