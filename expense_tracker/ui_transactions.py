"""UI module for transaction management."""

from datetime import datetime
from PySide6.QtWidgets import (QDateEdit, QFormLayout, QLabel, QPushButton,
                               QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem,
                               QWidget)


class TransactionForm(QWidget):
    """Widget for adding/editing transactions."""
    
    def __init__(self, parent=None, transaction_data=None):
        super().__init__(parent)
        self.transaction_data = transaction_data or {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the transaction form UI."""
        layout = QFormLayout(self)
        
        # Date field
        date_label = QLabel("Date:")
        layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_edit.setDate(datetime.strptime(today, "%Y-%m-%d").date())
        self.date_edit.setCalendarPopup(True)
        layout.addWidget(self.date_edit)
        
        # Amount field
        amount_label = QLabel("Amount:")
        layout.addWidget(amount_label)
        
        self.amount_edit = QLineEdit()
        self.amount_edit.setText(str(abs(self.transaction_data.get('amount', 0))))
        self.amount_edit.setValidator(self.create_amount_validator())
        layout.addWidget(self.amount_edit)
        
        # Category field
        category_label = QLabel("Category:")
        layout.addWidget(category_label)
        
        self.category_combo = QLineEdit()
        self.category_combo.setText(self.get_category_name())
        self.category_combo.setPlaceholderText("Select a category...")
        layout.addWidget(self.category_combo)
        
        # Type field (Income/Expense)
        type_label = QLabel("Type:")
        layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Income", "Expense"])
        self.type_combo.setCurrentIndex(0 if self.transaction_data.get('type', 1) == 1 else 1)
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        layout.addWidget(self.type_combo)
        
        # Description field
        desc_label = QLabel("Description:")
        layout.addWidget(desc_label)
        
        self.description_edit = QLineEdit()
        self.description_edit.setText(self.transaction_data.get('description', ''))
        layout.addWidget(self.description_edit)
        
        # Add/Edit buttons
        add_btn = QPushButton("Add Transaction")
        add_btn.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
        add_btn.clicked.connect(self.add_transaction)
        layout.addRow(add_btn)
        
        edit_btn = QPushButton("Edit Transaction")
        edit_btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        edit_btn.clicked.connect(self.edit_transaction)
        layout.addRow(edit_btn)
    
    def create_amount_validator(self):
        """Create a validator for the amount field."""
        from PySide6.QtCore import QIntValidator
        return QIntValidator(0, None, self)
    
    def get_category_name(self):
        """Get category name based on transaction type."""
        from database import get_income_categories, get_expense_categories
        
        if self.transaction_data.get('type', 1) == 1:
            categories = get_income_categories()
        else:
            categories = get_expense_categories()
        
        return next((cat['name'] for cat in categories.values()), "")
    
    def on_type_changed(self, index):
        """Handle type change."""
        category_name = self.get_category_name()
        self.category_combo.setText(category_name)
    
    def add_transaction(self):
        """Add a new transaction."""
        date = self.date_edit.date().toString("%Y-%m-%d")
        amount = self.amount_edit.text()
        
        if not amount or amount <= 0:
            QMessageBox.warning(self, "Error", "Please enter a valid amount.")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid numeric amount.")
            return
        
        category_id = self.category_combo.text()
        if not category_id:
            QMessageBox.warning(self, "Warning", "Please select a category.")
            return
        
        description = self.description_edit.text()
        
        from database import add_transaction
        
        transaction_data = {
            'date': date,
            'amount': amount,
            'category_id': category_id,
            'type': 1 if self.type_combo.currentIndex() == 0 else -1,
            'description': description
        }
        
        success = add_transaction(**transaction_data)
        
        if success:
            QMessageBox.information(self, "Success", "Transaction added successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to add transaction.")


class TransactionTable(QWidget):
    """Widget for displaying transactions."""
    
    def __init__(self, parent=None, transactions=None):
        super().__init__(parent)
        self.transactions = transactions or []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the transaction table UI."""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Date", "Amount", "Category", "Type", "Description"])
        
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for transaction in self.transactions:
            row = [
                QTableWidgetItem(str(transaction['id'])),
                QTableWidgetItem(transaction['date']),
                QTableWidgetItem(f"{'+' if transaction['type'] == 1 else ''}{transaction['amount']}"),
                QTableWidgetItem(self.get_category_name(transaction)),
                QTableWidgetItem("Income" if transaction['type'] == 1 else "Expense"),
                QTableWidgetItem(transaction['description'])
            ]
            table.insertRow(len(table.rowCount()))
            for col, item in enumerate(row):
                table.setItem(len(table.rowCount()) - 1, col, item)
        
        self.table = table
    
    def get_category_name(self, transaction):
        """Get category name based on transaction."""
        from database import get_income_categories, get_expense_categories
        
        if transaction['type'] == 1:
            categories = get_income_categories()
        else:
            categories = get_expense_categories()
        
        return next((cat['name'] for cat in categories.values()), "Unknown")
