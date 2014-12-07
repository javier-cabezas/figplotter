def range_generator(start, stop):
    assert start < stop, "Wrong values for range generator"
    distance = float(stop - start)
    return lambda x: (start + (distance/(x - 1)) * i if x > 1 else start for i in range(x))

class Parameter(object):
    def __init__(self, values):
        self.values = values

def param(l):
    if isinstance(l, list):
        # Generator from list
        return lambda x: (m for m in l)
    else:
        # Constant generator
        return lambda x: (l for _ in range(x))

def string_generator(pattern, values):
    return lambda x: (pattern % value for value in values(x))

