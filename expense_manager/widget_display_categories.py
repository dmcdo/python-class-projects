from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

class WidgetDisplayCategories(QWidget):
    def __init__(self, category_manager):
        super(QWidget, self).__init__()
        self._category_manager = category_manager

        self._category_combobox = QComboBox()
        self._category_combobox.currentTextChanged.connect(self.update_table)

        self._category_table = QTableWidget()
        self._category_table.setColumnCount(2)
        self._category_table.horizontalHeader().setStretchLastSection(True)
        self._category_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.update()

        self._central_layout = QVBoxLayout()
        self._central_layout.addWidget(self._category_combobox)
        self._central_layout.addWidget(self._category_table)
        self.setLayout(self._central_layout)
    
    def update(self):
        current_category_text = self._category_combobox.currentText()

        category_names = [c.get_name() for c in self._category_manager.get_all()]
        self._category_combobox.clear()
        self._category_combobox.addItem('-- Select Category --')
        self._category_combobox.addItems(category_names)
        self._category_combobox.setCurrentText(current_category_text)

        self.update_table()

    def update_table(self):
        current_category_text = self._category_combobox.currentText()

        if current_category_text and current_category_text != '-- Select Category --':
            category = self._category_manager.get_category(current_category_text)
            wallet = category.get_wallet()
            self._category_table.setRowCount(len(wallet) + 1)

            for i, transaction in enumerate(wallet):
                amount = transaction['amount']
                description = transaction['description']

                widget = QTableWidgetItem()
                widget.setText(description)
                self._category_table.setItem(i, 1, widget)
                widget = QTableWidgetItem()
                widget.setText(f'${amount:,.2f}')
                self._category_table.setItem(i, 0, widget)
            
            # Show the total balance at the bottom, highlighted green
            widget = QTableWidgetItem()
            widget.setText('Total Balance')
            widget.setBackground(QColor(200, 255, 200))
            self._category_table.setItem(len(wallet), 1, widget)
            widget = QTableWidgetItem()
            widget.setText(f'${category.get_balance():,.2f}')
            widget.setBackground(QColor(200, 255, 200))
            self._category_table.setItem(len(wallet), 0, widget)


        else:
            self._category_table.clear()
            self._category_table.setRowCount(0)

        self._category_table.setHorizontalHeaderLabels(('Amount', 'Description'))
