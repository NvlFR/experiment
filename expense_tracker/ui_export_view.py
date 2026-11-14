"""UI module for export view."""

from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton


class ExportView(QWidget):
    """Widget for exporting transactions to CSV."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the export view UI."""
        layout = QVBoxLayout(self)
        
        # Export button
        export_btn = QPushButton("Export to CSV")
        export_btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)
    
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
