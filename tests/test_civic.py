import os
import sys
sys.path.append('..')

import unittest
import pandas as pd
from helpers.civic import *


class CivicTests(unittest.TestCase):
    def set_up(self):
        pass


    def test_my_reps_valid(self):
        address = '951 Fell St Baltimore MD'
        reps = get_my_reps(address)

        self.assertIsInstance(reps, pd.core.frame.DataFrame)
        self.assertEqual(reps.shape, (5 , 3))


    def test_my_reps_invalid(self):
        address = '999 Wrong Address'

        self.assertRaises(Exception, get_my_reps, address)


    def test_state_reps_valid(self):
        state = 'MD'
        reps = get_state_reps(state)

        self.assertIsInstance(reps, pd.core.frame.DataFrame)


    def test_state_reps_invalid(self):
        state = 'ZZ'

        self.assertRaises(Exception, get_state_reps, state)


if __name__ == '__main__':
    unittest.main()
