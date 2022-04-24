
class MswapHelper:
    enable: bool
    swap_months: list
    must_close_days: list
    only_close_days: list

    def __init__(self, enable: bool, swap_months:list, must_close_days: list, only_close_days: list):
        self.must_close_days = must_close_days
        self.only_close_days = only_close_days
        self.swap_months = swap_months
        self.enable = enable
    
    def is_swap_month(self, bar_month: int) -> bool:
        if not self.enable:
            return False
        return bar_month in self.swap_months
    
    def is_must_close_day(self, bar_day: int) -> bool:
        if not self.enable:
            return False
        return bar_day in self.must_close_days

    def is_only_close_day(self, bar_day: int) -> bool:
        if not self.enable:
            return False
        return bar_day in self.only_close_days


