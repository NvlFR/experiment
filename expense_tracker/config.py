"""Configuration file for Expense Tracker application."""

import os

# Database path
DATABASE_PATH = "transactions.db"

# Default categories
DEFAULT_INCOME_CATEGORIES = ["Salary", "Freelance", "Investment", "Gift", "Other"]
DEFAULT_EXPENSE_CATEGORIES = ["Food & Beverage", "Transportation", "Utilities", "Entertainment", "Shopping", "Healthcare", "Education", "Travel", "Other"]

# Color scheme for dark theme
DARK_THEME_COLORS = {
    "background": "#1e1e1e",
    "card_background": "#2d2d2d",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "accent_color": "#4a90d9",
    "income_color": "#4caf50",
    "expense_color": "#f44336",
    "border_color": "#404040",
}

# Date format for filtering
DATE_FORMAT = "%Y-%m-%d"
