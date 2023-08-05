import unittest
import logging
from kinnaird_utils import text_parser_utils

logger = logging.getLogger(__name__)


def get_input(text):
    return input(text)


def answer():
    ans = get_input('enter yes or no')
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'


class TextTestCase(unittest.TestCase):
    def test_strip_special_characters(self):
        input_string = "Special $#! characters   spaces 888323"
        result = text_parser_utils.strip_special_characters(input_string)
        expected_output = "Specialcharactersspaces888323"
        self.assertEqual(result, expected_output)

    def test_parse_text_for_url(self):
        # Case: Base URL
        some_args = f"-u 'http://testphp.vulnweb.com' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com")
        # Case: /sup.html
        some_args = f"-u 'http://testphp.vulnweb.com/sup.html' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com/sup.html")
        # Case: With query parameters
        some_args = f"-u 'http://testphp.vulnweb.com/sup.html?bruh' --crawl -l 3 --params --blind --skip"
        result = text_parser_utils.parse_text_for_url(string=some_args)
        self.assertEqual(result, "http://testphp.vulnweb.com/sup.html?bruh")

