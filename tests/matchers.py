"""
Assertion matchers to be used across all tests.
"""

from datetime import UTC

from dirty_equals import IsNow, IsPositiveInt

IsPositiveInt = IsPositiveInt
IsNowUTC = IsNow(iso_string=True, delta=5, tz=UTC)
