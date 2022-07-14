import os
import sys

from utils import (
    Left,
    Right,
    compose,
    either
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
    return Right(actions[action]) \
        if action in actions else Left("Unknown action")


unsafeUptime = lambda _: unsafeCmdExec(uptime_command)
unsafePowerDialog = lambda cmd: unsafeCmdExec(cmd)

# returns the result of the selected power action plus the yes/no answer
def unsafeYesNoQuestion(_):
    res = unsafeCmdExec(yes_no_question_cmd)
    return Right(_) if len(str(res)) > 0 and str(res).upper()[0] == 'Y' \
                    else Left('Do nothing')

powerMenuDialog = compose(
    unsafePowerDialog,
    replace(src=power_dialog_cmd, pattern='$uptime'),
    unsafeUptime
)

getPowerActionCommand = compose(
    operatingSystemCommand,
    powerMenuDialog
)

either(
    sys.exit,
    unsafeCmdExec,
    either(
        sys.exit,
        unsafeYesNoQuestion,
        getPowerActionCommand(True)
    )
)
