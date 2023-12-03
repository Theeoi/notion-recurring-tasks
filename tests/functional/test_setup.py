#!/usr/bin/env python

import main


def test_header():
    assert isinstance(main.HEADERS, dict)
