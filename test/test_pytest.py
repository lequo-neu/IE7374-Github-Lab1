import pytest

from src import calculator


def test_fun1():
    assert calculator.fun1(10, 3) == 30
    assert calculator.fun1(0, 5) == 0
    assert calculator.fun1(5.5, 2) == 11.0
    assert calculator.fun1(100, 1) == 100
    assert calculator.fun1(0, 0) == 0
    assert calculator.fun1(0.5, 4) == 2.0


def test_fun2():
    assert calculator.fun2(50, 30) == 20
    assert calculator.fun2(30, 30) == 0
    assert calculator.fun2(10, 30) == -20
    assert calculator.fun2(0, 0) == 0
    assert calculator.fun2(0, 10) == -10
    assert calculator.fun2(100, 0) == 100


def test_fun3():
    assert calculator.fun3(10, 7) == 70
    assert calculator.fun3(0, 30) == 0
    assert calculator.fun3(5, 14) == 70
    assert calculator.fun3(2.5, 4) == 10.0
    assert calculator.fun3(0, 0) == 0
    assert calculator.fun3(1, 100) == 100


def test_fun4():
    assert calculator.fun4(30, 20, 70) == 120
    assert calculator.fun4(0, 0, 0) == 0
    assert calculator.fun4(10, -5, 50) == 55
    assert calculator.fun4(15, 5, 30) == 50
    assert calculator.fun4(0, -10, 0) == -10
    assert calculator.fun4(100, 0, 0) == 100


@pytest.mark.parametrize("func", [calculator.fun1, calculator.fun2, calculator.fun3])
@pytest.mark.parametrize("bad_args", [("10", 3), (10, None), ([1], 2)])
def test_rejects_non_numeric_input(func, bad_args):
    with pytest.raises(ValueError, match="must be numbers"):
        func(*bad_args)
