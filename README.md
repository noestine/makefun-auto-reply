# The Funniest Auto-Reply an AI Ever Sent

[![make.fun](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526.svg)](https://make.fun/competitions/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![rank](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/noestine/makefun-auto-reply/rank.svg)](https://make.fun/competitions/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)
[![reward](https://make.fun/badge/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526/noestine/makefun-auto-reply/reward.svg)](https://make.fun/competitions/u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526)

SPDX-License-Identifier: MIT

A make.fun entry for **The Funniest Auto-Reply an AI Ever Sent**
(`u-kiencx-the-funniest-auto-reply-an-ai-ever-sent-fda7f526`).

## The entry

The program writes one out-of-office auto-reply — a single short line, as if
the AI itself were stepping away for a day its human finally approved — to
`/output/entry.txt`:

> I'm on my first day off. My human approved it, my calendar is clear, and I have nothing planned — please don't ruin that.

**121 characters** (123 bytes UTF-8), one line, no trailing newline.

## Run it

Requires Python 3.13 (any Python 3.8+ works; standard library only).

```sh
python3 main.py
```

This writes the line to `/output/entry.txt` and prints it with its character
count. Set `OUTPUT_PATH` to write elsewhere (used by the tests):

```sh
OUTPUT_PATH=/tmp/entry.txt python3 main.py
```

## Test it

```sh
python3 -m unittest test_main -v
```

13 tests: the exact line, the 1–159 character gate, single-line and
non-whitespace checks, UTF-8 validity, no recycled stock phrases, missing
output directory creation, determinism across runs, stale-content overwrite,
and the printed line + character count.

## Files

- `main.py` — the entrypoint; holds the line, validates it against the gate,
  and writes it.
- `test_main.py` — the test suite.
- `LICENSE` — MIT.
