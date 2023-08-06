from functools import reduce


def blank(s):
    return isinstance(s, str) and not s.strip()


def get_in(seq, keys):
    return reduce(lambda mem, k: mem[k], keys, seq) or None


v = {'a': [{'b': 2}]}

print(get_in(v, ('a', 0, 'b')))
