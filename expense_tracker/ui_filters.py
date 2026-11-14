"""UI module for transaction filters."""

from PySide6.QtWidgets import QDateEdit, QComboBox, QLabel


class TransactionFilters(QWidget):
    """Widget for filtering transactions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the filters UI."""
        layout = QVBoxLayout(self)
        
        # Start date filter
        start_date_label = QLabel("Start Date:")
        layout.addWidget(start_date_label)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(self._get_default_start_date())
        layout.addWidget(self.start_date_edit)
        
        # End date filter
        end_date_label = QLabel("End Date:")
        layout.addWidget(end_date_label)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(self._get_default_end_date())
        layout.addWidget(self.end_date_edit)
    
    def _get_default_start_date(self):
        """Get the default start date (current month beginning)."""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        first_day_of_month = today.replace(day=today.day)
        return first_day_of_month.strftime("%Y-%m-%d")
    
    def _get_default_end_date(self):
        """Get the default end date (current month ending)."""
        from datetime import datetime
        
        today = datetime.now()
        last_day_of_month = today.replace(day=today.day + 1) - timedelta(days=1)
        return last_day_of_month.strftime("%Y-%m-%d")
