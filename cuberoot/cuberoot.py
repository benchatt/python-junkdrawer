import sys

bignum = float(sys.argv[1])
tol = 0.0001
steps = 100

def recurse(top: float, bottom: float):
    print(bottom,top)
    if bottom == 0.0:
        bottom = tol
    gap = top - bottom
    step = gap / float(steps)
    points = [(bottom + (n * step)) for n in range(steps)]
    square_quotient = lambda x: abs((x**2) - (bignum / x))
    offs = [square_quotient(p) for p in points]
    if min(offs) > tol:
        ends = [points[offs.index(min(offs))], None]
        del offs[offs.index(min(offs))]
        ends[1] = points[offs.index(min(offs))]
        return recurse(max(ends), min(ends))
    else:
        return points[offs.index(min(offs))]

find_top = lambda n: n / 2.0 if n > 1 else n * 2.0
print(recurse(find_top(bignum), 0))
