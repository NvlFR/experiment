#!/usr/bin/env python3
"""
Expense Tracker - Main Application Entry Point

This is the main entry point for the Expense Tracker desktop application.
It initializes and starts the PySide6 application window.

Author: Assistant
Date: 2026-11-14
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    """Main application window class."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setMinimumSize(800, 600)


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
