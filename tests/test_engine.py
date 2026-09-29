from datetime import datetime

import pytest

from conftest import LOG_DIR
from engine import parse_timestamp, severity, detect_gaps, GapDetector


# --- parse_timestamp ---

@pytest.mark.parametrize('line, expected', [
    ('2025-03-28 10:00:00 System start', datetime(2025, 3, 28, 10, 0, 0)),
    ('2025-03-28T10:00:00Z System start', datetime(2025, 3, 28, 10, 0, 0)),
    ('1.2.3.4 - - [28/Mar/2025:10:00:00 +0000] "GET / HTTP/1.1" 200', datetime(2025, 3, 28, 10, 0, 0)),
])
def test_parses_formats_with_year(line, expected):
    assert parse_timestamp(line) == expected


def test_syslog_takes_year_from_previous_timestamp():
    ref = datetime(2025, 3, 28, 12, 0, 0)
    assert parse_timestamp('Mar 28 12:01:00 host sshd[1]: Accepted', ref) == datetime(2025, 3, 28, 12, 1, 0)


def test_syslog_single_digit_day_padding():
    ref = datetime(2025, 3, 1)
    assert parse_timestamp('Mar  5 08:00:00 host cron', ref) == datetime(2025, 3, 5, 8, 0, 0)


def test_syslog_without_reference_uses_current_year():
    assert parse_timestamp('Mar 28 12:01:00 host app').year == datetime.now().year


def test_syslog_year_rollover():
    ref = datetime(2024, 12, 31, 23, 59, 50)
    assert parse_timestamp('Jan  1 00:00:10 host app', ref) == datetime(2025, 1, 1, 0, 0, 10)


@pytest.mark.parametrize('line', ['', 'INVALID ENTRY HERE', '2025-13-45 10:00:00 bad date'])
def test_unparseable_lines_return_none(line):
    assert parse_timestamp(line) is None


# --- severity ---

@pytest.mark.parametrize('seconds, expected', [
    (31, 'LOW'), (59.9, 'LOW'), (60, 'MEDIUM'), (299, 'MEDIUM'), (300, 'CRITICAL'), (7200, 'CRITICAL'),
])
def test_severity_bands(seconds, expected):
    assert severity(seconds) == expected


# --- detect_gaps on sample logs ---

def test_clean_log_has_no_findings():
    stats = detect_gaps(f'{LOG_DIR}/clean.log')
    assert stats.success
    assert stats.gaps == [] and stats.reversals == []
    assert stats.total_missing_time == 0


def test_tampered_log_finds_all_gaps():
    stats = detect_gaps(f'{LOG_DIR}/tampered.log')
    assert [(g.duration, g.severity) for g in stats.gaps] == [
        (40, 'LOW'), (50, 'LOW'), (45, 'LOW'), (435, 'CRITICAL'), (880, 'CRITICAL'), (2040, 'CRITICAL'),
    ]
    assert stats.gaps_by_sev == {'LOW': 3, 'MEDIUM': 0, 'CRITICAL': 3}
    assert stats.total_missing_time == 3490
    assert stats.gaps[3].notes == 'Line 5-7'


def test_corrupted_log():
    stats = detect_gaps(f'{LOG_DIR}/corrupted.log')
    # Syslog line gets 2025, not 1900, so no bogus 125-year gap
    assert all(g.duration < 3600 for g in stats.gaps)
    assert [(g.duration, g.severity) for g in stats.gaps] == [(240, 'MEDIUM'), (900, 'CRITICAL')]
    assert len(stats.reversals) == 1
    rev = stats.reversals[0]
    assert rev.kind == 'REVERSAL' and rev.duration == 70 and rev.notes.startswith('Line 4-5')
    assert stats.unparsed_lines == 2
    assert stats.total_lines == 8


def test_reversals_not_counted_as_missing_time():
    stats = detect_gaps(f'{LOG_DIR}/corrupted.log')
    assert stats.total_missing_time == 240 + 900


def test_threshold_is_respected():
    stats = detect_gaps(f'{LOG_DIR}/tampered.log', threshold=300)
    assert [g.duration for g in stats.gaps] == [435, 880, 2040]


def test_any_extension_is_accepted(tmp_path):
    log = tmp_path / 'syslog'
    log.write_text('2025-01-01 00:00:00 a\n2025-01-01 00:10:00 b\n')
    assert len(detect_gaps(str(log)).gaps) == 1


def test_quoted_path_is_accepted():
    assert detect_gaps(f'"{LOG_DIR}/tampered.log"').success


# --- invalid input never produces fake findings ---

def test_missing_file_reports_error_without_fake_data():
    stats = detect_gaps('does/not/exist.log')
    assert not stats.success
    assert 'not found' in stats.error.lower()
    assert stats.gaps == [] and stats.total_lines == 0 and stats.total_missing_time == 0


def test_directory_reports_error(tmp_path):
    stats = detect_gaps(str(tmp_path))
    assert not stats.success and stats.gaps == []


def test_binary_junk_does_not_crash(tmp_path):
    log = tmp_path / 'junk.log'
    log.write_bytes(b'\xff\xfe\x00garbage\n2025-01-01 00:00:00 ok\n')
    stats = detect_gaps(str(log))
    assert stats.success and stats.unparsed_lines == 1


# --- GapDetector ---

def test_incremental_detector_matches_batch_scan():
    with open(f'{LOG_DIR}/tampered.log') as f:
        lines = f.readlines()
    detector = GapDetector()
    events = [e for e in map(detector.feed, lines) if e]
    assert events == detect_gaps(f'{LOG_DIR}/tampered.log').gaps
