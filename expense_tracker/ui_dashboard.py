"""UI module for dashboard."""

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout)


class DashboardWidget(QWidget):
    """Widget for displaying dashboard statistics and charts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dashboard UI."""
        layout = QVBoxLayout(self)
        
        # Statistics cards
        income_label = QLabel("Total Income:")
        income_label.setStyleSheet("font-weight: bold; color: #4caf50;")
        layout.addWidget(income_label)
        
        expense_label = QLabel("Total Expenses:")
        expense_label.setStyleSheet("font-weight: bold; color: #f44336;")
        layout.addWidget(expense_label)
        
        balance_label = QLabel("Current Balance:")
        balance_label.setStyleSheet("font-weight: bold; color: #2196f3;")
        layout.addWidget(balance_label)
        
        # Add more cards for category breakdown
        category_income_label = QLabel("Income by Category:")
        category_income_label.setStyleSheet("font-weight: bold; color: #4caf50;")
        layout.addWidget(category_income_label)
        
        category_expense_label = QLabel("Expenses by Category:")
        category_expense_label.setStyleSheet("font-weight: bold; color: #f44336;")
        layout.addWidget(category_expense_label)
