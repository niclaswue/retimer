#!/usr/local/bin/python3
import argparse
import tempfile
import subprocess

parser = argparse.ArgumentParser(description="Set timer")
parser.add_argument(
    "commands",
    metavar="N",
    type=str,
    nargs="+",
    help="end dates for timer or intervals",
)
parser.add_argument("--name", type=str, help="event name")

args = parser.parse_args()
commands = args.commands


def parse_interval_string(time_interval: str) -> int:
    """Return minutes from interval string

    Args:
        time_interval (str): time interval string

    Returns:
        int: minutes in interval
    """
    # append stop char
    time_interval = f"{time_interval}!"
    interval_minutes = 0
    if "d" in time_interval:
        days, time_interval = time_interval.split("d")
        interval_minutes += int(days) * 60 * 24
    if "h" in time_interval:
        hours, time_interval = time_interval.split("h")
        interval_minutes += int(hours) * 60
    if "m" in time_interval:
        minutes, time_interval = time_interval.split("m")
        interval_minutes += int(minutes)
    assert time_interval == "!"
    return interval_minutes


def set_reminder(minutes: int, set_time: bool = False, name: str = "Timer"):
    name = name or "Timer"

    script = """
    tell application "Reminders"

    # Calculate date time for midnight today
    set currentDay to (current date) - (time of (current date))

    """

    if set_time:
        script += f"set theDate to currentDay + ({minutes} * minutes)"
    else:
        script += f"set theDate to currentDay + (time of (current date)) + ({minutes} * minutes)"

    script += f"""
    # Select the relevant list in Reminders.app
    set myList to list "Timer"

    tell myList
        # Create the reminder
        set newReminder to make new reminder
        set name of newReminder to "{name}"
        set remind me date of newReminder to theDate
    end tell
    end tell
    """

    with tempfile.NamedTemporaryFile(suffix="applescript") as temp:
        temp.write(bytes(script, encoding="utf-8"))
        temp.flush()
        subprocess.call(["osascript", temp.name])

    print(f"✅ Set Timer '{name}' for {minutes} minutes. Specific time is {set_time}")


if __name__ == "__main__":
    for cmd in commands:
        if cmd[0] == "@":
            # specific time today like @17:20
            hours, minutes = [int(v) for v in cmd.replace("@", "").split(":")]
            set_reminder(hours * 60 + minutes, set_time=True, name=args.name)
        elif "x" in cmd:
            # periodic event 5x20m
            amount, rest = cmd.split("x")
            amount = int(amount)
            if "+" in rest:
                # periodic event with break like 5x20m+5m
                interval, break_time = rest.split("+")
                period = parse_interval_string(interval)
                break_time = parse_interval_string(break_time)
                for i in range(1, amount + 1):
                    set_reminder(
                        (i * period + (i - 1) * break_time),
                        set_time=False,
                        name=f"{args.name} - Begin Break {i}",
                    )
                    set_reminder(
                        (i * period + i * break_time),
                        set_time=False,
                        name=f"{args.name} - End Break {i}",
                    )
            else:
                period = parse_interval_string(rest)
                for i in range(1, amount + 1):
                    set_reminder(i * period, set_time=False, name=f"{args.name} - {i}")

        elif cmd[-1] in ["h", "m", "d"]:
            # time delta like 5h or 10m or 2d
            set_reminder(parse_interval_string(cmd), set_time=False, name=args.name)
        else:
            raise NotImplementedError(str(args.commands))
