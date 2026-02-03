## Student Name: Javeria Alam
## Student ID: 218714451

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    WORK_START = 9 * 60      # 09:00
    WORK_END = 17 * 60       # 17:00
    LUNCH_START = 12 * 60    # 12:00
    LUNCH_END = 13 * 60      # 13:00
    GRANULARITY = 15         # minutes
    BUFFER = 15              # minutes after events

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # Convert events to minute ranges
    event_ranges = [
        (to_minutes(e["start"]), to_minutes(e["end"]))
        for e in events
    ]

    slots = []

    latest_start = WORK_END - meeting_duration
    start = WORK_START

    while start <= latest_start:
        end = start + meeting_duration

        # Rule: must not start during lunch break
        if LUNCH_START <= start < LUNCH_END:
            start += GRANULARITY
            continue

        conflict = False
        for ev_start, ev_end in event_ranges:
            # Apply buffer after events
            buffered_end = ev_end + BUFFER

            # Overlap check
            if not (end <= ev_start or start >= buffered_end):
                conflict = True
                break

        if not conflict:
            slots.append(to_time_str(start))

        start += GRANULARITY

    return slots
