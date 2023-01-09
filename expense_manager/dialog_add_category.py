from PyQt5.QtWidgets import *
from category_manager import DuplicateCategoryError

class DialogAddCategory(QDialog):
    def __init__(self, category_manager, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self._category_manager = category_manager
        self.setWindowTitle('Add a Category')

        self._name_edit = QLineEdit('Enter category name')
        self._name_edit.selectAll()
        self._name_edit.setFocus()

        # Buttons widget contains exit and OK buttons
        self._exit_button = QPushButton('Exit')
        self._ok_button = QPushButton('OK')
        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._exit_button)
        self._buttons_layout.addWidget(self._ok_button)
        self._buttons_widget = QWidget()
        self._buttons_widget.setLayout(self._buttons_layout)
        self._ok_button.clicked.connect(self.ok_button_pressed)
        self._exit_button.clicked.connect(self.close)

        self._cental_layout = QVBoxLayout()
        self._cental_layout.addWidget(self._name_edit)
        self._cental_layout.addWidget(self._buttons_widget)
        self.setLayout(self._cental_layout)
    
    def ok_button_pressed(self):
        name = self._name_edit.text().strip()
        if name and '-- Select Category --' not in name: # if valid category name
            try:
                self._category_manager.add_category(name)
                msg = QMessageBox(parent=self)
                msg.setIcon(QMessageBox.Information)
                msg.setText(f'Category "{name}" was successfully created.')
                msg.setWindowTitle('Success!')
                msg.exec_()
                self.close()
            except DuplicateCategoryError:
                msg = QMessageBox(parent=self)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f'A category with the name "{name}" already exists.')
                msg.setWindowTitle('Error Adding Category')
                msg.exec_()
        else:
            msg = QMessageBox(parent=self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Invalid or empty category name.')
            msg.setWindowTitle('Error Adding Category')
            msg.exec_()
        
        self._name_edit.selectAll()
        self._name_edit.setFocus()
