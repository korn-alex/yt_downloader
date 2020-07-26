import unittest
from unittest import mock
from secrets import token_hex
from yt_downloader import Tracklist


class TestTracklist(unittest.TestCase):
    def test_get_timestamp(self):
        self.assertEqual(Tracklist.get_timestamp('7:38'), '00:07:38')
        self.assertEqual(Tracklist.get_timestamp('1:07:38'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('(1:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp(' 01:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('pre text "12" 01:07:38)'), '01:07:38')
        self.assertEqual(Tracklist.get_timestamp('01:07:38.513)'), '01:07:38.513')

        self.assertRaises(RuntimeError, Tracklist.get_timestamp, ' no timestamp')
    
    def test_get_clean_trackname(self):
        self.assertEqual(Tracklist.get_clean_trackname(' %& name 4:53'), 'name')
        self.assertEqual(Tracklist.get_clean_trackname(' %& name 4:53 %/('), 'name')
        self.assertEqual(Tracklist.get_clean_trackname('(4:53:11) name ..'), 'name')
        self.assertEqual(Tracklist.get_clean_trackname('..(4:53:11) name ..k'), 'name k')
        self.assertRaises(AttributeError, Tracklist.get_clean_trackname, '..')
        self.assertEqual(Tracklist.get_clean_trackname('..5:53', name='myname'), 'myname')
        self.assertEqual(Tracklist.get_clean_trackname('..', name='f9bf78b9a18ce6d46a0cd2b0b86df9da'), 'f9bf78b9a18ce6d46a0cd2b0b86df9da')