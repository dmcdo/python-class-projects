import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

class WidgetDisplayPieChart(QWidget):
    def __init__(self, category_manager):
        super(QWidget, self).__init__()
        self._category_manager = category_manager

        self._image = None
        self._image_bytes = None
        self._label = QLabel()
        self._dropdown = QComboBox()
        self._dropdown.addItems(('Spending Percentage',
                                 'Spending Amount',
                                 'Revenue Percentage',
                                 'Revenue Amount',
                                 'Percentage of Total Budget',
                                 'Total Budget'))
        self._dropdown.setCurrentText('Spending Percentage')
        self._dropdown.currentTextChanged.connect(self.update)

        self._central_layout = QVBoxLayout()
        self._central_layout.addWidget(self._dropdown)
        self._central_layout.addWidget(self._label)
        self.setLayout(self._central_layout)

        self.update()
    
    def update(self):
        self.generate_pie_chart()
        self._image = QPixmap()
        self._image.loadFromData(self._image_bytes)
        self._label.setPixmap(self._image)

    def generate_pie_chart(self):
        plt.close()

        # Retrieve the list of categories
        categories = self._category_manager.get_all()
        mode = self._dropdown.currentText()


        # Get relevant pie "slices"
        # Only display slice if relevant to the selected mode
        slices = []
        names = []

        for category in categories:
            total = 0
            if 'Spending' in mode:
                for transaction in category.get_wallet():
                    if transaction['amount'] < 0:
                        total -= transaction['amount']
            elif 'Revenue' in mode:
                for transaction in category.get_wallet():
                    if transaction['amount'] > 0:
                        total += transaction['amount']
            else:
                total = category.get_balance()
            if total > 0:
                slices.append(total)
                names.append(category.get_name())
        
        total = sum(slices)

        # Plot pie chart
        if 'Percent' in mode:
            plt.pie(slices, labels=names, autopct="%1.2f%%", shadow=False, normalize=True)
        else:
            plt.pie(slices,
                    labels=names,
                    autopct=lambda x: f'${total * x * 0.01:,.2f}',
                    shadow=False,
                    normalize=True)
        
        # Save to bytes
        self._image_bytes = BytesIO()
        plt.savefig(self._image_bytes, dpi=100, format='png')
        self._image_bytes.seek(0)
        self._image_bytes = self._image_bytes.read()