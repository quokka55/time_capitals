#!/usr/bin/env python3
"""
Show current time for all Australian state and territory capitals with
timezone information. Offsets and daylight saving come from the system
timezone database, so they stay correct throughout the year.
"""

import datetime
from zoneinfo import ZoneInfo


def get_capitals():
    """Return a dict of Australian state/territory capitals -> IANA timezone."""
    return {
        "Sydney": "Australia/Sydney",
        "Melbourne": "Australia/Melbourne",
        "Brisbane": "Australia/Brisbane",
        "Hobart": "Australia/Hobart",
        "Canberra": "Australia/Canberra",
        "Adelaide": "Australia/Adelaide",
        "Darwin": "Australia/Darwin",
        "Perth": "Australia/Perth",
    }


def format_offset(offset):
    """Format a timedelta UTC offset as +HH:MM."""
    total_minutes = int(offset.total_seconds()) // 60
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def show_times():
    """Display current time for all capitals."""
    now = datetime.datetime.now().astimezone()

    print("=" * 60)
    print("AUSTRALIAN CAPITALS - CURRENT TIME")
    print(f"Reference Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')} (Local System Time)")
    print("=" * 60)
    print()

    for city, tz_name in get_capitals().items():
        try:
            local_time = now.astimezone(ZoneInfo(tz_name))
            is_dst = bool(local_time.dst())

            print(f"{city:15} | {local_time.strftime('%H:%M')} ({local_time.strftime('%Z')})")
            print(f"{'':15} | Offset: UTC{format_offset(local_time.utcoffset())}")
            print(f"{'':15} | DST: {'Yes' if is_dst else 'No'}")
            print()
        except Exception as e:
            print(f"{city:15} | ERROR: {e}")
            print()


def show_timezone_overview():
    """Show each capital's offset in winter (July) and summer (January)."""
    year = datetime.date.today().year
    winter = datetime.datetime(year, 7, 1, 12)
    summer = datetime.datetime(year, 1, 1, 12)

    print("=" * 60)
    print("AUSTRALIAN TIMEZONE VARIATION OVERVIEW")
    print("=" * 60)
    print()
    print(f"{'City':15} | {'Winter (Jul)':18} | {'Summer (Jan)':18} | DST")
    print("-" * 60)

    for city, tz_name in get_capitals().items():
        tz = ZoneInfo(tz_name)
        w = winter.replace(tzinfo=tz)
        s = summer.replace(tzinfo=tz)
        has_dst = w.utcoffset() != s.utcoffset()
        w_str = f"{w.strftime('%Z')} UTC{format_offset(w.utcoffset())}"
        s_str = f"{s.strftime('%Z')} UTC{format_offset(s.utcoffset())}"
        print(f"{city:15} | {w_str:18} | {s_str:18} | {'Yes' if has_dst else 'No'}")
    print()


if __name__ == "__main__":
    show_times()
    show_timezone_overview()
