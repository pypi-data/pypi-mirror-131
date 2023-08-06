#!/usr/bin/env python

"""Tests for `pitrading` package."""


import unittest

import pandas as pd

from pitrading import pitrading
from pitrading.holidays import Holidays


class TestPitrading(unittest.TestCase):
    """Tests for `pitrading` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        Holidays.tradingday("20220101")
        Holidays.tradingday("20221001")
        Holidays.tradingday("20220901")
        Holidays.tradingday("20221201")
        