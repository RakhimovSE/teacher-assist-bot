import unittest

from src.google_calendar import gcal


class GCalTestCase(unittest.TestCase):
    def test_is_match(self):
        self.assertTrue(gcal.is_match('f'))
        self.assertTrue(gcal.is_match('_'))
        self.assertFalse(gcal.is_match('5'))
        self.assertTrue(gcal.is_match('foo'))
        self.assertTrue(gcal.is_match('_foo123'))
        self.assertTrue(gcal.is_match('f123oo'))
        self.assertFalse(gcal.is_match('123foo'))
        self.assertFalse(gcal.is_match('1_foo'))
        self.assertFalse(gcal.is_match('foo bar'))
        self.assertFalse(gcal.is_match('foo.bar'))


if __name__ == '__main__':
    unittest.main()
