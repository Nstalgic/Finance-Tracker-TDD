"""
///////////////////////////////////////////////////////////////
APPLICATION BY: MICHAEL HUFF
Application created with: Qt Designer and PyQt5
AUG 31, 2021
V: 1.0.0
///////////////////////////////////////////////////////////////
"""

import sys
from datetime import date as dt

import matplotlib
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator

import utility
from expenses import Expense, ExpensesTracker
from signals import ThreadSignals

matplotlib.use("Qt5Agg")

plt.set_loglevel("WARNING")
sns.set_style("darkgrid")
threadSignals = ThreadSignals()


class MplCanvas(FigureCanvasQTAgg):
    """Creates a Matplotlib object and draws the plot on it

    Args:
        FigureCanvasQTAgg (Figure): Figure of a graph
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ExpenseWindow(QtWidgets.QMainWindow):
    """Main window of application"""

    def __init__(self, expense_tracker):
        super(ExpenseWindow, self).__init__()
        uic.loadUi("addexpense.ui", self)

        self.btn_add.clicked.connect(self.add_expense)
        self.expense_tracker = expense_tracker

        self.window_setup()
        self.validate_amount()

    def window_setup(self):
        """Main set up of the window"""
        self.de_date.setDate(QDate.currentDate())
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())

    def validate_amount(self):
        """Validates the amount input"""
        validator = QRegExpValidator(QRegExp(r"[0-9].+"))
        self.le_amount.setValidator(validator)

    def add_expense(self):
        """Adds an expense to the list"""
        new_expense = self._create_expense()
        self.expense_tracker.add_expense(new_expense)
        threadSignals.update_data.emit()
        self._reset_fields()

    def _create_expense(self):
        """Creates an expense object"""
        name = self.le_name.text()
        amount = float(self.le_amount.text())
        category = self.le_category.text()
        date = self.de_date.text()

        return Expense(name, amount, category, date)

    def _reset_fields(self):
        """Resets the fields"""
        self.le_name.clear()
        self.le_amount.clear()
        self.le_category.clear()
        self.de_date.setDate(QDate.currentDate())


class MainWindow(QtWidgets.QMainWindow):
    """Main window of application"""

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("tracker.ui", self)

        self.expenses_tracker = ExpensesTracker()
        self.expense_window = ExpenseWindow(self.expenses_tracker)
        self.setFixedSize(self.size())

        self.setup_date_picker()
        self.create_graphs()

        self.action_add.triggered.connect(self.open_expense_window)
        threadSignals.update_data.connect(self.update_graphs)

        self.show()

    def create_graphs(self):
        """Creates the graph objects"""
        mpl_linegraph, mpl_bargraph = self._create_graph_objects()
        self._plot_graph_objects(mpl_linegraph, mpl_bargraph)
        self._set_up_graph_objects(mpl_linegraph, mpl_bargraph)

    def _set_up_graph_objects(self, mpl_linegraph, mpl_bargraph):
        """Sets up the graph object
        Args:
            mpl_linegraph (MplCanvas): MplCanvas object
            mpl_bargraph (MplCanvas): MplCanvas object
        """
        self._graph_setup_line(mpl_linegraph)
        self._graph_setup_bar(mpl_bargraph)

    def _plot_graph_objects(self, mpl_linegraph, mpl_bargraph):
        """Plots the graph objects"""
        self._plot_line_graph(mpl_linegraph)
        self._plot_bar_graph(mpl_bargraph)

    def _create_graph_objects(self) -> MplCanvas:
        """Creates MplCanvas objects

        Returns:
            MplCanvas: MplCanvas object
        """
        mpl_linegraph = MplCanvas(self, width=5, height=4, dpi=100)
        mpl_bargraph = MplCanvas(self, width=5, height=4, dpi=100)
        return mpl_linegraph, mpl_bargraph

    def _plot_bar_graph(self, mpl_bargraph):
        """Plots a bar graph to the provided MplCanvas object

        Args:
            mpl_bargraph (MplCanvas): MplCanvas object
        """
        today = str(dt.today())
        list_of_dates = self.expenses_tracker.get_week_dates(today)
        list_of_expenses = self._get_expenses_by_dates(list_of_dates)
        frequency_list = utility.get_frequency_history_list(list_of_expenses)
        mpl_bargraph.axes.bar(
            list(frequency_list.keys()), list(frequency_list.values()), align="center"
        )
        mpl_bargraph.axes.set_title("Purchases A Day")
        mpl_bargraph.axes.set_ylabel("Number Of Items")

    def _plot_line_graph(self, mpl_linegraph):
        """Plots a line graph to the provided MplCanvas object

        Args:
            mpl_bargraph (MplCanvas): MplCanvas object
        """
        today = str(dt.today())
        list_of_dates = self.expenses_tracker.get_expenses_by_month(today)
        total_amount = utility.get_amount_history_list(list_of_dates)
        mpl_linegraph.axes.set_ylabel("Amount")
        mpl_linegraph.axes.set_title("Monthly Spending")

        mpl_linegraph.axes.plot(total_amount)

    def _graph_setup_line(self, mpl_linegraph):
        """Creates layout and present MplCanvas Object"""
        layout_linegraph = QtWidgets.QVBoxLayout()
        layout_linegraph.addWidget(mpl_linegraph)
        self.mpl_linegraph.setLayout(layout_linegraph)

    def _graph_setup_bar(self, mpl_bargraph):
        """Creates layout and present MplCanvas Object"""
        layout_bargraph = QtWidgets.QVBoxLayout()
        layout_bargraph.addWidget(mpl_bargraph)
        self.mpl_bargraph.setLayout(layout_bargraph)

    def update_graphs(self):
        """Updates then draws the updated MplCanvas object"""
        graphs = self.findChildren(MplCanvas)
        self._plot_line_graph(graphs[0])
        self._plot_bar_graph(graphs[1])

        graphs[0].draw()
        graphs[1].draw()

    def open_expense_window(self):
        """Opens the expense window"""
        self.expense_window.show()

    def _display_item_on_list(self):
        """Displays the item on the list"""
        item = self.expenses_tracker.get_expense_by_index(-1)

        self.lw_exspense.addItem(f"{item.name}          ${item.amount}")

    def _display_all_items_on_list(self):
        """Displays all items on the list"""
        list_of_expenses = self.expenses_tracker.get_expenses_list()
        self._set_total_label(list_of_expenses)
        self._display_expenses(list_of_expenses)

    def index_change_handler(self):
        """Handles index changes"""

        self.lw_exspense.clear()

        if self.cbo_date.currentIndex() == 0:
            # show today
            self._display_today_on_list()
        elif self.cbo_date.currentIndex() == 1:
            # show this week
            self._display_by_week_on_list()
        elif self.cbo_date.currentIndex() == 2:
            # show this month
            self._display_by_month_on_list()
        elif self.cbo_date.currentIndex() == 3:
            # show this year
            self._display_by_year_on_list()
        elif self.cbo_date.currentIndex() == 4:
            # show all
            self._display_all_items_on_list()

    def setup_date_picker(self):
        """Sets up the date picker"""
        self.cbo_date.addItem("Today")
        self.cbo_date.addItem("This week")
        self.cbo_date.addItem("This month")
        self.cbo_date.addItem("This year")
        self.cbo_date.addItem("All time")
        self.cbo_date.currentIndexChanged.connect(self.index_change_handler)
        self.cbo_date.setCurrentIndex(-1)

    def _set_total_label(self, list_of_expenses):
        """Sets the total label with sum of provided expense list

        Args:
            list_of_expenses (Expenses): A list of expenses
        """
        total = str(
            "{:.2f}".format(
                round(self.expenses_tracker.get_sum_of_expenses(list_of_expenses), 2)
            )
        )
        self.lbl_total.setText(f"${total}")

    def _display_today_on_list(self):
        """Displays today's expenses on the list"""
        today = str(dt.today())
        list_of_expenses = self.expenses_tracker.get_expenses_list_by_date(today)
        self._set_total_label(list_of_expenses)
        self._display_expenses(list_of_expenses)

    def _display_by_week_on_list(self):
        """Displays expenses by week on the list"""
        today = str(dt.today())
        list_of_dates = self.expenses_tracker.get_week_dates(today)
        list_of_expenses = self._get_expenses_by_dates(list_of_dates)
        if list_of_expenses:
            self._set_total_label(list_of_expenses)
            self._display_expenses(list_of_expenses)

    def _display_by_month_on_list(self):
        """Displays expenses by month on the list"""
        today = str(dt.today())
        list_of_dates = self.expenses_tracker.get_expenses_by_month(today)
        self._set_total_label(list_of_dates)
        self._display_expenses(list_of_dates)

    def _display_by_year_on_list(self):
        """Displays expenses by year on the list"""
        today = str(dt.today())
        list_of_dates = self.expenses_tracker.get_expenses_by_year(today)
        self._set_total_label(list_of_dates)
        self._display_expenses(list_of_dates)

    def _display_expenses(self, list_of_dates):
        """Displays all expenses on the list widget

        Args:
            list_of_dates (Expenses): List of expenses
        """
        for item in list_of_dates:
            total = str("{:.2f}".format(round(item.amount, 2)))
            self.lw_exspense.addItem(f"{item.name}          ${total}")

    def _get_expenses_by_dates(self, list_of_dates: list[str]) -> list[Expense]:
        """Return a list of expenses matching provided dates.

        Args:
            list_of_dates (list[str]): list of dates as string type

        Returns:
            list[Expense]: list of expense
        """
        list_of_expenses = []
        for date in list_of_dates:
            list_of_expenses += self.expenses_tracker.get_expenses_list_by_date(date)

        return list_of_expenses


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
