"""The server clock.

ALWAYS use clock.now() instead of timezone.now(). That way the dev-only
"move clock forward" button changes every time rule (fees, today's totals...).
"""
from datetime import timedelta

from django.utils import timezone

_offset = timedelta(0)  # how far the clock has been moved forward


def now():
    return timezone.now() + _offset


def advance(minutes):
    global _offset
    _offset += timedelta(minutes=minutes)


def reset():
    global _offset
    _offset = timedelta(0)


def offset_minutes():
    return int(_offset.total_seconds() // 60)
