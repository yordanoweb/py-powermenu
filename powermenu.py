import os
import sys

from utils import IO, compose, inc, add, R, \
                  upper, concat, id, Maybe, replace, \
                  first, default

DIR = os.path.dirname(os.path.abspath(__file__))

power_menu_rofi_command=f"rofi -theme {DIR}/powermenu.rasi"

uptime_command="uptime -p | sed -e 's/up //g'"

# Options
shutdown=""
reboot=""
lock=""
suspend=""
logout=""

# Variable passed to rofi
power_options=f"{shutdown}\n{reboot}\n{lock}\n{suspend}\n{logout}"
_msg="Options  -  yes / y / no / n"

power_options_question_cmd=f'echo "{power_options}" | {power_menu_rofi_command} -p "UP - $uptime" -dmenu -selected-row 2'
yes_no_question_cmd=f"{DIR}/confirm"

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
    "": lambda: "rofi -e \"Lock not implemented yet\"",
    "": lambda: "rofi -e \"Sleep not implemented yet\"",
    "": lambda: "bspc quit",
  }
  return actions[action] if action in actions else lambda: False

ioUptime = IO(unsafe_cmd_exec(uptime_command))
ioYesNo = IO(unsafe_cmd_exec(yes_no_question_cmd))

power_options_fn = IO.of(replace(power_options_question_cmd)) \
  .ap(IO.of("$uptime")) \
  .ap(ioUptime) \
  .map(unsafe_cmd_exec) \
  .unsafePerformIO()

ioPowerOptions = IO(power_options_fn)

power_command_to_execute = ioPowerOptions \
  .map(possible_actions) \
  .map(IO) \
  .join() \
  .unsafePerformIO()

if not power_command_to_execute:
    exit()

yes_no_answer = ioYesNo \
  .map(upper) \
  .map(default(expected='', d='N')) \
  .map(first) \
  .unsafePerformIO()

if yes_no_answer == 'Y':
  IO(unsafe_cmd_exec(power_command_to_execute)) \
    .unsafePerformIO()

