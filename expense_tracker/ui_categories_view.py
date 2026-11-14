"""UI module for categories view."""

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QWidget)


class CategoriesView(QWidget):
    """Widget for displaying and managing categories."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the categories view UI."""
        layout = QVBoxLayout(self)
        
        # Income categories section
        income_label = QLabel("Income Categories:")
        income_label.setStyleSheet("font-weight: bold; color: #4caf50;")
        layout.addWidget(income_label)
        
        self.income_categories = QWidget()
        income_layout = QVBoxLayout(self.income_categories)
        
        for i in range(1, 6):  # Default categories
            category_widget = QWidget()
            cat_layout = QHBoxLayout(category_widget)
            
            cat_name_label = QLabel(f"Category {i}")
            cat_name_label.setStyleSheet("background-color: #4caf50; color: white;")
            cat_delete_btn = QPushButton("Delete")
            cat_delete_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
            cat_delete_btn.clicked.connect(self.delete_income_category, i)
            
            cat_layout.addWidget(cat_name_label)
            cat_layout.addWidget(cat_delete_btn)
            
            income_layout.addWidget(category_widget)
        
        layout.addWidget(self.income_categories)
        
        # Expense categories section
        expense_label = QLabel("Expense Categories:")
        expense_label.setStyleSheet("font-weight: bold; color: #f44336;")
        layout.addWidget(expense_label)
        
        self.expense_categories = QWidget()
        expense_layout = QVBoxLayout(self.expense_categories)
        
        for i in range(1, 10):  # Default categories
            category_widget = QWidget()
            cat_layout = QHBoxLayout(category_widget)
            
            cat_name_label = QLabel(f"Category {i}")
            cat_name_label.setStyleSheet("background-color: #f44336; color: white;")
            cat_delete_btn = QPushButton("Delete")
            cat_delete_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
            cat_delete_btn.clicked.connect(self.delete_expense_category, i)
            
            cat_layout.addWidget(cat_name_label)
            cat_layout.addWidget(cat_delete_btn)
            
            expense_layout.addWidget(category_widget)
        
        layout.addWidget(self.expense_categories)
    
    def delete_income_category(self, index):
        """Delete an income category."""
        from database import get_income_categories
        
        categories = get_income_categories()
        if index in categories:
            del categories[index]
            self.income_categories.layout.removeWidget(self.income_categories.layout.itemAt(index))
    
    def delete_expense_category(self, index):
        """Delete an expense category."""
        from database import get_expense_categories
        
        categories = get_expense_categories()
        if index in categories:
            del categories[index]
            self.expense_categories.layout.removeWidget(self.expense_categories.layout.itemAt(index))
