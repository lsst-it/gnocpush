#!/usr/bin/env python3

from gnocpush.utils import sanitize_severity


def test_critical():
    words = ["critical", "CRITICAL", "cRiTiCaL", "Critical"]
    for word in words:
        assert sanitize_severity(word) == 'Critical'


def test_major():
    words = ["major", "MAJOR", "mAjOr", "Major"]
    for word in words:
        assert sanitize_severity(word) == 'Major'


def test_minor():
    words = ["minor", "MINOR", "mInOr", "Minor"]
    for word in words:
        assert sanitize_severity(word) == 'Minor'


def test_unknown():
    words = ["unknown", "UNKNOWN", "uNkNoWn", "Unknown", "foo", "bar", "baz"]
    for word in words:
        assert sanitize_severity(word) == 'Unknown'


def test_ok():
    words = ["ok", "OK", "oK", "Ok"]
    for word in words:
        assert sanitize_severity(word) == 'OK'
