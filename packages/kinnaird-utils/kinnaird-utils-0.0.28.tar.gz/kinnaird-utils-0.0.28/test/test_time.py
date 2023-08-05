import unittest
import logging
from kinnaird_utils.time import get_year_month_day_string

logger = logging.getLogger(__name__)


class TimeTestCase(unittest.TestCase):
    def test_get_year_month_day_string(self):
        """this is pretty much just to see the output while I am writing this, not to verify results or be a solid check at all"""
        results = get_year_month_day_string()
        print(results)

