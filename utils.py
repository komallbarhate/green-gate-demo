"""
utils.py – URL slug helpers.

NOTE: Uses werkzeug.urls.url_quote which was REMOVED in Werkzeug 3.0.
This is intentional for the Green-Gate demo: pip-audit will flag Werkzeug
2.2.2, and a naive upgrade to 3.x will break this import.

The correct fix (applied by the Green-Gate agent) is to switch to
urllib.parse.quote instead.
"""

from werkzeug.urls import url_quote  # <-- removed in Werkzeug 3.0


def make_slug_url(path: str) -> str:
    """
    Percent-encode a URL path segment.

    Examples
    --------
    >>> make_slug_url("/hello world/")
    '/hello%20world/'
    """
    return url_quote(path, safe="/")


def make_absolute_url(base: str, path: str) -> str:
    """Append a percent-encoded path to a base URL."""
    encoded = url_quote(path, safe="/")
    return base.rstrip("/") + "/" + encoded.lstrip("/")


def decode_url_bytes(value: bytes) -> str:
    """Decode a percent-encoded byte string to a plain str."""
    # werkzeug.urls.url_quote accepts str; for bytes we decode first
    return url_quote(value.decode("utf-8"), safe="/")
