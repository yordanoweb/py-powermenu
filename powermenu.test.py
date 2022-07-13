import os
import sys

from utils import (
    compose
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


def replace(src, pattern):
    return lambda replacement: str(src).replace(pattern, replacement)


def unsafeCmdExec(cmd):
    proc = os.popen(cmd)
    res = proc.read().strip()
    return res


def operatingSystemCommand(action):
    actions = {
        "": "systemctl poweroff",
        "": "systemctl reboot",
        "": 'rofi -e "Lock not implemented yet"',
        "": 'rofi -e "Sleep not implemented yet"',
        "": "bspc quit",
    }
    return actions[action] if action in actions else "exit"


unsafeUptime = lambda _: unsafeCmdExec(uptime_command)
unsafePowerDialog = lambda cmd: unsafeCmdExec(cmd)

powerMenuDialog = compose(
    unsafePowerDialog,
    replace(src=power_dialog_cmd, pattern='$uptime'),
    unsafeUptime
)

execPowerAction = compose(
    unsafeCmdExec,
    operatingSystemCommand,
    powerMenuDialog
)

execPowerAction(True)
