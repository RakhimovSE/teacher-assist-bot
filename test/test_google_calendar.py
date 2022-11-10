import unittest
from datetime import datetime

from src.google_calendar import Event, helpers


class GoogleCalendarTestCase(unittest.TestCase):
    def test_is_match(self):
        valid_var_names = ['f', '_', 'foo', '_foo123', 'f123oo']
        invalid_var_names = ['5', '123foo', '1_foo', 'foo bar', 'foo.bar']
        [self.assertTrue(helpers.is_match(value)) for value in valid_var_names]
        [self.assertFalse(helpers.is_match(value)) for value in invalid_var_names]

    def test_get_event_args(self):
        start = datetime(2022, 11, 9, 9, 0, 0)

        for description, args in [
            ('hello world', {}),
            ('hello\ntelegram_id=123', {'telegram_id': '123'}),
            ('line 1\nwrong key=281\nRIGHT_key=yo\n1wrong=key\n_right_key2=true\nline 2',
             {'RIGHT_key': 'yo', '_right_key2': 'true'}),
        ]:
            event = Event("Test event", start, description=description)
            self.assertEqual(event.args, args)


if __name__ == '__main__':
    unittest.main()
