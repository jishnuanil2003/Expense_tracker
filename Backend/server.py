from fastapi import FastAPI,HTTPException
import db_helper as db
from datetime import date
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Expense(BaseModel):
    amount:float
    category:str
    notes:str

class DateRange(BaseModel):
    start_date:date
    end_date:date

@app.get('/expense/{expense_date}', response_model=List[Expense])
def get_expense(expense_date:date):
    expense = db.retrieve_expense_by_date(expense_date)
    print(f"Received request{expense_date}")
    return expense
@app.post('/expense/{expense_date}')
def add_or_edit_expense(expense_date:date,expenses: List[Expense]):
    for expense in expenses:
        db.create_expense(expense_date,expense.amount,expense.category,expense.notes)
    return {'message':'Data added successfully'}
@app.delete('/expense/{expense_date}')
def delete_expense(expense_date:date):
    db.delete_expense(expense_date)
    return {'message':'Data deleted successfully'}
@app.post('/analytics')
def get_expense_summary(date_range:DateRange):
    data = db.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,detail="Failed to load analytics")
    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total !=0 else 0
        breakdown[row['category']]={
            'total':row['total'],
            'percentage':percentage
        }
    return breakdown

@app.get('/analytics/month')
def get_expense_summary_month():
    data = db.fetch_expense_summary_month()
    if data is None:
        raise HTTPException(status_code=500,detail="Failed to load analytics")

    return data