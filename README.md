# Python Pomodoro Timer

A terminal [Pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer.
Work in focused sessions separated by short breaks, with a longer break after
every few sessions. Uses only the Python standard library.

## Features

- Configurable work, short-break and long-break lengths
- Configurable number of work sessions and long-break interval
- Live countdown in the terminal
- Terminal bell at the end of each phase
- Ctrl+C stops the timer cleanly and shows a summary

## Usage

```bash
# Classic Pomodoro: 4 x 25 min work, 5 min short breaks
python3 pomodoro.py

# 50/10 sessions, 3 of them
python3 pomodoro.py --work 50 --short-break 10 --sessions 3

# 6 sessions with a 20 min long break after every 2nd session
python3 pomodoro.py -n 6 --long-every 2 --long-break 20
```

```
Pomodoro: 4 session(s), total time 115:00. Ctrl+C to stop.

[1/4] Work  24:59
```

| Option | Default | Meaning |
|---|---|---|
| `-w`, `--work` | 25 | work session length (minutes) |
| `-s`, `--short-break` | 5 | short break length (minutes) |
| `-l`, `--long-break` | 15 | long break length (minutes) |
| `-n`, `--sessions` | 4 | number of work sessions |
| `--long-every` | 4 | long break after this many sessions |

Durations accept decimals, e.g. `--work 0.5` for a 30-second session.

## Tests

The timer takes an injectable `sleep` function, so the tests run instantly:

```bash
python3 -m unittest test_pomodoro.py
```
