import unittest
from yt_downloader import Tracklist

class TestTracklist(unittest.TestCase):
    def test_get_timestamp(self):
        self.assertEqual(Tracklist.get_timestamp('7:38'), '00:07:38')
        self.assertEqual(Tracklist.get_timestamp('1:07:38'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('(1:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp(' 01:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('pre text "12" 01:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('01:07:38.513)'), '01:07:38.513')

        self.assertRaises(RuntimeError, Tracklist.get_timestamp, [' no timestamp'])