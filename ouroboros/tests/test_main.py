#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ouroboros` package."""

import unittest

from ouroboros import main


class TestMain(unittest.TestCase):
    """Tests for `main` module."""

    def test_handler(self):
        """Test something."""
        expected = 'Hello, World!'
        actual = main.handler({}, None)
        self.assertEqual(expected, actual)
