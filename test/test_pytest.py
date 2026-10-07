from src import calculator


def test_fun1():
    assert calculator.fun1(10, 3) == 30
    assert calculator.fun1(0, 5) == 0
    assert calculator.fun1(5.5, 2) == 11.0
    assert calculator.fun1(100, 1) == 100


def test_fun2():
    assert calculator.fun2(50, 30) == 20
    assert calculator.fun2(30, 30) == 0
    assert calculator.fun2(10, 30) == -20
    assert calculator.fun2(0, 0) == 0


def test_fun3():
    assert calculator.fun3(10, 7) == 70
    assert calculator.fun3(0, 30) == 0
    assert calculator.fun3(5, 14) == 70
    assert calculator.fun3(2.5, 4) == 10.0


def test_fun4():
    assert calculator.fun4(30, 20, 70) == 120
    assert calculator.fun4(0, 0, 0) == 0
    assert calculator.fun4(10, -5, 50) == 55
    assert calculator.fun4(15, 5, 30) == 50
