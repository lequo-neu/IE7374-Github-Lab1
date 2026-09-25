# src/calculator.py
# IE7374 Lab 1 — Modified version
# Original: generic arithmetic (add, subtract, multiply, sum-of-3)
# Modified: drug shortage supply-chain calculations


def fun1(daily_usage, lead_time_days):
    """
    Calculates safety stock (units needed to cover lead time).
    Args:
        daily_usage (int/float): Units consumed per day.
        lead_time_days (int/float): Days to receive a new order.
    Returns:
        int/float: Safety stock threshold.
    Raises:
        ValueError: If inputs are not numbers.
    """
    if not (isinstance(daily_usage, (int, float)) and
            isinstance(lead_time_days, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    return daily_usage * lead_time_days


def fun2(stock_on_hand, safety_stock):
    """
    Calculates stock surplus above the safety stock threshold.
    Args:
        stock_on_hand (int/float): Current inventory level.
        safety_stock (int/float): Minimum required stock.
    Returns:
        int/float: Surplus (negative = below safety stock).
    Raises:
        ValueError: If inputs are not numbers.
    """
    if not (isinstance(stock_on_hand, (int, float)) and
            isinstance(safety_stock, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    return stock_on_hand - safety_stock


def fun3(daily_usage, horizon_days):
    """
    Calculates total units needed over a forecast horizon.
    Args:
        daily_usage (int/float): Units consumed per day.
        horizon_days (int/float): Forecast window (e.g. D50 or D80).
    Returns:
        int/float: Total units required.
    Raises:
        ValueError: If inputs are not numbers.
    """
    if not (isinstance(daily_usage, (int, float)) and
            isinstance(horizon_days, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    return daily_usage * horizon_days


def fun4(safety_stock, surplus, units_needed):
    """
    Computes a composite shortage urgency score.
    Args:
        safety_stock (int/float): Minimum required stock.
        surplus (int/float): Stock above safety level (can be negative).
        units_needed (int/float): Total units required over horizon.
    Returns:
        int/float: Composite urgency score.
    """
    return safety_stock + surplus + units_needed