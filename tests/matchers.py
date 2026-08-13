"""
Assertion matchers to be used across all tests.
"""

from datetime import UTC

from dirty_equals import IsNow, IsPositiveInt

__all__ = ["IsPositiveInt", "IsNowUTC"]

IsNowUTC = IsNow(iso_string=True, delta=5, tz=UTC)
