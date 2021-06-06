from unittest.mock import patch

from django.test import TestCase
from django.core.management import call_command
from django.db.utils import OperationalError


class CommandTests(TestCase):

    def test_wait_for_db_when_db_is_ready(self):
        """test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """test wating for the db when db is not ready"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
