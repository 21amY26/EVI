import threading
import time

from live import follow


def append_later(path, lines, delay=0.2, step=0.05):
    def write():
        time.sleep(delay)
        for line in lines:
            with open(path, 'a') as f:
                f.write(line)
            time.sleep(step)
    t = threading.Thread(target=write)
    t.start()
    return t


def test_live_ignores_existing_lines_and_catches_new_gap(tmp_path):
    log = tmp_path / 'app.log'
    log.write_text('2025-01-01 00:00:00 old\n2025-01-01 01:00:00 old gap\n')
    events = []
    writer = append_later(log, ['2025-01-01 02:00:00 new\n', '2025-01-01 02:10:00 new gap\n'])
    stats = follow(str(log), duration=1.0, poll_interval=0.05, on_event=events.append)
    writer.join()
    assert stats.total_lines == 2
    assert [g.duration for g in stats.gaps] == [600]
    assert events == stats.gaps


def test_hybrid_links_old_and_new_lines(tmp_path):
    log = tmp_path / 'app.log'
    log.write_text('2025-01-01 00:00:00 old\n')
    writer = append_later(log, ['2025-01-01 00:20:00 new\n'])
    stats = follow(str(log), duration=1.0, from_start=True, poll_interval=0.05)
    writer.join()
    assert [g.duration for g in stats.gaps] == [1200]


def test_live_joins_partially_written_lines(tmp_path):
    log = tmp_path / 'app.log'
    log.write_text('')
    writer = append_later(log, ['2025-01-01 00:00:00 a\n2025-01-01 00:', '10:00 b\n'], step=0.2)
    stats = follow(str(log), duration=1.2, poll_interval=0.05)
    writer.join()
    assert stats.unparsed_lines == 0
    assert [g.duration for g in stats.gaps] == [600]


def test_live_survives_truncation(tmp_path):
    log = tmp_path / 'app.log'
    log.write_text('2025-01-01 00:00:00 a\n' * 50)

    def rotate():
        time.sleep(0.2)
        log.write_text('')
        time.sleep(0.1)
        with open(log, 'a') as f:
            f.write('2025-01-01 00:00:00 x\n2025-01-01 00:30:00 y\n')
    t = threading.Thread(target=rotate)
    t.start()
    stats = follow(str(log), duration=1.0, poll_interval=0.05)
    t.join()
    assert [g.duration for g in stats.gaps] == [1800]


def test_live_missing_file_reports_error():
    stats = follow('nope.log', duration=0.1)
    assert not stats.success and stats.gaps == []
