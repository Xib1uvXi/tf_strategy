
class MswapHelper:
    enable: bool

    def __init__(self, enable: bool):
        
        self.enable = enable
    
    def is_swap_month(self, bar_month: int) -> bool:
        if not self.enable:
            return False
        return bar_month in [7, 12, 4]
    
    def is_must_close_day(self, bar_month: int, bar_day: int) -> bool:
        if not self.enable:
            return False
        
        if bar_month in [7, 12]:
            return bar_day in [29,30,31]
        
        if bar_month == 4:
            return bar_day in [28,29,30]
        
        return False


    def is_only_close_day(self, bar_month: int, bar_day: int) -> bool:
        if not self.enable:
            return False
        
        if bar_month in [7, 12]:
            return bar_day in [26,27,28]
        
        if bar_month == 4:
            return bar_day in [25,26,27]
        
        return False


