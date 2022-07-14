import os
import sys

from utils import Left, Right, compose, either

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
power_dialog_cmd = f'echo "{power_options}" | {power_menu_rofi_command} -p "UP - $UPTIME" -dmenu -selected-row 2'

yes_no_question_cmd = f"{DIR}/confirm"


"""
Replaces the string "pattern" inside of the original "src" string
parameter. Returns a new function waiting for the "replacement"
string.

(string, string) -> f string -> string
"""
def replace(src, pattern):
    return lambda replacement: str(src).replace(pattern, replacement)


"""
Executes a command in the operating system and returns its output.

string -> string
"""
def unsafeCmdExec(cmd):
    proc = os.popen(cmd)
    res = proc.read().strip()
    return res


"""
Returns the right action to take according to the "action" parameter.
Takes care of the response.

string -> Either string
"""
def operatingSystemCommand(action):
    actions = {
        "": "systemctl poweroff",
        "": "systemctl reboot",
        "": 'rofi -e "Lock not implemented yet"',
        "": 'rofi -e "Sleep not implemented yet"',
        "": "bspc quit",
    }
    return Right(actions[action]) if action in actions else Left("Unknown action")


unsafeUptime = lambda _: unsafeCmdExec(uptime_command)
unsafePowerDialog = lambda cmd: unsafeCmdExec(cmd)

"""
Shows the question "Are you sure (y/n)?" and takes care of
the answer for further decisions.
"""
def unsafeYesNoQuestion(_):
    res = unsafeCmdExec(yes_no_question_cmd)
    return (
        Right(_)
        if len(str(res)) > 0 and str(res).upper()[0] == "Y"
        else Left("Do nothing")
    )

"""
Execute the command that returns system uptime. Then, use the returned
system uptime string, for composing the long string required as parameters
for rofi being able to draw a power menu dialog.
"""
powerMenuDialog = compose(
    unsafePowerDialog, replace(power_dialog_cmd, "$UPTIME"), unsafeUptime
)

"""
Returns the matching action among all the possible power actions in
the rofi dialog shown by "powerMenuDialog" 
"""
getPowerActionCommand = compose(operatingSystemCommand, powerMenuDialog)

"""
The selected power action is only executed if the answer is "Y".
Otherwise, the execution stops.

(f, f, Monad a) -> Either b
"""
powerActionDecision = either(sys.exit, unsafeYesNoQuestion, getPowerActionCommand(True))

either(sys.exit, unsafeCmdExec, powerActionDecision)
