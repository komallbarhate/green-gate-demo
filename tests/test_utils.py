"""
tests/test_utils.py – Tests for utils.py

These tests PASS on Werkzeug 2.2.2 (pinned in requirements.txt).
They FAIL with an ImportError on Werkzeug 3.0+ because url_quote was
removed from werkzeug.urls.

This is the intentional "red" moment in the Green-Gate demo.
"""

import pytest

from utils import decode_url_bytes, make_absolute_url, make_slug_url


# ---------------------------------------------------------------------------
# Test: make_slug_url
# ---------------------------------------------------------------------------

def test_make_slug_url_encodes_spaces():
    assert make_slug_url("/hello world/") == "/hello%20world/"


def test_make_slug_url_preserves_slashes():
    assert make_slug_url("/a/b/c") == "/a/b/c"


def test_make_slug_url_encodes_special_chars():
    result = make_slug_url("/café")
    # é is percent-encoded
    assert "%" in result
    assert result.startswith("/")


# ---------------------------------------------------------------------------
# Test: make_absolute_url
# ---------------------------------------------------------------------------

def test_make_absolute_url_joins_correctly():
    result = make_absolute_url("https://example.com", "/path to/file")
    assert result == "https://example.com/path%20to/file"


# ---------------------------------------------------------------------------
# Test: decode_url_bytes
# ---------------------------------------------------------------------------

def test_decode_url_bytes_plain():
    assert decode_url_bytes(b"/plain/path") == "/plain/path"
