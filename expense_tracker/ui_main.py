"""Main UI module for Expense Tracker application."""

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QStackedWidget, QSplitter, QLabel)
from datetime import datetime


class MainWindow(QMainWindow):
    """Main window for the Expense Tracker application."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main window UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with stack
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Expense Tracker")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        main_layout.addWidget(title_label)
        
        # Create stacked widget for different views
        self.stack = QStackedWidget()
        
        # Dashboard view
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.addWidget(QLabel("Dashboard - Income & Expenses"))
        self.stack.addWidget(dashboard_widget)
        
        # Add more widgets for different views
        categories_widget = self._create_categories_view()
        transactions_widget = self._create_transactions_view()
        filters_widget = self._create_filters_view()
        export_widget = self._create_export_view()
        
        self.stack.addWidget(categories_widget)
        self.stack.addWidget(transactions_widget)
        self.stack.addWidget(filters_widget)
        self.stack.addWidget(export_widget)
        
        main_layout.addWidget(self.stack)
        
        # Add help button
        help_btn = QPushButton("Help")
        help_btn.setStyleSheet("background-color: #4a90d9; color: white; font-weight: bold;")
        help_btn.clicked.connect(self.show_help)
        main_layout.addWidget(help_btn)
    
    def _create_categories_view(self):
        """Create categories view widget."""
        from ui_categories import CategoryManager
        
        categories_widget = CategoryManager()
        return categories_widget
    
    def _create_transactions_view(self):
        """Create transactions view widget."""
        from ui_transactions import TransactionTable
        
        transactions_widget = TransactionTable(transactions=[])
        return transactions_widget
    
    def _create_filters_view(self):
        """Create filters view widget."""
        from ui_filters import TransactionFilters
        
        filters_widget = TransactionFilters()
        return filters_widget
    
    def _create_export_view(self):
        """Create export view widget."""
        from ui_export import ExportWidget
        
        export_widget = ExportWidget()
        return export_widget
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
        📋 Expense Tracker - Help
        
        Features:
        1. Track your income and expenses
        2. Add, edit, and delete transactions
        3. Categorize your transactions
        4. Generate reports and statistics
        5. Export data to CSV
        
        Tips:
        - Use descriptive category names for better organization
        - Regularly review your transactions
        - Adjust your budget based on spending patterns
        
        For more information, check the README.md file.
        """
        
        from PySide6.QtWidgets import QMessageBox
        
        QMessageBox.information(self, "Help", help_text)


class Application(QWidget):
    """Application class for Expense Tracker."""
    
    def __init__(self):
        super().__init__()
        # QApplication is created in main block
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Initialize database
        from database import init_database
        
        try:
            init_database()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(['--platform', 'offscreen'])
    app.exec()
