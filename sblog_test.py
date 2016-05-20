"""Unit tests for sblog package."""

import unittest

from sblog import Foo


class TestFoo(unittest.TestCase):

    def test_noNewItems(self):
        a = [1, 2, 3, 4, 5]
        b = [2, 3, 4, 5]
        f = Foo(a)
        self.assertEqual(f.update(b), [])

    def test_newItemsWithOverlap(self):
        a = [1, 2, 3, 4, 5]
        b = [3, 4, 5, 6, 7]
        f = Foo(a)
        self.assertEqual(f.update(b), [6, 7])

    def test_newItemsNoOverlap(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        f = Foo(a)
        self.assertEqual(f.update(b), [6, 7, 8, 9, 10])

    def test_allNewWhenEmpty(self):
        b = [1, 2, 3, 4, 5]
        f = Foo()
        self.assertEqual(f.update(b), [1, 2, 3, 4, 5])

    def test_multiple(self):
        f = Foo()
        self.assertEqual(f.update([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
        self.assertEqual(f.update([1, 2, 3, 4, 5]), [])
        self.assertEqual(f.update([2, 3, 4, 5, 6]), [6])
        self.assertEqual(f.update([5, 6, 7, 8, 9]), [7, 8, 9])

if __name__ == '__main__':
    unittest.main()
