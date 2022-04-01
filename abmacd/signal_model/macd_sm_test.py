import unittest

from macd_sm import ABMacdAction, ABMacdSignalModel

class TestAB(unittest.TestCase):
    def test_open(self):
        abm = ABMacdSignalModel()

        abm.update_b_signal_value(0.59, -16.9)
        abm.update_a_signal_value(21.33, 45.44)

        abm.update_b_signal_value(18.29, -9.86)
        abm.update_a_signal_value(37.09, 43.77)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_a_signal_value(47.09, 44.42)
        abm.update_b_signal_value(52.62, 23.04)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.A_OPEN_LONG)

        abm.update_b_signal_value(48.86, 28.21)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_b_signal_value(46.55, 31.87)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)
        
        abm.update_b_signal_value(46.60, 34.82)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_a_signal_value(51.88, 45.92)
        abm.update_b_signal_value(46.11, 37.08)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_b_signal_value(44.01, 38.47)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_b_signal_value(43.45, 39.52)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_b_signal_value(39.73, 39.52)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_a_signal_value(53.90, 47.51)
        abm.update_b_signal_value(37.56, 39.13)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.B_CLOSE_LONG)

        abm.update_b_signal_value(34.63, 38.23)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_b_signal_value(21.57, 34.90)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.EMPTY)

        abm.update_a_signal_value(44.09, 46.83)
        abm.update_b_signal_value(11.49, 30.22)
        r = abm.exec()
        self.assertEqual(r, ABMacdAction.A_RB_SHORT)

    
    def d1(self):
        abm = ABMacdSignalModel()




if __name__ == '__main__':
    unittest.main()