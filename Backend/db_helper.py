import mysql.connector
from contextlib import contextmanager
from logger import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def set_connection(commit = False):
    connection = mysql.connector.connect(
        host='localhost',
        user = 'root',
        password = 'jishnuanil',
        database = 'expense_manager'
    )
    if connection.is_connected():
        print("Connection successfull")
    else:
        print("connection unsuccessfull")

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def create_expense(expense_date,amount,category,notes):
    logger.info(
        f"create_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with set_connection(commit=True) as cursor:
         cursor.execute('INSERT INTO expense_manager.expenses(expense_date,amount,category,notes) VALUES(%s,%s,%s,%s)',(expense_date,amount,category,notes))
    return {
        "expense_date": expense_date,
        "amount": amount,
        "category": category,
        "note": notes
    }

def retrieve_expense():
    with set_connection(commit=False) as cursor:
        cursor.execute('SELECT * FROM expense_manager.expenses')
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def retrieve_expense_by_date(expense_date):
    logger.info(f"retrieve_expenses_by_date called with {expense_date}")
    with set_connection(commit=False) as cursor:
        cursor.execute('SELECT * FROM expense_manager.expenses WHERE expense_date=%s',(expense_date,))
        return cursor.fetchall()


def delete_expense(expense_date):
    with set_connection(commit=True) as cursor:
        logger.info(f"delete_expenses called with {expense_date}")
        cursor.execute('DELETE FROM expense_manager.expenses WHERE expense_date=%s',(expense_date,))

def fetch_expense_summary(start_date,end_date):
    if end_date < start_date:
        return "End date must be after start date "
    else:
        with set_connection(commit=False) as cursor:
            logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
            cursor.execute('SELECT category,SUM(amount) as total FROM expense_manager.expenses WHERE expense_date BETWEEN %s and %s GROUP BY category', (start_date,end_date))
            expenses = cursor.fetchall()
            return expenses
def fetch_expense_summary_month():
    with set_connection(commit=False) as cursor:
        logger.info("fetch_expense_summary_month called to fetch expense of all months")
        cursor.execute(
            '''SELECT
    YEAR(expense_date) AS year,
    MONTH(expense_date) AS expense_month,
    MONTHNAME(expense_date) AS month_name,
    SUM(amount) AS total
    FROM expenses
    GROUP BY year, expense_month, month_name
    ORDER BY year, expense_month;
            ''')
        expenses = cursor.fetchall()
        return expenses
if __name__ == '__main__':
    # create_expense('2026-01-04','900','Gym','Gym Fees')
    # retrieve_expense()
    fetch_expense_summary('2024-08-01','2025-01-01')