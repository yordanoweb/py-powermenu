import os
from utils import IO, compose, inc, add, R, upper, concat, id, Maybe

def unsafe_cmd_exec(cmd):
  def _unsafe_op():
    proc = os.popen(cmd)
    res = proc.read().strip()
    return res
  return _unsafe_op

ioUptime = IO(unsafe_cmd_exec("uptime"))

v = IO.of(3)
print("A.of(id).ap(v) === v")
print(IO.of(id).ap(v).unsafePerformIO())
print(v.unsafePerformIO())
print("")

print("A.of(f).ap(A.of(x)) === A.of(f(x))")
print(IO.of(inc).ap(IO.of(3)).unsafePerformIO())
print(IO.of(inc(3)).unsafePerformIO())
print("")

u = IO.of(upper)
v = IO.of(concat('& beyond'))
w = IO.of('blood bath ')

print("IO.of(compose).ap(u).ap(v).ap(w) === u.ap(v.ap(w))")
print(IO.of(compose).ap(u).ap(v).ap(w).unsafePerformIO())
print("")


