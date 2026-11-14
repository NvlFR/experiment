"""UI module for transactions view."""

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QWidget,
                               QFileDialog, QMessageBox)


class TransactionsView(QWidget):
    """Widget for displaying and managing transactions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the transactions view UI."""
        layout = QVBoxLayout(self)
        
        # Add transaction button
        add_btn = QPushButton("Add New Transaction")
        add_btn.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
        add_btn.clicked.connect(self.add_transaction)
        layout.addWidget(add_btn)
        
        # Export button
        export_btn = QPushButton("Export to CSV")
        export_btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)
    
    def add_transaction(self):
        """Add a new transaction."""
        from ui_transactions import TransactionForm
        
        form = TransactionForm(transaction_data={})
        form.show()
    
    def export_csv(self):
        """Export transactions to CSV file."""
        from database import export_transactions_to_csv
        
        filename, _ = QFileDialog.getSaveFileName(self, "Export Transactions to CSV", "transactions_export.csv", "CSV Files (*.csv)")
        
        if filename:
            success = export_transactions_to_csv(filename)
            
            if success:
                QMessageBox.information(self, "Success", f"Transactions exported successfully to {filename}!")
            else:
                QMessageBox.critical(self, "Error", "Failed to export transactions.")
