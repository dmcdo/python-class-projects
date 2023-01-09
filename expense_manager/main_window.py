from PyQt5.QtWidgets import *
from category_manager import CategoryManager
from widget_managmement_buttons import WidgetMgmtButtons
from widget_display_categories import WidgetDisplayCategories
from widget_display_pie_chart import WidgetDisplayPieChart

class MainWindow(QMainWindow):
    def __init__(self, category_manager=None):
        super(MainWindow, self).__init__()
        self._category_manager = category_manager or CategoryManager()
        self.setGeometry(50, 50, 1050, 600)
        self.setWindowTitle('Expense Report')

        # Window Management Buttons go at top
        self._mgmt_buttons = WidgetMgmtButtons(self._category_manager, self.update_all)

        # Center widget contains the category displayer and pie chat displayer
        self._data_displayer = WidgetDisplayCategories(self._category_manager)
        self._piechart_display = WidgetDisplayPieChart(self._category_manager)
        self._center_layout = QHBoxLayout()
        self._center_layout.addWidget(self._data_displayer)
        self._center_layout.addWidget(self._piechart_display)
        self._center_widget = QWidget()
        self._center_widget.setLayout(self._center_layout)

        # Bottom widget contains just the Quit button
        self._quit_button = QPushButton('Quit')
        self._quit_button.clicked.connect(self.close)
        self._quit_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._bottom_layout = QHBoxLayout()
        self._bottom_layout.addSpacerItem(self._quit_spacer)
        self._bottom_layout.addWidget(self._quit_button)
        self._bottom_widget = QWidget()
        self._bottom_widget.setLayout(self._bottom_layout)

        # Central widget/layout contains everything in the window
        self._central_layout = QVBoxLayout()
        self._central_layout.addWidget(self._mgmt_buttons)
        self._central_layout.addWidget(self._center_widget)
        self._central_layout.addWidget(self._bottom_widget)
        
        self._central_widget = QWidget()
        self._central_widget.setLayout(self._central_layout)
        self.setCentralWidget(self._central_widget)

    def update_all(self):
        self._data_displayer.update()
        self._piechart_display.update()
