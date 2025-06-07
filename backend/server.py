from fastapi import FastAPI,HTTPException
from datetime import date
import database
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount:float
    category:str
    notes:str

class Datevalid(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()

@app.get('/expenses/{expense_date}',response_model=List[Expense])
def get_expenses(expense_date : date):
    expenses = database.fetch_data_by_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail='Failed to retrieve data')
    return expenses

@app.post('/expenses/{expense_date}')
def insert_expenses(expense_date : date, expenses:List[Expense]):
    database.delete_data(expense_date)
    for expense in expenses:
        database.insert_data(expense_date,expense.amount,expense.category,expense.notes)
    return f'Data inserted successfully...'

@app.post('/analytics/')
def get_summary(date_range: Datevalid):
    data = database.fetch_summary(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,detail='Failed to retrieve data')

    breakdown={}
    total = sum([row['total'] for row in data])
    for row in data:
        percentage = (row['total']/total)*100
        breakdown[row['category']]={
            'total':row['total'],
            'percentage':percentage
        }

    return breakdown

@app.get('/month_analytics/')
def get_analytics_month():
    expenses = database.fetch_month_summary()
    if expenses is None:
        raise HTTPException(status_code=500, detail='Failed to retrieve data')
    return expenses