import unittest

from pomodoro import LONG_BREAK, SHORT_BREAK, WORK, Phase, build_schedule, countdown, format_time, run


class ScheduleTest(unittest.TestCase):

    def test_default_schedule(self):
        names = [phase.name for phase in build_schedule()]
        self.assertEqual(names, [WORK, SHORT_BREAK, WORK, SHORT_BREAK, WORK, SHORT_BREAK, WORK])

    def test_long_break_after_every_n_sessions(self):
        names = [phase.name for phase in build_schedule(sessions=5, long_every=2)]
        self.assertEqual(names, [WORK, SHORT_BREAK, WORK, LONG_BREAK, WORK, SHORT_BREAK,
                                 WORK, LONG_BREAK, WORK])

    def test_single_session_has_no_break(self):
        self.assertEqual(build_schedule(sessions=1), [Phase(WORK, 25)])

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            build_schedule(sessions=0)
        with self.assertRaises(ValueError):
            build_schedule(work=0)


class FormatTimeTest(unittest.TestCase):

    def test_formats_minutes_and_seconds(self):
        self.assertEqual(format_time(65), "01:05")
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(-3), "00:00")


class CountdownTest(unittest.TestCase):

    def test_sleeps_once_per_second_and_rings_bell(self):
        sleeps, output = [], []
        countdown(Phase(WORK, 0.05), "Work", sleep=sleeps.append, write=output.append)
        self.assertEqual(sleeps, [1, 1, 1])
        self.assertIn("\a", output[-1])
        self.assertIn("00:03", output[0])

    def test_run_counts_completed_sessions(self):
        sleeps = []
        schedule = build_schedule(sessions=3, work=1 / 60, short_break=1 / 60)
        completed = run(schedule, sleep=sleeps.append, write=lambda s: None)
        self.assertEqual(completed, 3)
        self.assertEqual(len(sleeps), 5)  # 3 work + 2 breaks, one second each


if __name__ == "__main__":
    unittest.main()
