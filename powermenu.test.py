import os
import sys

from utils import (
    IO,
    unsafePerformIO,
    Identity,
)

DIR = os.path.dirname(os.path.abspath(__file__))

uptime_command = "uptime -p | sed -e 's/up //g'"

# Options
shutdown = ""
reboot = ""
lock = ""
suspend = ""
logout = ""

# Variable passed to rofi
power_options = f"{shutdown}\n{reboot}\n{lock}\n{suspend}\n{logout}"
_msg = "Options  -  yes / y / no / n"

power_menu_rofi_command = f"rofi -theme {DIR}/powermenu.rasi"
power_dialog_cmd = f'echo "{power_options}" | {power_menu_rofi_command} -p "UP - $uptime" -dmenu -selected-row 2'

yes_no_question_cmd = f"{DIR}/confirm"


def compose(f, g, h):
    return lambda x: f(g(h(x)))


def replace(src, pattern):
    return lambda replacement: str(src).replace(pattern, replacement)


def unsafe_cmd_exec(cmd):
    proc = os.popen(cmd)
    res = proc.read().strip()
    return res


def possible_actions(action):
    actions = {
        "": lambda: "systemctl poweroff",
        "": lambda: "systemctl reboot",
        "": lambda: 'rofi -e "Lock not implemented yet"',
        "": lambda: 'rofi -e "Sleep not implemented yet"',
        "": lambda: "bspc quit",
    }
    return actions[action] if action in actions else lambda: "exit"


unsafe_uptime = lambda: unsafe_cmd_exec(uptime_command)

# receives a fn that returns side effect (command execution result)
rofi_power_options_dialog_fn = compose(
    replace(src=power_dialog_cmd, pattern='$uptime'),
    unsafePerformIO,
    IO
)

selected_power_action = compose(
    possible_actions,
    unsafe_cmd_exec,
    rofi_power_options_dialog_fn
)

