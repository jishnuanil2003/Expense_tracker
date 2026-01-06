import datetime

from Backend import db_helper as db

def test_create_expense():
    expense = db.create_expense('2026-02-03',250,'Transportation','filled petrol')
    assert expense['expense_date'] == '2026-02-03'
    assert expense['amount']== 250
    assert expense['category'] == 'Transportation'

def test_retrieve_expense_by_date():
    expense = db.retrieve_expense_by_date('2024-09-30')
    assert len(expense) > 0
    assert expense[0]['expense_date'] == datetime.date(2024, 9, 30)