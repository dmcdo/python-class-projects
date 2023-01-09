from PyQt5.QtWidgets import *

class DialogAddRevenueOrExpense(QDialog):
    def __init__(self, category_manager, is_revenue=True, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self._category_manager = category_manager
        self._is_revenue = is_revenue
        self.setWindowTitle('Add Revenue' if is_revenue else 'Add Expense')

        category_names = [c.get_name() for c in self._category_manager.get_all()]
        self._category_combobox = QComboBox()
        self._category_combobox.addItem('-- Select Category --')
        self._category_combobox.addItems(category_names)

        self._amount_edit = QLineEdit()
        self._amount_label = QLabel('Amount $')
        self._amount_layout = QHBoxLayout()
        self._amount_layout.addWidget(self._amount_label)
        self._amount_layout.addWidget(self._amount_edit)
        self._amount_widget = QWidget()
        self._amount_widget.setLayout(self._amount_layout)

        self._description_edit = QLineEdit()
        self._description_label = QLabel('Desctiption')
        self._description_layout = QHBoxLayout()
        self._description_layout.addWidget(self._description_label)
        self._description_layout.addWidget(self._description_edit)
        self._description_widget = QWidget()
        self._description_widget.setLayout(self._description_layout)

        self.exit_button = QPushButton('Exit')
        self._ok_button = QPushButton('OK')
        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self.exit_button)
        self._buttons_layout.addWidget(self._ok_button)
        self._buttons_widget = QWidget()
        self._buttons_widget.setLayout(self._buttons_layout)
        self._ok_button.clicked.connect(self.ok_button_pressed)
        self.exit_button.clicked.connect(self.close)

        self._central_layout = QVBoxLayout()
        self._central_layout.addWidget(self._category_combobox)
        self._central_layout.addWidget(self._amount_widget)
        self._central_layout.addWidget(self._description_widget)
        self._central_layout.addWidget(self._buttons_widget)
    
        self.setLayout(self._central_layout)
        self._category_combobox.setFocus()
    
    def ok_button_pressed(self):
        name = self._category_combobox.currentText()
        desc = self._description_edit.text().strip()

        if name == '-- Select Category --': # No category selected
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Please select a category.')
            msg.setWindowTitle('No Category Selected')
            msg.exec_()
            return

        # convert amount string to float
        try:
            amount = float(self._amount_edit.text().replace(',', ''))
            amount_text_invalid = False
        except ValueError:
            amount = 0.0
            amount_text_invalid = True

        if amount_text_invalid or amount <= 0:
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f'Invalid amount ${amount:.2f}.')
            msg.setWindowTitle('Invlid Amount')
            msg.exec_()
        elif self._is_revenue: # Add revenue
            category = self._category_manager.get_category(name)
            category.add_revenue(amount, desc)
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Information)
            msg.setText(f'${amount:.2f} added to {name}.')
            msg.setWindowTitle('Success!')
            msg.exec_()
            self.close()
        else: # Add expense
            category = self._category_manager.get_category(name)
            success = category.add_expense(amount, desc)
            if success:
                msg = QMessageBox(parent=self)
                msg.setIcon(QMessageBox.Information)
                msg.setText(f'${amount:.2f} removed from {name}.')
                msg.setWindowTitle('Success!')
                msg.exec_()
                self.close()
            else:
                msg = QMessageBox(parent=self)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f'Insufficient funds available in {name}.')
                msg.setWindowTitle('Insufficient Funds')
                msg.exec_()