from datetime import datetime
from datetime import date as dt
import pytest


class Test_expense_object:
    def setup_class(self):
        from expenses import Expense

        self.exp = Expense("test", 22.2, "food", "2019-01-01")

    def test_expense_object_creation(self):
        from expenses import Expense

        assert isinstance(self.exp, Expense)

    def test_expense_object_type_name_is_string(self):
        assert isinstance(self.exp.name, str)

    def test_expense_object_type_price_is_float(self):
        assert isinstance(self.exp.amount, float)

    def test_expense_object_type_price_is_float(self):
        assert isinstance(self.exp.amount, float)

    def test_expense_object_type_category_is_string(self):
        assert isinstance(self.exp.category, str)

    def test_expense_object_type_date_is_datetime_date(self):
        assert isinstance(self.exp.date, dt)

    def test_no_date_uses_todays_day(self):
        from expenses import Expense

        self.exp = Expense("test", 22.2, "food")
        assert self.exp.get_date() == dt.today()

    def test_no_date_uses_todays_day_and_updates(self):

        new_date_string = "2019-01-01"

        self.exp.set_date(new_date_string)
        new_date = datetime.strptime(new_date_string, "%Y-%m-%d").date()
        assert self.exp.get_date() == new_date

    def test_get_amount(self):
        assert self.exp.get_amount() == 22.2

    def test_get_category(self):
        assert self.exp.get_category() == "food"

    def test_get_date(self):
        creation_date = datetime.strptime("2019-01-01", "%Y-%m-%d").date()
        assert self.exp.get_date() == creation_date

    def test_set_expense_name(self):
        self.exp.set_name("test")
        assert self.exp.name == "test"

    def test_set_amount_positive(self):
        self.exp.set_amount(33.3)
        assert self.exp.amount == 33.3

    def test_set_amount_negativee(self):
        self.exp.set_amount(-33.3)
        assert self.exp.amount == -33.3

    def test_set_category(self):
        self.exp.set_category("hardware")
        assert self.exp.category == "hardware"

    def test_set_date(self):

        date_string = "2020-06-06"
        self.exp.set_date(date_string)

        new_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        assert self.exp.date == new_date

    def test_get_name(self):
        assert self.exp.get_name() == "test"


class Test_expenses_tracker_object:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        from expenses import ExpensesTracker

        self.exp_tracker = ExpensesTracker()

    def test_expenses_list_creation(self):
        from expenses import ExpensesTracker

        assert isinstance(self.exp_tracker, ExpensesTracker)

    def test_expenses_list_type_is_list(self):
        assert isinstance(self.exp_tracker.expenses_list, list)

    def test_add_expense(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        assert len(self.exp_tracker.expenses_list) == 1

    def test_remove_expense_by_index(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.remove_expense_by_index(0)
        assert self.exp_tracker.size == 0

    def test_get_expenses_list(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        assert len(self.exp_tracker.get_expenses_list()) == 1

    def test_get_expenses_list_with_many_entrys(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2022-02-02"))
        assert len(self.exp_tracker.get_expenses_list()) == 2

    def test_add_two_remove_one_by_index(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.remove_expense_by_index(0)
        assert len(self.exp_tracker.get_expenses_list()) == 1

    def test_get_expense_by_index(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        exp_at_index = self.exp_tracker.get_expense_by_index(0)
        assert exp_at_index.amount == 22.2

    def test_get_expense_by_index_with_no_entrys(self):

        exp_at_index = self.exp_tracker.get_expense_by_index(0)
        assert exp_at_index is None

    def test_get_expense_by_index_with_no_entrys_and_negative_index(self):

        exp_at_index = self.exp_tracker.get_expense_by_index(-1)
        assert exp_at_index is None

    def test_get_expense_list_with_no_entrys(self):
        assert self.exp_tracker.get_expenses_list() == []

    def test_get_expense_list_by_category(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 60, "coffee", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test6", 70, "coffee", "2019-01-01"))

        list_of_food_expenses = self.exp_tracker.get_expenses_list_by_category("food")

        assert len(list_of_food_expenses) == 3

    def test_get_expense_list_by_date(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 60, "coffee", "2020-01-01"))

        list_of_date_expenses = self.exp_tracker.get_expenses_list_by_date("2019-01-01")
        assert len(list_of_date_expenses) == 3

    def test_get_expense_list_by_date_range_first_element(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 60, "coffee", "2022-01-01"))

        list_of_date_range_expenses = self.exp_tracker.get_expenses_list_by_date_range(
            "2019-01-01", "2020-01-01"
        )

        first_element_sum = list_of_date_range_expenses[0].amount
        assert first_element_sum == 22.2

    def test_get_expense_list_by_date_range_last_element(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 60, "coffee", "2022-01-01"))

        list_of_date_range_expenses = self.exp_tracker.get_expenses_list_by_date_range(
            "2019-01-01", "2020-01-01"
        )

        last_element_sum = list_of_date_range_expenses[-1].amount
        assert last_element_sum == 50

    def test_get_expense_list_by_amount_range(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test", 22.2, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 60, "coffee", "2022-01-01"))

        list_of_amount_range_expenses = (
            self.exp_tracker.get_expenses_list_by_amount_range(20, 40)
        )
        assert len(list_of_amount_range_expenses) == 4

    def test_get_all_expense_sum(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        total = self.exp_tracker.get_all_expenses_amount_sum()
        assert total == 150.0

    def test_get_all_amount_sum_by_category(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        total = self.exp_tracker.get_all_amount_sum_by_category("food")
        assert total == 60.0

    def test_get_all_amount_sum_by_date(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        total = self.exp_tracker.get_all_amount_sum_by_date("2019-01-01")

        assert total == 60.0

    def test_get_all_amount_sum_by_date_range(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "3022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "3020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        total = self.exp_tracker.get_all_amount_sum_by_date_range(
            "3020-01-01", "3022-01-01"
        )

        assert total == 90

    def test_get_average_of_all_expenses(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        average = self.exp_tracker.get_average_of_all_expenses()

        assert average == 30

    def test_get_average_of_expenses_by_category(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        average = self.exp_tracker.get_average_of_expenses_by_category("food")

        assert average == 20

    def test_get_average_of_expenses_by_date(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        average = self.exp_tracker.get_average_of_expenses_by_date("2019-01-01")

        assert average == 20

    def test_get_average_of_date_range(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "3022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "3020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        average = self.exp_tracker.get_average_of_date_range("3020-01-01", "3022-01-01")

        assert average == 45

    def test_get_number_of_purchases_a_day(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2022-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2020-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2019-01-01"))

        number = self.exp_tracker.get_number_of_purchases_a_day("2019-01-01")

        assert number == 3

    def test_get_oldest_date_from_expenses(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2015-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2017-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2018-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2020-01-01"))

        date = self.exp_tracker.get_oldest_date()
        oldest_date = "2015-01-01"

        assert oldest_date == date

    def test_get_newest_date_from_expenses(self):
        from expenses import Expense

        self.exp_tracker.add_expense(Expense("test1", 20, "food", "2015-01-01"))
        self.exp_tracker.add_expense(Expense("test2", 30, "food", "2017-01-01"))
        self.exp_tracker.add_expense(Expense("test3", 40, "games", "2018-01-01"))
        self.exp_tracker.add_expense(Expense("test4", 50, "bills", "2019-01-01"))
        self.exp_tracker.add_expense(Expense("test5", 10, "food", "2020-01-01"))

        date = self.exp_tracker.get_newest_date()
        new_date = "2020-01-01"

        assert new_date == date

    def test_get_list_of_week_dates(self):
        from expenses import Expense

        date = self.exp_tracker.get_week_dates("2021-08-18")
        week_dates = [
            "2021-08-15",
            "2021-08-16",
            "2021-08-17",
            "2021-08-18",
            "2021-08-19",
            "2021-08-20",
            "2021-08-21",
        ]

        assert week_dates == date

    def test_get_list_of_week_dates_end_of_month(self):
        from expenses import Expense

        date = self.exp_tracker.get_week_dates("2021-08-29")
        week_dates = [
            "2021-08-29",
            "2021-08-30",
            "2021-08-31",
            "2021-09-01",
            "2021-09-02",
            "2021-09-03",
            "2021-09-04",
        ]

        assert week_dates == date

    def test_get_list_of_month_dates(self):
        from expenses import Expense

        obj1 = Expense("test1", 20, "food", "2015-01-01")
        obj2 = Expense("test2", 30, "food", "2017-01-01")
        obj3 = Expense("test3", 40, "games", "2018-01-01")
        obj4 = Expense("test4", 50, "bills", "2019-02-01")
        obj5 = Expense("test5", 10, "food", "2020-03-01")

        self.exp_tracker.add_expense(obj1)
        self.exp_tracker.add_expense(obj2)
        self.exp_tracker.add_expense(obj3)
        self.exp_tracker.add_expense(obj4)
        self.exp_tracker.add_expense(obj5)

        date = self.exp_tracker.get_expenses_by_month("2020-01-08")
        week_dates = [
            obj1,
            obj2,
            obj3,
        ]

        assert week_dates == date

    def test_get_list_of_year_dates(self):
        from expenses import Expense

        obj1 = Expense("test1", 20, "food", "2015-01-01")
        obj2 = Expense("test2", 30, "food", "2020-01-01")
        obj3 = Expense("test3", 40, "games", "2018-01-01")
        obj4 = Expense("test4", 50, "bills", "2019-02-01")
        obj5 = Expense("test5", 10, "food", "2020-03-01")

        self.exp_tracker.add_expense(obj1)
        self.exp_tracker.add_expense(obj2)
        self.exp_tracker.add_expense(obj3)
        self.exp_tracker.add_expense(obj4)
        self.exp_tracker.add_expense(obj5)

        date = self.exp_tracker.get_expenses_by_year("2020-01-08")
        week_dates = [
            obj2,
            obj5,
        ]

        assert week_dates == date

    def test_get_sum_of_expense_list(self):
        from expenses import Expense

        obj1 = Expense("test1", 20, "food", "2015-01-01")
        obj2 = Expense("test2", 30, "food", "2017-01-01")
        obj3 = Expense("test3", 40, "games", "2018-01-01")
        obj4 = Expense("test4", 50, "bills", "2019-02-01")
        obj5 = Expense("test5", 10, "food", "2020-03-01")

        list_of_expsenses = [obj1, obj2, obj3, obj4, obj5]

        sum = self.exp_tracker.get_sum_of_expenses(list_of_expsenses)
        assert sum == 150

    def test_purchase_per_day(self):
        from expenses import Expense

        obj1 = Expense("test1", 20, "food", "2015-01-01")
        obj2 = Expense("test2", 30, "food", "2020-01-01")
        obj3 = Expense("test3", 40, "games", "2018-01-01")
        obj4 = Expense("test4", 50, "bills", "2015-01-01")
        obj5 = Expense("test5", 10, "food", "2020-03-01")

        self.exp_tracker.add_expense(obj1)
        self.exp_tracker.add_expense(obj2)
        self.exp_tracker.add_expense(obj3)
        self.exp_tracker.add_expense(obj4)
        self.exp_tracker.add_expense(obj5)

        days = self.exp_tracker.purchases_per_day("2015-01-01")
        assert days == 2
