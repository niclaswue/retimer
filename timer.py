#!/usr/local/bin/python3
import argparse
import tempfile
import subprocess

parser = argparse.ArgumentParser(description="Set timer")
parser.add_argument("commands", metavar="N", type=str, nargs="+", help="end dates for timer or intervals")
parser.add_argument("--name", type=str, help="Event name")

args = parser.parse_args()
commands = args.commands


def set_reminder(minutes, set_time=False, name="Timer"):
    name = name or "Timer"
    print(f"Setting {name} for time {minutes} specific time is {set_time}")

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


for cmd in commands:
    if cmd[0] == "@":
        # specific time like @17:20
        hours, minutes = cmd.replace("@", "").split(":")
        hours = int(hours)
        minutes = int(minutes)
        set_reminder(hours * 60 + minutes, set_time=True, name=args.name)
    elif "x" in cmd:
        # periodic event 5x20m
        amount, rest = cmd.split("x")
        amount = int(amount)
        if "+" in rest:
            # periodic event with break like 5x20m+5m
            interval, break_time = rest.split("+")
            period = int(eval(interval.replace("h", "*60").replace("m", "").replace("d", "*60*24")))
            break_time = int(eval(break_time.replace("h", "*60").replace("m", "").replace("d", "*60*24")))
            for i in range(1, amount + 1):
                set_reminder((i * period + (i - 1) * break_time), set_time=False, name=f"{args.name} - Begin Pause {i}")
                set_reminder((i * period + i * break_time), set_time=False, name=f"{args.name} - End Pause {i}")
        else:
            period = int(eval(rest.replace("h", "*60").replace("m", "").replace("d", "*60*24")))
            for i in range(1, amount + 1):
                set_reminder(i * period, set_time=False, name=f"{args.name} - {i}")

    elif cmd[-1] in ["h", "m", "d"]:
        # time delta like 5h or 10m or 2d
        minutes = int(eval(cmd.replace("h", "*60").replace("m", "").replace("d", "*60*24")))
        set_reminder(minutes, set_time=False, name=args.name)
    else:
        raise NotImplementedError(str(args.commands))
