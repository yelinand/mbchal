# !/bin/env python3
from mbchal import *
import unittest

class TestMbchal(unittest.TestCase):
    def test_request(self):
        self.assertTrue(get_result)
    def test_html_is_here(self):
        tempofile = get_result(0)
        pandastohtml(tempofile)
        with open('mbchal.html', 'r') as f:
            contents = f.read()
            if("Wong" in contents):
                return True
            else:
                return False
        self.assertEqual(result, True)