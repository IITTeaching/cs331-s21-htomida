import unittest
import sys
from contextlib import contextmanager
from io import StringIO

#################################################################################
# TESTING OUTPUTS
#################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

#################################################################################
# EXERCISE 1
#################################################################################

# implement this function
def is_perfect(n):
    divs = [x for x in range(1, n) if n % x == 0]
    if(sum(divs) == n):
        return True
    else:
        return False

# (3 points)
def test1():
    tc = unittest.TestCase()
    for n in (6, 28, 496):
        tc.assertTrue(is_perfect(n), '{} should be perfect'.format(n))
    for n in (1, 2, 3, 4, 5, 10, 20):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))
    for n in range(30, 450):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))

#################################################################################
# EXERCISE 2
#################################################################################

# implement this function
def multiples_of_3_and_5(n):
    multi = [x for x in range(1, n) if (x % 3 == 0 or x % 5 == 0)]
    return sum(multi)

# (3 points)
def test2():
    tc = unittest.TestCase()
    tc.assertEqual(multiples_of_3_and_5(10), 23)
    tc.assertEqual(multiples_of_3_and_5(500), 57918)
    tc.assertEqual(multiples_of_3_and_5(1000), 233168)

#################################################################################
# EXERCISE 3
#################################################################################
def integer_right_triangles(p):
    tri_count = 0
    hypo = int(p / 3)
    oppo = hypo
    adjc = hypo
    rem =  p % 3
    if(rem > 0):
        if(rem == 1):
            oppo += 1
        else:
            oppo += 1
            adjc += 1
    for i in range(oppo):
        for j in range(oppo-i):
            if((oppo-i-j)**2 + (adjc+j)**2 == (hypo+i)**2):
                 tri_count += 1
    return tri_count


def test3():
    tc = unittest.TestCase()
    tc.assertEqual(integer_right_triangles(60), 2)
    tc.assertEqual(integer_right_triangles(100), 0)
    tc.assertEqual(integer_right_triangles(180), 3)

#################################################################################
# EXERCISE 4
#################################################################################

# implement this function
def gen_pattern(chars):
    pattern = ''
    char_len = len(chars)
    pat_len = (len(chars)*2)-1
    for l in range(pat_len):
        if(l <= char_len-1):
            line = chars[:-(l+2):-1]
            if len(line) > 1:
                line += line[-2::-1]
        else:
            line = chars[:-char_len+l:-1]
            if len(line) > 1:
                line += line[-2::-1]
        line = '.'.join(line)
        line = line.center(pat_len*2-1, '.')
        pattern += line
        pattern += '\n'
        
    print(pattern)

def test4():
    tc = unittest.TestCase()
    with captured_output() as (out,err):
        gen_pattern('@')
        tc.assertEqual(out.getvalue().strip(), '@')
    with captured_output() as (out,err):
        gen_pattern('@%')
        tc.assertEqual(out.getvalue().strip(),
        """
..%..
%.@.%
..%..
""".strip())
    with captured_output() as (out,err):
        gen_pattern('ABC')
        tc.assertEqual(out.getvalue().strip(),
        """
....C....
..C.B.C..
C.B.A.B.C
..C.B.C..
....C....
""".strip())
    with captured_output() as (out,err):
        gen_pattern('#####')
        tc.assertEqual(out.getvalue().strip(),
                             """
........#........
......#.#.#......
....#.#.#.#.#....
..#.#.#.#.#.#.#..
#.#.#.#.#.#.#.#.#
..#.#.#.#.#.#.#..
....#.#.#.#.#....
......#.#.#......
........#........
""".strip())
    with captured_output() as (out,err):
        gen_pattern('abcdefghijklmnop')
        tc.assertEqual(out.getvalue().strip(),
"""
..............................p..............................
............................p.o.p............................
..........................p.o.n.o.p..........................
........................p.o.n.m.n.o.p........................
......................p.o.n.m.l.m.n.o.p......................
....................p.o.n.m.l.k.l.m.n.o.p....................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
....................p.o.n.m.l.k.l.m.n.o.p....................
......................p.o.n.m.l.m.n.o.p......................
........................p.o.n.m.n.o.p........................
..........................p.o.n.o.p..........................
............................p.o.p............................
..............................p..............................
""".strip()
)

#################################################################################
# RUN ALL TESTS
#################################################################################
def main():
    test1()
    test2()
    test3()
    test4()

if __name__ == '__main__':
    main()
