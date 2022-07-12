import os
import sys

from utils import (
    IO,
    unsafePerformIO,
    replace,
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


def unsafe_cmd_exec(cmd):
    def _unsafe_op():
        proc = os.popen(cmd)
        res = proc.read().strip()
        return res

    return _unsafe_op


def possible_actions(action):
    actions = {
        "": lambda: "systemctl poweroff",
        "": lambda: "systemctl reboot",
        "": lambda: 'rofi -e "Lock not implemented yet"',
        "": lambda: 'rofi -e "Sleep not implemented yet"',
        "": lambda: "bspc quit",
    }
    return actions[action] if action in actions else lambda: False


assert callable(unsafe_cmd_exec(uptime_command)), "Not a function"

# ready to call "unsafePerformIO()" and will return sys uptime
# IO string
ioUptime = IO(unsafe_cmd_exec(uptime_command))

# IO -> string
power_menu_fn = compose(
    unsafe_cmd_exec,
    replace(power_dialog_cmd)('$uptime'),
    unsafePerformIO
)

assert callable(power_menu_fn), "Not a function"

