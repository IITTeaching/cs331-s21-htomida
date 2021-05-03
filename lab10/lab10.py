from unittest import TestCase
import random

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            ### BEGIN SOLUTION
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left
            ### END SOLUTION

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def rebalance(t):
        ### BEGIN SOLUTION
        def bf(n):
           return AVLTree.Node.height(n.right) - AVLTree.Node.height(n.left)
        if t.left and t.right:
            bf_root = bf(t)
        elif t.left:
            bf_root = 0 - AVLTree.Node.height(t.left)
        elif t.right:
            bf_root = AVLTree.Node.height(t.right) - 0
        else:
            bf_root = 0
        if bf_root == -2:
            if bf(t.left) <= 0:
                t.rotate_right()
            elif bf(t.left) > 0:
                t.left.rotate_left()
                t.rotate_right()
        elif bf_root == 2:
            if bf(t.right) >= 0:
                t.rotate_left()
            elif bf(t.right) < 0:
                t.right.rotate_right()
                t.rotate_left()
        ### END SOLUTION

    def add(self, val):
        assert(val not in self)
        ### BEGIN SOLUTION
        def rec_add(r, val):
            if(r.val > val):
                if(r.left):
                    rec_add(r.left,val)
                    AVLTree.rebalance(r)
                else:
                    r.left = AVLTree.Node(val)
            elif(r.val < val):
                if(r.right):
                    rec_add(r.right,val)
                    AVLTree.rebalance(r)
                else:
                    r.right = AVLTree.Node(val)

        if self.root:
            rec_add(self.root, val)
        else:
            self.root = AVLTree.Node(val)
        self.size += 1
        ### END SOLUTION

    def tmax(self, n):
        if not n.right:
            return n.val
        return self.tmax(n.right)

    def __delitem__(self, val):
        assert(val in self)
        ### BEGIN SOLUTION
        def rec_del(parent,isleft,t,val):
            if t.val > val:
                rec_del(t, True, t.left, val)
                AVLTree.rebalance(t)
            elif t.val < val:
                rec_del(t, False, t.right,val)
                AVLTree.rebalance(t)
            else:
                if t.left and t.right: # node has two children, replace with largest value in the left subtree and then delete that one
                    replaceval = self.tmax(t.left)
                    t.val = replaceval
                    rec_del(t, True, t.left, replaceval)
                    AVLTree.rebalance(t)
                elif t.left: # replace node with its only child (the left one)
                    t.val = t.left.val
                    t.right = t.left.right
                    t.left = t.left.left
                    AVLTree.rebalance(t)
                elif t.right: # replace node with its only child (the right one)
                    t.val = t.right.val
                    t.left = t.right.left
                    t.right = t.right.right
                    AVLTree.rebalance(t)
                else:
                    if parent:
                        if isleft:
                            parent.left = None
                        else:
                            parent.right = None
                    else:
                        self.root = None

        rec_del(None,None,self.root,val)
        self.size += -1
        ### END SOLUTION

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
# TEST CASES
################################################################################
def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

# LL-fix (simple) test
# 10 points
def test_ll_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 2, 1]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RR-fix (simple) test
# 10 points
def test_rr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 2, 3]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# LR-fix (simple) test
# 10 points
def test_lr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 1, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RL-fix (simple) test
# 10 points
def test_rl_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 3, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# ensure key order is maintained after insertions and removals
# 30 points
def test_key_order_after_ops():
    tc = TestCase()
    vals = list(range(0, 100000000, 333333))
    random.shuffle(vals)

    t = AVLTree()
    for x in vals:
        t.add(x)

    for _ in range(len(vals) // 3):
        to_rem = vals.pop(random.randrange(len(vals)))
        del t[to_rem]

    vals.sort()

    for i,val in enumerate(t):
        tc.assertEqual(val, vals[i])

# stress testing
# 30 points
def test_stress_testing():
    tc = TestCase()

    def check_balance(t):
        tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

    t = AVLTree()
    vals = list(range(1000))
    random.shuffle(vals)
    for i in range(len(vals)):
        t.add(vals[i])
        for x in vals[:i+1]:
            tc.assertIn(x, t, 'Element added not in tree')
        traverse(t.root, check_balance)

    random.shuffle(vals)
    for i in range(len(vals)):
        del t[vals[i]]
        for x in vals[i+1:]:
            tc.assertIn(x, t, 'Incorrect element removed from tree')
        for x in vals[:i+1]:
            tc.assertNotIn(x, t, 'Element removed still in tree')
        traverse(t.root, check_balance)



################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_ll_fix_simple,
              test_rr_fix_simple,
              test_lr_fix_simple,
              test_rl_fix_simple,
              test_key_order_after_ops,
              test_stress_testing]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
