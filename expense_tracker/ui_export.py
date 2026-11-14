"""UI module for CSV export."""

from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton


class ExportWidget(QWidget):
    """Widget for exporting transactions to CSV."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the export UI."""
        layout = QVBoxLayout(self)
        
        # Export button
        export_btn = QPushButton("Export to CSV")
        export_btn.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)
