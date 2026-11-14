"""Database module for Expense Tracker application."""

import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional

DATABASE_PATH = "transactions.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """Context manager for getting a database cursor with automatic commit/rollback."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()


def init_database() -> None:
    """Initialize the database with required tables."""
    with get_db_cursor() as cursor:
        # Income categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Expense categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                type INTEGER NOT NULL,  -- 1 for income, -1 for expense
                description TEXT,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
        
        # Insert default income categories
        cursor.executemany("INSERT OR IGNORE INTO income_categories (name) VALUES (?)",
                          [(cat,) for cat in ["Salary", "Freelance", "Investment", "Gift", "Other"]])
        
        # Insert default expense categories
        cursor.executemany("INSERT OR IGNORE INTO expense_categories (name) VALUES (?)",
                          [(cat,) for cat in ["Food & Beverage", "Transportation", "Utilities", 
                                           "Entertainment", "Shopping", "Healthcare", "Education", "Travel", "Other"]])


def get_income_categories() -> list:
    """Get all income categories."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM income_categories")
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categories


def get_expense_categories() -> list:
    """Get all expense categories."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM expense_categories")
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categories


def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    income_only: bool = False,
    expense_only: bool = False,
    category_id: Optional[int] = None,
    order_by: str = "date DESC"
) -> list:
    """Get transactions with optional filtering."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if income_only:
        query += " AND type = 1"
    elif expense_only:
        query += " AND type = -1"
    if category_id:
        query += " AND category_id = ?"
        params.append(category_id)
    
    cursor.execute(query, params)
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Sort transactions by date DESC
    transactions.sort(key=lambda x: x["date"], reverse=True)
    return transactions


def add_transaction(
    date: str,
    amount: float,
    category_id: int,
    transaction_type: int,
    description: Optional[str] = None
) -> bool:
    """Add a new transaction."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO transactions (date, amount, category_id, type, description) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category_id, transaction_type, description or "")
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error adding transaction: {e}")
        return False
    finally:
        conn.close()


def update_transaction(
    transaction_id: int,
    date: Optional[str] = None,
    amount: Optional[float] = None,
    category_id: Optional[int] = None,
    description: Optional[str] = None
) -> bool:
    """Update an existing transaction."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "UPDATE transactions SET date=?, amount=?, category_id=?"
    params = [date, amount, category_id]
    
    if description is not None:
        query += ", description=?"
        params.append(description)
    
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error updating transaction: {e}")
        return False
    finally:
        conn.close()


def delete_transaction(transaction_id: int) -> bool:
    """Delete a transaction by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error deleting transaction: {e}")
        return False
    finally:
        conn.close()


def get_transaction_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """Get financial statistics including total income, total expenses, and balance."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total income
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) as total_income
        FROM transactions
        WHERE type = 1
        {%if start_date}AND date >= ?{%endif}{%if end_date}AND date <= ?{%endif}
    """, [start_date, end_date] if (start_date or end_date) else [])
    
    total_income = cursor.fetchone()[0]
    
    # Total expenses
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) as total_expenses
        FROM transactions
        WHERE type = -1
        {%if start_date}AND date >= ?{%endif}{%if end_date}AND date <= ?{%endif}
    """, [start_date, end_date] if (start_date or end_date) else [])
    
    total_expenses = cursor.fetchone()[0]
    
    # Current balance
    balance = total_income - total_expenses
    
    conn.close()
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    }


def get_transaction_categories(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """Get income and expense categories with their totals."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Income categories
    cursor.execute("""
        SELECT ic.id, ic.name, COALESCE(SUM(t.amount), 0) as total
        FROM income_categories ic
        LEFT JOIN transactions t ON ic.id = t.category_id AND t.type = 1
        {%if start_date}AND t.date >= ?{%endif}{%if end_date}AND t.date <= ?{%endif}
        GROUP BY ic.id, ic.name
    """, [start_date, end_date] if (start_date or end_date) else [])
    
    income_categories = {dict(row): row["total"] for row in cursor.fetchall()}
    
    # Expense categories
    cursor.execute("""
        SELECT ec.id, ec.name, COALESCE(SUM(t.amount), 0) as total
        FROM expense_categories ec
        LEFT JOIN transactions t ON ec.id = t.category_id AND t.type = -1
        {%if start_date}AND t.date >= ?{%endif}{%if end_date}AND date <= ?{%endif}
        GROUP BY ec.id, ec.name
    """, [start_date, end_date] if (start_date or end_date) else [])
    
    expense_categories = {dict(row): row["total"] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        "income": income_categories,
        "expenses": expense_categories
    }


def export_transactions_to_csv(
    filename: str = "transactions_export.csv",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> bool:
    """Export transactions to CSV file."""
    import csv
    
    transactions = get_transactions(start_date=start_date, end_date=end_date)
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'date', 'amount', 'category_name', 'type', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for transaction in transactions:
                row = {
                    'id': transaction['id'],
                    'date': transaction['date'],
                    'amount': transaction['amount'],
                    'category_name': get_category_name(transaction['category_id'], transaction['type']),
                    'type': transaction['type'],
                    'description': transaction['description']
                }
                writer.writerow(row)
        return True
    except IOError as e:
        print(f"Error exporting to CSV: {e}")
        return False


def get_category_name(category_id: int, transaction_type: int) -> str:
    """Get category name based on transaction type."""
    if transaction_type == 1:
        return get_income_categories()[category_id]['name']
    else:
        return get_expense_categories()[category_id]['name']


def get_transactions_by_category(
    category_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> list:
    """Get transactions by category."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM transactions WHERE category_id=? AND 1=1"
    params = [category_id]
    
    if start_date:
        query += " AND date>=?"
        params.append(start_date)
    if end_date:
        query += " AND date<=?"
        params.append(end_date)
    
    cursor.execute(query, params)
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return transactions


def add_income_category(name: str) -> bool:
    """Add a new income category."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO income_categories (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error adding income category: {e}")
        return False
    finally:
        conn.close()


def add_expense_category(name: str) -> bool:
    """Add a new expense category."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO expense_categories (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error adding expense category: {e}")
        return False
    finally:
        conn.close()


def get_transactions_by_month(year: int, month: int) -> list:
    """Get transactions by year and month."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT date, amount, category_id, type
        FROM transactions
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ORDER BY date DESC
    """
    cursor.execute(query, (year, month))
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return transactions
