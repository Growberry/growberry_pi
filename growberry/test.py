import unittest

class TestConfig(unittest.TestCase):

    def test_sensors(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")