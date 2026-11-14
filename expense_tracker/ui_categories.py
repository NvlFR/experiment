"""UI module for categories management."""

from PySide6.QtWidgets import (QComboBox, QFormLayout, QLabel, QPushButton,
                               QLineEdit, QMessageBox, QWidget)


class CategoryManager(QWidget):
    """Widget for managing income and expense categories."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the category manager UI."""
        self.layout = QVBoxLayout(self)
        
        # Income categories section
        income_label = QLabel("Income Categories:")
        income_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(income_label)
        
        self.income_categories = QComboBox()
        self.income_categories.addItems(["Salary", "Freelance", "Investment", "Gift", "Other"])
        self.income_categories.currentIndexChanged.connect(self.on_income_category_changed)
        self.layout.addWidget(self.income_categories)
        
        # Expense categories section
        expense_label = QLabel("Expense Categories:")
        expense_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(expense_label)
        
        self.expense_categories = QComboBox()
        self.expense_categories.addItems(["Food & Beverage", "Transportation", "Utilities", 
                                         "Entertainment", "Shopping", "Healthcare", "Education", "Travel", "Other"])
        self.expense_categories.currentIndexChanged.connect(self.on_expense_category_changed)
        self.layout.addWidget(self.expense_categories)
        
        # Add new category buttons
        add_income_btn = QPushButton("Add New Income Category")
        add_income_btn.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
        add_income_btn.clicked.connect(self.add_income_category)
        self.layout.addWidget(add_income_btn)
        
        add_expense_btn = QPushButton("Add New Expense Category")
        add_expense_btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        add_expense_btn.clicked.connect(self.add_expense_category)
        self.layout.addWidget(add_expense_btn)
    
    def on_income_category_changed(self, index):
        """Handle income category selection change."""
        pass
    
    def on_expense_category_changed(self, index):
        """Handle expense category selection change."""
        pass
    
    def add_income_category(self):
        """Add a new income category."""
        name = self.income_categories.currentText()
        if name == "Add New Income Category":
            QMessageBox.warning(self, "Warning", "Please select an existing category first.")
            return
        
        # Get category ID from database
        from database import get_income_categories
        categories = get_income_categories()
        
        if name in [cat['name'] for cat in categories]:
            QMessageBox.warning(self, "Warning", f"Category '{name}' already exists.")
            return
        
        # Create new category entry
        new_category = {"id": len(categories) + 1, "name": name}
        self.income_categories.insertItem(name)
    
    def add_expense_category(self):
        """Add a new expense category."""
        name = self.expense_categories.currentText()
        if name == "Add New Expense Category":
            QMessageBox.warning(self, "Warning", "Please select an existing category first.")
            return
        
        # Get category ID from database
        from database import get_expense_categories
        categories = get_expense_categories()
        
        if name in [cat['name'] for cat in categories]:
            QMessageBox.warning(self, "Warning", f"Category '{name}' already exists.")
            return
        
        # Create new category entry
        new_category = {"id": len(categories) + 1, "name": name}
        self.expense_categories.insertItem(name)
