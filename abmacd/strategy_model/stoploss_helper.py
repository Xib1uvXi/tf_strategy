from abmacd.strategy_model.riskctl_model.stop_loss import Stoploss


class StoplossHelper:
    enable: bool

    long_stoploss_line: float
    short_stoploss_line: float

    long_stoploss: Stoploss
    short_stoploss: Stoploss

    def __init__(self, enable: bool, long_stoploss_line: float, short_stoploss_line: float):
        self.enable = enable
        self.long_stoploss_line = long_stoploss_line
        self.short_stoploss_line = short_stoploss_line
        self.long_stoploss = Stoploss(1, self.long_stoploss_line)
        self.short_stoploss = Stoploss(-1, self.short_stoploss_line)

    def check_long_stoploss(self, price: float) -> bool:
        if not self.enable:
            return False
        return self.long_stoploss.need_close(price)

    def check_short_stoploss(self, price: float) -> bool:
        if not self.enable:
            return False
        return self.short_stoploss.need_close(price)
