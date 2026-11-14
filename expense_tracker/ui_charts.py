"""UI module for transaction charts."""

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QWidget, QPushButton)


class TransactionChartsWidget(QWidget):
    """Widget for displaying transaction charts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the charts UI."""
        layout = QVBoxLayout(self)
        
        # Income chart placeholder
        income_chart_label = QLabel("Income Chart")
        income_chart_label.setStyleSheet("font-size: 16px; color: #4caf50;")
        layout.addWidget(income_chart_label)
        
        # Expense chart placeholder
        expense_chart_label = QLabel("Expense Chart")
        expense_chart_label.setStyleSheet("font-size: 16px; color: #f44336;")
        layout.addWidget(expense_chart_label)
