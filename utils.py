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


def compose(f):
    return lambda g: lambda x: f(g(x))


def upper(s):
    return str(s).upper()


def concat(s):
    return lambda d: str(s) + str(d)


def replace(src_str):
    return lambda part: lambda replacement: str(src_str).replace(part, replacement)


def join(m):
    return m.join()


class R:
    @staticmethod
    def compose(f, g):
        return lambda: f(g())


class Maybe:
    def is_nothing(self):
        return self.value == None or self.value == False

    def is_just(self):
        return not self.is_nothing

    def __init__(self, x):
        self.value = x

    def inspect(self):
        return "Nothing" if self.is_nothing else f"Just({self.value})"

    @classmethod
    def of(x):
        return Maybe(x)

    def map(self, fn):
        return self if self.is_nothing else Maybe.of(fn(self.value))

    def ap(self, f):
        return self if self.is_nothing else f.map(self.value)

    def chain(self, fn):
        return self.map(fn).join()

    def join(self):
        return self if self.is_nothing else self.value

    def sequence(self, of):
        return self.traverse(of, id)

    def traverse(self, of, fn):
        return of(self) if self.is_nothing else fn(self.value).map(Maybe.of)


class IO:
    def __init__(self, fn):
        self.unsafePerformIO = fn

    def inspect(self):
        return "IO(?)"

    @staticmethod
    def of(x):
        return IO(lambda: x)

    def map(self, fn):
        return IO(R.compose(fn, self.unsafePerformIO))

    def ap(self, some_container):
        return self.chain(lambda fn: some_container.map(fn))

    def chain(self, fn):
        return self.map(fn).join()

    def join(self):
        return IO(lambda: self.unsafePerformIO().unsafePerformIO())


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
