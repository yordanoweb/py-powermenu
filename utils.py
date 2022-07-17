import os


def id(n):
    return n


def default(expected, d):
    return lambda m: d if m == expected else m


def first(s):
    return str(s)[0]


def inc(n):
    return n + 1


def add(n):
    return lambda m: n + m


def powTwo(x):
    return x * 2


def map(fn):
    return lambda m: m.map(fn)


def compose(*funcs):
    _funcs = list(funcs).__reversed__()

    def _compose(*x):
        result = x[0] if len(x) > 0 else None
        for f in _funcs:
            result = f(result)
        return result

    return _compose


def either(left, right, m):
    return left(m.value) if isinstance(m, Left) else right(m.value)


def upper(s):
    return str(s).upper()


def concat(s):
    return lambda d: str(s) + str(d)


def replace(src_str):
    return lambda part: lambda replacement: str(src_str).replace(part, replacement)


def join(m):
    return m.join()


def log(x):
    print(x)
    return x


def unsafePerformIO(io):
    return io.unsafePerformIO()


def join(m):
    return m.join()


def yesNoTupleToEither(t):
    return Right(t[1]) \
        if t[0] == True or str(t[0]).upper() == 'Y' \
        else Left(False)


"""
Executes a command in the operating system and returns its output.

string -> string
"""
def unsafeCmdExec(cmd):
    proc = os.popen(cmd)
    res = proc.read().strip()
    return res


class Either:
    def __init__(self, x):
        self.value = x

    @staticmethod
    def of(x):
        return Right(x)


class Left(Either):
    def isLeft():
        return True

    def isRight():
        return False

    @staticmethod
    def of(x):
        raise Exception("`of` called on class Left (value) instead of Either (type)")

    def inspect(self):
        return f"Left({self.value})"

    def map(self):
        return self

    def ap(self):
        return self

    def chain(self):
        return self

    def join(self):
        return self

    def sequence(self, of):
        return of(self)

    def traverse(self, of, fn):
        return of(self)


class Right(Either):
    def isLeft():
        return False

    def isRight():
        return True

    @staticmethod
    def of(x):
        raise Exception("`of` called on class Right (value) instead of Either (type)")

    def inspect(self):
        return "Right({self.value})"

    def map(self, fn):
        return Either.of(fn(self.value))

    def ap(self, f):
        return f.map(self.value)

    def chain(self, fn):
        return fn(self.value)

    def join(self):
        return self.value

    def sequence(self, of):
        return self.traverse(of, id)

    def traverse(self, of, fn):
        fn(self.value).map(Either.of)


class Maybe:
    def __init__(self, value) -> None:
        self.value = value

    def isNothing(self):
        return self.value == None or self.value == False

    def isJust(self):
        return not self.isNothing

    def __init__(self, x):
        self.value = x

    def inspect(self):
        return "Nothing" if self.isNothing() else f"Just({self.value})"

    @staticmethod
    def of(x):
        return Maybe(x)

    def map(self, fn):
        return self if self.isNothing() else Maybe.of(fn(self.value))

    def ap(self, f):
        return self if self.isNothing() else f.map(self.value)

    def chain(self, fn):
        return self.map(fn).join()

    def join(self):
        return self if self.isNothing() else self.value

    def sequence(self, of):
        return self.traverse(of, id)

    def traverse(self, of, fn):
        return of(self) if self.isNothing() else fn(self.value).map(Maybe.of)


class IO:
    def __init__(self, fn):
        self.unsafePerformIO = fn

    def inspect(self):
        return f"IO({self.unsafePerformIO()})"

    @staticmethod
    def of(x):
        return IO(lambda *args: x)

    def map(self, fn):
        return IO(compose(fn, self.unsafePerformIO))

    def ap(self, some_container):
        return self.chain(lambda fn: some_container.map(fn))

    def chain(self, fn):
        return self.map(fn).join()

    def join(self):
        return IO(lambda *args: self.unsafePerformIO().unsafePerformIO())


class Identity:
    def __init__(self, x):
        self.value = x

    def inspect(self):
        return f"Identity({self.value})"

    @staticmethod
    def of(x):
        return Identity(x)

    def map(self, fn):
        return Identity.of(fn(self.value))

    def ap(self, f):
        return f.map(self.value)

    def chain(self, fn):
        return self.map(fn).join()

    def join(self):
        return self.value

    def sequence(self, of):
        return self.traverse(of, id)

    def traverse(self, of, fn):
        return fn(self.value).map(Identity.of)
