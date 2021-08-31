from datetime import datetime
from datetime import timedelta
from datetime import date as dt
import calendar


class Expense:
    def __init__(self, name: str, amount: float, category: str, date=None):
        self.name = name
        self.amount = amount
        self.category = category
        if not date:
            self.date = dt.today()
        else:
            self.date = datetime.strptime(date, "%Y-%m-%d").date()

    def set_name(self, name: str):
        self.name = name

    def set_amount(self, amount: float):
        self.amount = amount

    def set_category(self, category: str):
        self.category = category

    def set_date(self, date: str):
        self.date = datetime.strptime(date, "%Y-%m-%d").date()

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def get_category(self):
        return self.category

    def get_date(self):
        return self.date


class ExpensesTracker:
    def __init__(self):
        self.expenses_list = []
        self.size = 0

    def add_expense(self, expense: Expense):
        self.expenses_list.append(expense)
        print("Expense added")
        self.size += 1

    def remove_expense_by_index(self, index: int):
        self.expenses_list.pop(index)
        print("Expense removed")
        self.size -= 1

    def get_expenses_list(self) -> list[Expense]:
        return self.expenses_list

    def get_expense_by_index(self, index: int) -> Expense:
        if self.size != 0:
            return self.expenses_list[index]
        else:
            return None

    def get_expenses_list_by_category(self, category: str) -> list[Expense]:
        return [
            expense for expense in self.expenses_list if expense.category == category
        ]

    def get_expenses_list_by_date(self, date: str) -> list[Expense]:
        date = self.convert_date_to_datetime(date)
        return [expense for expense in self.expenses_list if expense.date == date]

    def get_expenses_list_by_date_range(
        self, date_start: str, date_end: str
    ) -> list[Expense]:

        date_start = self.convert_date_to_datetime(date_start)
        date_end = self.convert_date_to_datetime(date_end)

        return [
            expense
            for expense in self.expenses_list
            if date_start <= expense.date <= date_end
        ]

    def convert_date_to_datetime(self, date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d").date()

    def get_expenses_list_by_amount_range(
        self, min_number: int, max_number: int
    ) -> list:
        return [
            expense
            for expense in self.expenses_list
            if min_number <= expense.amount <= max_number
        ]

    def get_all_expenses_amount_sum(self) -> float:
        return self.get_sum_of_all_in_expense_list()

    def get_all_amount_sum_by_category(self, category: str) -> float:
        list_by_categories = self.get_expenses_list_by_category(category)

        return self.get_sum_of_all_in_expense_list(list_by_categories)

    def get_all_amount_sum_by_date(self, date: str) -> float:
        list_by_dates = self.get_expenses_list_by_date(date)

        return self.get_sum_of_all_in_expense_list(list_by_dates)

    def get_all_amount_sum_by_date_range(self, date_start: str, date_end: str) -> float:
        list_by_dates = self.get_expenses_list_by_date_range(date_start, date_end)

        return self.get_sum_of_all_in_expense_list(list_by_dates)

    def get_average_of_all_expenses(self) -> float:
        return self.get_average_of_all_in_expense_list()

    def get_average_of_all_in_expense_list(self, list_of_expenses=None) -> float:
        list_of_expenses = (
            self.expenses_list if not list_of_expenses else list_of_expenses
        )
        return self.get_average_from_list(list_of_expenses)

    def get_average_of_expenses_by_category(self, category: str) -> float:
        list_of_expenses = self.get_expenses_list_by_category(category)

        return self.get_average_from_list(list_of_expenses)

    def get_average_of_expenses_by_date(self, date: str) -> float:
        list_of_expenses = self.get_expenses_list_by_date(date)

        return self.get_average_from_list(list_of_expenses)

    def get_average_of_date_range(self, date_start: str, date_end: str) -> float:
        list_of_expenses = self.get_expenses_list_by_date_range(date_start, date_end)

        return self.get_average_from_list(list_of_expenses)

    def get_number_of_purchases_a_day(self, date: str) -> int:
        list_of_expenses = self.get_expenses_list_by_date(date)

        return len(list_of_expenses)

    def get_average_from_list(self, list_of_expenses):
        return self.get_sum_of_all_in_expense_list(list_of_expenses) / len(
            list_of_expenses
        )

    def get_sum_of_all_in_expense_list(
        self, list_of_expenses: list[Expense] = None
    ) -> float:
        list_of_expenses = (
            self.expenses_list if not list_of_expenses else list_of_expenses
        )
        return sum([expense.amount for expense in list_of_expenses])

    def get_oldest_date(self) -> str:
        return str(min([expense.date for expense in self.expenses_list]))

    def get_newest_date(self) -> str:
        return str(max([expense.date for expense in self.expenses_list]))

    def get_week_dates(self, date: str) -> list[str]:
        year, month, day = self.extract_date_from_string(date)
        date = datetime(year, month, day)
        week_dates = []
        date_string = date.strftime("%a")

        while date_string != "Sun":
            date = date - timedelta(days=1)
            date_string = date.strftime("%a")

        for _ in range(7):
            week_dates.append(str(date.date()))
            date += timedelta(days=1)

        return week_dates

    def create_calendar_object(self, year, month):
        calendar.setfirstweekday(calendar.SUNDAY)
        obj = calendar.monthcalendar(year, month)
        return obj

    def format_string_to_string_date(self, year, month, day):
        if month >= 10:
            month = str(month)
        else:
            month = "0" + str(month)

        if day >= 10:
            day = str(day)
        else:
            day = "0" + str(day)

        return str(year) + "-" + month + "-" + day

    def extract_date_from_string(self, date):
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        return year, month, day

    def get_expenses_by_day(self, day: str) -> list[Expense]:
        expenses_by_day = []
        for expense in self.expenses_list:
            if expense.date == day:
                expenses_by_day.append(expense)

        return expenses_by_day

    def get_expenses_by_month(self, date: str) -> list[Expense]:
        expenses_by_month = []
        month = self.extract_date_from_string(date)[1]
        for expense in self.expenses_list:
            if expense.date.month == month:
                expenses_by_month.append(expense)

        return expenses_by_month

    def get_expenses_by_year(self, date: str) -> list[Expense]:
        expenses_by_year = []
        year = self.extract_date_from_string(date)[0]
        for expense in self.expenses_list:
            if expense.date.year == year:
                expenses_by_year.append(expense)

        return expenses_by_year

    def get_sum_of_expenses(self, list_of_expenses: list[Expense]) -> float:
        return sum([expense.amount for expense in list_of_expenses])

    def purchases_per_day(self, date: str) -> int:
        return len(self.get_expenses_list_by_date(date))
