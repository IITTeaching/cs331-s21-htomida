from unittest import TestCase
import random
import functools

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################
class Heap:
    def __init__(self, key=lambda x:x):
        self.data = []
        self.key  = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2

    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2

    def pos_exists(self, n):
        return n < len(self)

    def switch_node(self, parent, child):
        parentval = self.data[parent]
        childval = self.data[child]
        self.data[parent] = childval
        self.data[child] = parentval

    def trickle_down(self, n):
        lc = Heap._left(n)
        rc = Heap._right(n)
        curval = self.key(self.data[n])
        if self.pos_exists(lc):
            if self.pos_exists(rc):
                lcval = self.key(self.data[lc])
                rcval = self.key(self.data[rc])
                if lcval > curval or rcval > curval:
                    if lcval > rcval:
                        self.switch_node(n, lc)
                        self.trickle_down(lc)
                    else:
                        self.switch_node(n, rc)
                        self.trickle_down(rc)
            else:
                lcval = self.key(self.data[lc])
                if lcval > curval:
                    self.switch_node(n, lc)
                    self.trickle_down(lc)
        elif self.pos_exists(rc):
            rcval = self.key(self.data[rc])
            if rcval > curval:
                self.switch_node(n, rc)
                self.trickle_down(rc)

    def trickle_up(self, n):
        if n > 0:
            p = Heap._parent(n)
            pval = self.key(self.data[p])
            curval = self.key(self.data[n])
            if pval < curval:
                self.switch_node(p,n)
                self.trickle_up(p)
 
    def heapify(self, idx=0):
        ### BEGIN SOLUTION
        p = Heap._parent(idx)
        if len(self.data) == 0:
            return
        pval = self.key(self.data[p])
        curval = self.key(self.data[idx])
        lc = Heap._left(idx)
        rc = Heap._right(idx)
        if self.pos_exists(lc):
            lcval = self.key(self.data[lc])
            if curval < lcval:
                self.trickle_down(idx)
        if self.pos_exists(rc):
            rcval = self.key(self.data[rc])
            if curval < rcval:
                self.trickle_down(idx)
        if curval > pval :
            self.trickle_up(idx)
        ### END SOLUTION

    def add(self, x):
        ### BEGIN SOLUTION
        self.data.append(x)
        self.heapify(len(self.data)-1)
        ### END SOLUTION

    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self.heapify()
        return ret

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################

# (6 point)
def test_key_heap_1():
    from unittest import TestCase
    import random

    tc = TestCase()
    h = Heap()

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])

# (6 point)
def test_key_heap_2():
    tc = TestCase()
    h = Heap(lambda x:-x)

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])

# (6 points)
def test_key_heap_3():
    tc = TestCase()
    h = Heap(lambda s:len(s))

    h.add('hello')
    h.add('hi')
    h.add('abracadabra')
    h.add('supercalifragilisticexpialidocious')
    h.add('0')

    tc.assertEqual(h.data,
                   ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])

# (6 points)
def test_key_heap_4():
    tc = TestCase()
    h = Heap()

    random.seed(0)
    lst = list(range(-1000, 1000))
    random.shuffle(lst)

    for x in lst:
        h.add(x)
    for x in range(999, -1000, -1):
        tc.assertEqual(x, h.pop())

# (6 points)
def test_key_heap_5():
    tc = TestCase()
    h = Heap(key=lambda x:abs(x))

    random.seed(0)
    lst = list(range(-1000, 1000, 3))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x:abs(x))):
        tc.assertEqual(x, h.pop())

################################################################################
# 2. MEDIAN
################################################################################
def running_medians(iterable):
    ### BEGIN SOLUTION
    min_heap = Heap(key=lambda x:-x)
    max_heap = Heap()
    medians = []
    for i, x in enumerate(iterable):
        if i == 0:
            medians.append(x)
            max_heap.add(x)
        elif medians[-1] < x:
            min_heap.add(x)
            if len(min_heap) - len(max_heap) == 0:
                medians.append((min_heap.peek() + max_heap.peek()) / 2)
                if medians[-1] > min_heap.peek():
                    max_heap.add(min_heap.pop())
            elif len(min_heap) - len(max_heap) == 1:
                medians.append(min_heap.peek())
                max_heap.add(min_heap.pop())
        elif medians[-1] >= x:
            max_heap.add(x)
            if len(max_heap) - len(min_heap) == 0:
                medians.append((min_heap.peek() + max_heap.peek()) / 2)
                if medians[-1] < max_heap.peek():
                    min_heap.add(max_heap.pop())
            elif len(max_heap) - len(min_heap) == 1:
                medians.append(max_heap.peek())
            elif len(max_heap) - len(min_heap) == 2:
                temp = max_heap.pop()
                medians.append((max_heap.peek() + temp) / 2)
                min_heap.add(temp)
    return medians
    ### END SOLUTION

################################################################################
# TESTS
################################################################################
def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i%2 == 0:
            medians.append(values[i//2])
        else:
            medians.append((values[i//2] + values[i//2+1]) / 2)
    return medians

# (13 points)
def test_median_1():
    tc = TestCase()
    tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))

# (13 points)
def test_median_2():
    tc = TestCase()
    vals = [random.randrange(10000) for _ in range(1000)]
    tc.assertEqual(running_medians_naive(vals), running_medians(vals))

# MUST COMPLETE IN UNDER 10 seconds!
# (14 points)
def test_median_3():
    tc = TestCase()
    vals = [random.randrange(100000) for _ in range(100001)]
    m_mid   = sorted(vals[:50001])[50001//2]
    m_final = sorted(vals)[len(vals)//2]
    running = running_medians(vals)
    tc.assertEqual(m_mid, running[50000])
    tc.assertEqual(m_final, running[-1])

################################################################################
# 3. TOP-K
################################################################################
def topk(items, k, keyf):
    ### BEGIN SOLUTION
    min_heap = Heap(key=lambda x:-keyf(x))
    for i in items:
        if len(min_heap) < k:
            min_heap.add(i)
        else:
            if keyf(min_heap.peek()) < keyf(i):
                min_heap.pop()
                min_heap.add(i)
    return min_heap.data[::-1]
    ### END SOLUTION

################################################################################
# TESTS
################################################################################
def get_age(s):
    return s[1]

def naive_topk(l,k,keyf):
    revkey = lambda x: keyf(x) * -1
    return sorted(l, key=revkey)[0:k]

# (30 points)
def test_topk_students():
    tc = TestCase()
    students = [ ('Peter', 33), ('Bob', 23), ('Alice', 21), ('Gertrud', 53) ]

    tc.assertEqual(naive_topk(students, 2, get_age),
                   topk(students, 2, get_age))

    tc.assertEqual(naive_topk(students, 1, get_age),
                   topk(students, 1, get_age))

    tc.assertEqual(naive_topk(students, 3, get_age),
                   topk(students, 3, get_age))

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_key_heap_1,
              test_key_heap_2,
              test_key_heap_3,
              test_key_heap_4,
              test_key_heap_5,
              test_median_1,
              test_median_2,
              test_median_3,
              test_topk_students
              ]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
