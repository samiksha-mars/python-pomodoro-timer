"""A terminal Pomodoro timer."""

import argparse
import sys
import time
from dataclasses import dataclass

WORK, SHORT_BREAK, LONG_BREAK = "Work", "Short break", "Long break"


@dataclass(frozen=True)
class Phase:
    name: str
    minutes: float

    @property
    def seconds(self):
        return int(round(self.minutes * 60))


def build_schedule(sessions=4, work=25, short_break=5, long_break=15, long_every=4):
    """Return the list of phases: work sessions separated by breaks (no trailing break)."""
    if sessions < 1:
        raise ValueError("sessions must be at least 1")
    if min(work, short_break, long_break) <= 0 or long_every < 1:
        raise ValueError("durations must be positive and long_every at least 1")
    schedule = []
    for number in range(1, sessions + 1):
        schedule.append(Phase(WORK, work))
        if number < sessions:
            is_long = number % long_every == 0
            schedule.append(Phase(LONG_BREAK, long_break) if is_long else Phase(SHORT_BREAK, short_break))
    return schedule


def format_time(seconds):
    minutes, secs = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{secs:02d}"


def countdown(phase, label, sleep=time.sleep, write=sys.stdout.write):
    """Count down one phase, redrawing the remaining time once per second."""
    for remaining in range(phase.seconds, 0, -1):
        write(f"\r{label}  {format_time(remaining)} ")
        sys.stdout.flush()
        sleep(1)
    write(f"\r{label}  {format_time(0)} done!\a\n")


class Stopped(Exception):
    """Raised by run() when the timer is interrupted with Ctrl+C."""

    def __init__(self, completed):
        super().__init__(completed)
        self.completed = completed


def run(schedule, sleep=time.sleep, write=sys.stdout.write):
    """Run every phase in order; return the number of completed work sessions.

    On Ctrl+C, raise Stopped carrying the number of sessions completed so far.
    """
    total_work = sum(1 for phase in schedule if phase.name == WORK)
    completed = 0
    for phase in schedule:
        if phase.name == WORK:
            label = f"[{completed + 1}/{total_work}] {WORK}"
        else:
            label = f"      {phase.name}"
        try:
            countdown(phase, label, sleep, write)
        except KeyboardInterrupt:
            raise Stopped(completed) from None
        if phase.name == WORK:
            completed += 1
    return completed


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run a Pomodoro timer in the terminal.")
    parser.add_argument("-w", "--work", type=float, default=25, help="work minutes (default 25)")
    parser.add_argument("-s", "--short-break", type=float, default=5, help="short break minutes (default 5)")
    parser.add_argument("-l", "--long-break", type=float, default=15, help="long break minutes (default 15)")
    parser.add_argument("-n", "--sessions", type=int, default=4, help="number of work sessions (default 4)")
    parser.add_argument("--long-every", type=int, default=4,
                        help="take a long break after this many sessions (default 4)")
    args = parser.parse_args(argv)

    try:
        schedule = build_schedule(args.sessions, args.work, args.short_break,
                                  args.long_break, args.long_every)
    except ValueError as e:
        parser.error(str(e))

    total = sum(phase.seconds for phase in schedule)
    print(f"Pomodoro: {args.sessions} session(s), total time {format_time(total)}. Ctrl+C to stop.\n")
    try:
        completed = run(schedule)
    except Stopped as stopped:
        print(f"\n\nStopped early. You completed {stopped.completed} work session(s).")
        return 130
    print(f"\nAll done! You completed {completed} work session(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
