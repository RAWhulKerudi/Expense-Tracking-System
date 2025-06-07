from backend import database

def test_fetch_data_by_date():
    expenses = database.fetch_data_by_date('2025-05-20')

    assert len(expenses)==1
    assert expenses[0]['amount']==500
    assert expenses[0]['category']=='shopping'
    assert expenses[0]['notes']=='Flip flops'


def test_fetch_data_invalid():
    expenses = database.fetch_data_by_date('1500-05-20')

    assert len(expenses)==0
