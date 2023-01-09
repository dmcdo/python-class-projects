from PyQt5.QtWidgets import *

class DialogTransferMoney(QDialog):
    def __init__(self, category_manager, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self._category_manager = category_manager
        self.setWindowTitle('Transfer Money')

        category_names = [c.get_name() for c in self._category_manager.get_all()]
        self._transfer_from_label = QLabel('Transfer from:')
        self._transfer_to_label = QLabel('Transfer to:')
        self._transfer_from_combobox = QComboBox()
        self._transfer_to_combobox = QComboBox()
        self._transfer_from_combobox.addItem('-- Select Category --')
        self._transfer_to_combobox.addItem('-- Select Category --')
        self._transfer_from_combobox.addItems(category_names)
        self._transfer_to_combobox.addItems(category_names)
        
        self._amount_edit = QLineEdit()
        self._amount_label = QLabel('Amount $')
        self._amount_layout = QHBoxLayout()
        self._amount_layout.addWidget(self._amount_label)
        self._amount_layout.addWidget(self._amount_edit)
        self._amount_widget = QWidget()
        self._amount_widget.setLayout(self._amount_layout)

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
        self._central_layout.addWidget(self._transfer_from_label)
        self._central_layout.addWidget(self._transfer_from_combobox)
        self._central_layout.addWidget(self._transfer_to_label)
        self._central_layout.addWidget(self._transfer_to_combobox)
        self._central_layout.addWidget(self._amount_widget)
        self._central_layout.addWidget(self._buttons_widget)
        self.setLayout(self._central_layout)

    def ok_button_pressed(self):
        from_name = self._transfer_from_combobox.currentText()
        to_name = self._transfer_to_combobox.currentText()

        if from_name == '-- Select Category --': # no category selected
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Please select a category to transfer money from.')
            msg.setWindowTitle('Invalid Category Selection')
            msg.exec_()
            return
        if to_name == '-- Select Category --': # no category selected
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Please select a category to transfer money to.')
            msg.setWindowTitle('Invalid Category Selection')
            msg.exec_()
            return
        if from_name == to_name: # same category selected twice
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Please select two distinct categories.')
            msg.setWindowTitle('Invalid Category Selection')
            msg.exec_()
            return

        # get amount to transfer
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
            return

        from_category = self._category_manager.get_category(from_name)
        to_category = self._category_manager.get_category(to_name)

        success = from_category.transfer_money(amount, to_category)
        if success:
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Information)
            msg.setText(f'Successfully transferred ${amount:.2f} '
                        f'from {from_name} to {to_name}.')
            msg.setWindowTitle('Success!')
            msg.exec_()
            self.close()
        else:
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f'Insufficient funds available in {from_name}.')
            msg.setWindowTitle('Insufficient Funds')
            msg.exec_()