import mysql.connector
from contextlib import contextmanager
from log_setup import get_logger

logger=get_logger('database')

@contextmanager
def get_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager'
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_data_by_date(date):
    logger.info(f'fetch_data_by_date called with {date}')
    with get_cursor() as cursor:
        cursor.execute('select * from expenses where expense_date = %s',(date,))
        data=cursor.fetchall()
        return data

def insert_data(expense_date,amount,category,notes):
    logger.info(f'insert_data called with {expense_date},{amount},{category},{notes}')
    with get_cursor(commit=True) as cursor:
        cursor.execute('insert into expenses(expense_date,amount,category,notes) '
                       'values(%s, %s, %s, %s)',(expense_date,amount,category,notes))

def delete_data(expense_date):
    logger.info(f'delete_data called with {expense_date}')
    with get_cursor(commit=True) as cursor:
        cursor.execute('delete from expenses where expense_date=%s',(expense_date,))

def fetch_summary(start_date,end_date):
    logger.info(f'fetch_summary called with start date:{start_date},end date:{end_date}')
    with get_cursor() as cursor:
        cursor.execute('select category,sum(amount) as total from expenses where expense_date between %s and %s group by category',(start_date,end_date))
        data = cursor.fetchall()
        return data

def fetch_month_summary():
    logger.info(f'fetch_month_summary called')
    with get_cursor() as cursor:
        cursor.execute('SELECT month(expense_date) as month_number, monthname(expense_date) as month_name,sum(amount) as total FROM expenses group by month_number,month_name order by month_number')
        data = cursor.fetchall()
        return data


if __name__=='__main__':
    # insert_data('2025-05-20',500,'shopping','Flip flops')
    # summary = fetch_summary('2024-08-1','2024-08-2')
    # for d in summary:
    #     print(d)
    a=fetch_data_by_date('2024-08-1')
    print(len(a))
    print(__file__)
