from PyQt5.QtWidgets import *
from dialog_add_category import DialogAddCategory
from dialog_add_revenue_or_expense import DialogAddRevenueOrExpense
from dialog_transfer_money import DialogTransferMoney

class WidgetMgmtButtons(QWidget):
    def __init__(self, category_manager, mainwindow_update_all):
        super(QWidget, self).__init__()
        self._category_manager = category_manager
        self._mainwindow_update_all = mainwindow_update_all

        self._add_category_button = QPushButton('Add Category')
        self._add_revenue_button = QPushButton('Add Revenue')
        self._add_expense_button = QPushButton('Add Expense')
        self._transfer_money_button = QPushButton('Transfer Money')
        self._add_category_button.clicked.connect(self.add_category_pressed)
        self._add_revenue_button.clicked.connect(self.add_revenue_pressed)
        self._add_expense_button.clicked.connect(self.add_expense_pressed)
        self._transfer_money_button.clicked.connect(self.transfer_money_pressed)

        self._top_vlayout = QHBoxLayout()
        self._top_vlayout.addWidget(self._add_category_button)
        self._top_vlayout.addWidget(self._add_revenue_button)
        self._top_vlayout.addWidget(self._add_expense_button)
        self._top_vlayout.addWidget(self._transfer_money_button)
        
        self.setLayout(self._top_vlayout)

    def add_category_pressed(self):
        dialog = DialogAddCategory(self._category_manager, self)
        dialog.exec_()
        self._mainwindow_update_all()
    
    def add_revenue_pressed(self):
        dialog = DialogAddRevenueOrExpense(self._category_manager, parent=self)
        dialog.exec_()
        self._mainwindow_update_all()
    
    def add_expense_pressed(self):
        dialog = DialogAddRevenueOrExpense(self._category_manager,
                                           is_revenue=False,
                                           parent=self)
        dialog.exec_()
        self._mainwindow_update_all()

    def transfer_money_pressed(self):
        dialog = DialogTransferMoney(self._category_manager, self)
        dialog.exec_()
        self._mainwindow_update_all()