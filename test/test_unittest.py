import sys
import os
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestCalculator(unittest.TestCase):

    def test_fun1(self):
        self.assertEqual(calculator.fun1(10, 3), 30)
        self.assertEqual(calculator.fun1(0, 5), 0)
        self.assertEqual(calculator.fun1(5.5, 2), 11.0)
        self.assertEqual(calculator.fun1(100, 1), 100)

    def test_fun2(self):
        self.assertEqual(calculator.fun2(50, 30), 20)
        self.assertEqual(calculator.fun2(30, 30), 0)
        self.assertEqual(calculator.fun2(10, 30), -20)
        self.assertEqual(calculator.fun2(0, 0), 0)

    def test_fun3(self):
        self.assertEqual(calculator.fun3(10, 7), 70)
        self.assertEqual(calculator.fun3(0, 30), 0)
        self.assertEqual(calculator.fun3(5, 14), 70)
        self.assertEqual(calculator.fun3(2.5, 4), 10.0)

    def test_fun4(self):
        self.assertEqual(calculator.fun4(30, 20, 70), 120)
        self.assertEqual(calculator.fun4(0, 0, 0), 0)
        self.assertEqual(calculator.fun4(10, -5, 50), 55)
        self.assertEqual(calculator.fun4(15, 5, 30), 50)


if __name__ == '__main__':
    unittest.main()