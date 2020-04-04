import sys
sys.path.append('../..')

import unittest
import pandas as pd
from helpers.maplight import *


class MaplightTests(unittest.TestCase):
    def set_up(self):
        pass

    def test_candidate_record_valid(self):
        name = 'Chris Van Hollen'
        state = 'md'
        record = get_candidate_record(name, state)

        self.assertIsInstance(record, dict)
        self.assertEqual(len(record), 4)


    def test_candidate_record_invalid(self):
        name = 'Wrong Name'
        state = 'md'

        self.assertRaises(Exception, get_candidate_record, name, state)


    def test_all_contributions_valid(self):
        mlid = '4497'
        cycle = '2020'
        contribs = get_all_contributions(mlid, cycle)

        self.assertIsInstance(contribs, pd.core.frame.DataFrame)
        self.assertEqual(contribs.shape[1], 15)


    def test_all_contributions_invalid(self):
        mlid = '4497'
        cycle = '1900'

        self.assertRaises(Exception, get_all_contributions, mlid, cycle)


if __name__ == '__main__':
    unittest.main()
