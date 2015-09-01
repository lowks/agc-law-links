__author__ = 'lowks'

import unittest
import json
from agc_law import Law, LawPages
from mock import patch, Mock


class AGCTest(unittest.TestCase):

    def setUp(self):
        self.law = Law()
        self.input_html = """<div class="article-content">
<table><a href="hoho">hoho</a></table>
<table><a href="hehe">hehe</a></table></div>"""
        # import ipdb; ipdb.set_trace()
        self.lp = LawPages(self.input_html)

    @patch("agc_law.requests")
    @patch("agc_law.LawPages")
    def test_find_laws(self, mock_law_pages, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_law_pages.return_value.give_pages.return_value = 'hulahoop'
        self.assertEqual(self.law.find_laws(), 'hulahoop')

    @patch("agc_law.requests")
    def test_find_laws_exception(self, mock_requests):
        mock_requests.get.return_value.status_code = 400
        with self.assertRaises(SystemExit):
            self.law.find_laws()

    @patch("agc_law.Law.fetch")
    def test_dump_to_json(self, mock_fetch):
        mock_fetch.return_value = "mypage"
        self.assertTrue(self.law.dump_to_json(),
                        json.dumps({'lom': list("mypage")}))

    def test_lp_give_pages(self):
        self.assertListEqual(self.lp.give_pages(),
                             [(u'hehe', 'http://www.agc.gov.myhehe')])

    @patch("agc_law.LawPages.extract")
    def test_extract_to_json(self, mock_extract):
        mock_extract.return_value = "gula"
        data = self.lp.extract_to_json()
        self.assertEqual(data, '{\n    "lom": "gula"\n}')