## Student Name: Javeria Alam
## Student ID: 218714451

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

def test_no_events_full_day_available():
    """
    When no events exist, the entire working day excluding lunch should be available.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    # Earliest slot is 09:00, latest is 16:00 (so it ends by 17:00)
    assert "09:00" in slots
    assert "16:00" in slots
    # No slots during lunch
    assert all(not s.startswith("12") for s in slots)

def test_meeting_too_long_for_remaining_time():
    """
    Meetings longer than the remaining free time should not be scheduled.
    """
    events = [{"start": "09:00", "end": "16:30"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    # Only 16:30–17:00 is free, too short for 60 min
    assert slots == []

def test_multiple_back_to_back_events():
    """
    Multiple consecutive events should leave only proper gaps available.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:15", "end": "11:15"},
        {"start": "11:30", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    # Slot between 12:00–12:30 is blocked (lunch), next available should be 13:00
    assert "13:00" in slots
    assert "11:15" not in slots  # overlaps with next event
    assert "09:15" not in slots  # overlaps with first event

def test_event_ends_at_work_end():
    """
    An event ending exactly at work end should not block earlier valid slots.
    """
    events = [{"start": "16:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    # Latest meeting should end by 16:30 to avoid overlap
    assert "16:00" not in slots
    assert "15:30" in slots

def test_meeting_fits_before_first_event():
    """
    A meeting that fits before the first event of the day should be scheduled.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=45, day="2026-02-01")

    # Slot should exist before 10:00, respecting granularity
    assert "09:00" in slots
    assert "09:15" in slots
    assert "09:30" in slots
    assert "10:00" not in slots  # overlaps with event

