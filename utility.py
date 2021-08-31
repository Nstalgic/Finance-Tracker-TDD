from expenses import Expense


def get_amount_history_list(list_of_dates: list[Expense]) -> list[float]:
    """Returns a list of rolling sums based on provided list.

    Args:
        list_of_dates (list[Expense]): List of expense objects

    Returns:
        list[float]: a list of rolling sums
    """
    total = 0
    expense_amounts = []

    for expense in list_of_dates:
        total += expense.amount
        expense_amounts.append(total)

    return expense_amounts


def get_frequency_history_list(list_of_dates: list[Expense]) -> dict[int]:
    """Returns a dictonary containing number of purchases per day of week.

    Args:
        list_of_dates (list[Expense]): List of expense objects

    Returns:
        dict[int]: Dictonary containing number of purchases per day.
    """
    frequency_list = {
        "Sun": 0,
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
    }
    if list_of_dates:
        for expense in list_of_dates:
            day_key = expense.date.strftime("%a")
            frequency_list[day_key] += 1

    return frequency_list
