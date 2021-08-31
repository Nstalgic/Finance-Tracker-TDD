from PySide6.QtCore import QObject, Signal


class ThreadSignals(QObject):

    update_data = Signal()
