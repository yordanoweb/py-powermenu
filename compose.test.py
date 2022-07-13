def compose(*funcs):
    _funcs = list(funcs)
    _funcs.reverse()
    def _compose(x):
        result = x
        for f in _funcs:
            result = f(result)
        return result
    return _compose


def log(x):
    print(x)
    return x


compose(
    lambda n: n + 1,
    log,
    lambda n: n * 2,
    log
)(9)
