# i3-switch

[![PyPI](https://img.shields.io/pypi/v/i3-switch)](https://pypi.org/project/i3-switch/)

i3 script to switch between windows in history.

This script is inspired by [i3-swap-focus](https://github.com/olivierlemoal/i3-swap-focus).

It provides a configurable history length and supports consecutive switching within the history.
Besides, it can skip the closed windows, windows in scratchpad, or windows not in the current workspace.

## Installation

```
pip install i3-switch
```

## Configuration

Add the following lines to your i3 config file:

```
# Start i3-switch process
exec i3-switch

bindsym $mod+Tab exec pkill -USR1 -F "/tmp/i3-switch.pid"
# Switch in the same workspaces
# bindsym $mod+Tab exec pkill -USR2 -F "/tmp/i3-switch.pid"
```

To change the options for i3-switch in your i3 config:

```
exec i3-switch --max-len 1000 --timeout 400
```

## Consecutive Switching

When switching before it times out,
the history within the consecutive switch won't be recorded.

For example, at first the records are `DCBA`,
after switch twice consecutively,
it should become `BDCA`.

Internally, the process is as follows:
`DCBA` -> `CDCBA` -> `BCDCBA` -> `BDCA` (cleanup after timeout).
This process is necessary because the signal itself is stateless,
so the state is kept in the history.


## Options

| Name        | Description               | Default |
| ----------- | ------------------------- | ------- |
| `--max-len` | Max length of the window deque | `100`     |
| `--timeout` | Timeout for consecutive switching in milliseconds | `500` |
