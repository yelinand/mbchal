# !/bin/env python3
from mbchal import *
import unittest

class TestMbchal(unittest.TestCase):
    def test_request(self):
        self.assertTrue(get_result)
    def test_html_is_created(self):
        mock_dataframe = [{"first_name":"George","last_name":"Bluth"}]
        pandastohtml(mock_dataframe)
        with open('mbchal.html', 'r') as f:
            contents = f.read()
            self.assertIn("Bluth", contents)
            self.assertNotIn("Beth", contents)