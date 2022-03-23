import string
from enum import Enum

class MacdSignalModel:
    name = ""
    # signal value
    dif0 = 0.0
    dif1 = 0.0
    dea0 = 0.0
    dea1 = 0.0
    init: int

    def __init__(self, name: string):
        self.name = name
        self.init = 0
    
    # update signal value
    def update(self, fast_macd0: float, slow_macd0: float):
        if self.init <= 1:
            self.init = self.init + 1
        # swap
        self.dif1 = self.dif0
        self.dea1 = self.dea0
        self.dif0 = fast_macd0
        self.dea0 = slow_macd0
    
    # cross signal
    def cross_over(self) -> bool:
        if self.init <= 1:
            return False

        return self.dif0 > self.dea0 and self.dif1 < self.dea1

    def cross_below(self) -> bool:
        if self.init <= 1:
            return False

        return self.dif0 < self.dea0 and self.dif1 > self.dea1

    def macd_gt_zero(self) -> bool:
        if self.init <= 1:
            return False

        return self.dif0 > 0.0 and self.dea0 > 0.0 and self.dif1 >= 0.0 and self.dea1 >= 0.0
    
    def dif_crossover_zero(self) -> bool:
        if self.init <= 1:
            return False

        return self.dif0 > 0.0 and self.dif1 <= 0.0

class ABMacdAction(Enum):
    A_OPEN_LONG = "A开多"
    A_OPEN_SHORT = "A开空"

    B_CLOSE_SHORT = "B平空"
    B_CLOSE_LONG = "B平多"

    B_OPEN_LONG = "B开多"
    B_OPEN_LONG_A = "B多回"
    B_OPEN_SHORT_A = "B空回"
    
    A_RB_SHORT = "A平多开空"
    A_RB_LONG = "A平空开多"
    
    EMPTY = "EMPTY"

class ABMacdSignalModel:
    asm: MacdSignalModel
    bsm: MacdSignalModel

    a_sv_init: bool
    b_sv_init: bool
    direction: int

    def __init__(self):
        self.asm = MacdSignalModel("A")
        self.bsm = MacdSignalModel("B")
        self.a_sv_init = False
        self.b_sv_init = False
        self.direction = 0

    def update_a_signal_value(self, fast_macd0: float, slow_macd0: float):
        self.asm.update(fast_macd0, slow_macd0)
        self.a_sv_init = True
    
    def update_b_signal_value(self, fast_macd0: float, slow_macd0: float):
        self.bsm.update(fast_macd0, slow_macd0)
        self.b_sv_init = True
    
    def exec(self) -> ABMacdAction:
        if self.a_sv_init == False and self.b_sv_init == False:
             return ABMacdAction.EMPTY
        
        if self.b_sv_init and not self.a_sv_init:
            # reset b_sv_init
            self.b_sv_init = False

            if self.direction == 0:
                return ABMacdAction.EMPTY
            
            if self.direction == 1:
                return self._b_handle_long()

            if self.direction == -1:
                return self._b_handle_short()
        
        if self.a_sv_init and self.b_sv_init:
            # reset a_sv_init & b_sv_init
            self.a_sv_init = False
            self.b_sv_init = False

            if self.direction == 0:
                return self._a_open()
            
            if self.direction == 1:
                if self.asm.macd_gt_zero() and self.asm.cross_below():
                    self.direction = -1
                    return ABMacdAction.A_RB_SHORT
                
                return self._b_handle_long()
            
            if self.direction == -1:
                if self.asm.macd_gt_zero() and self.asm.cross_over():
                    self.direction = 1
                    return ABMacdAction.A_RB_LONG
                
                return self._b_handle_short()
    
    def _a_open(self) -> ABMacdAction:
        if not self.asm.macd_gt_zero():
            return ABMacdAction.EMPTY
        
        if self.asm.cross_over():
            self.direction = 1
            return ABMacdAction.A_OPEN_LONG

        if self.asm.cross_below():
            self.direction = -1
            return ABMacdAction.A_OPEN_SHORT

        return ABMacdAction.EMPTY
    
    def _b_handle_long(self) -> ABMacdAction:
        if self.bsm.macd_gt_zero():
            if self.bsm.cross_below():
                return ABMacdAction.B_CLOSE_LONG
            
            if self.bsm.cross_over():
                return ABMacdAction.B_OPEN_LONG_A
            
            return ABMacdAction.EMPTY
        
        else:
            if self.bsm.dif_crossover_zero():
                return ABMacdAction.B_OPEN_LONG
            
            return ABMacdAction.EMPTY
    
    def _b_handle_short(self) -> ABMacdAction:
        if not self.bsm.macd_gt_zero():
            if self.bsm.dif_crossover_zero():
                return ABMacdAction.B_CLOSE_SHORT
            
            return ABMacdAction.EMPTY
        
        else:
            if self.bsm.cross_over():
                return ABMacdAction.B_CLOSE_SHORT
            
            if self.bsm.cross_below():
                return ABMacdAction.B_OPEN_SHORT_A
            
            return ABMacdAction.EMPTY

