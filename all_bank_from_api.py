import datetime
from BD import Model_db
from BD.alchemy import engine
from sqlalchemy.orm import Session
import requests


def PrivatBank(date_privat, db_date):
    req = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_privat}')
    curr_list = req.json()
    sale_usd = ''
    buy_usd = ''
    for dic in curr_list['exchangeRate']:
        if dic['currency'] == 'USD':
            sale_usd = dic['saleRate']
            buy_usd = dic['purchaseRate']

    # Запись в базу по гривне
    bank = 'Privatbank'
    date = db_date
    currency = 'UAH'
    buy_value = 1/buy_usd
    sell_value = 1/sale_usd

    with Session(engine) as session:
        insert_query = Model_db.Currency(bank=bank, date=date, currency=currency,
                                         buy_value=buy_value, sell_value=sell_value)
        session.add(insert_query)
        session.commit()

    for dic in curr_list['exchangeRate']:
        if dic['currency'] in ('EUR', 'GBP', 'USD'):
            currency = dic['currency']
            sale_cur = dic['saleRate'] / sale_usd
            buy_cur = dic['purchaseRate'] / buy_usd
            # запись для выбранной валлюты
            with Session(engine) as session:
                insert_query = Model_db.Currency(bank=bank, date=date, currency=currency,
                                                 buy_value=buy_cur, sell_value=sale_cur)
                session.add(insert_query)
                session.commit()

def NBU(date_privat, db_date):
    req = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_privat}')
    curr_list = req.json()
    sale_usd = ''
    buy_usd = ''
    for dic in curr_list['exchangeRate']:
        if dic['currency'] == 'USD':
            sale_usd = dic['saleRateNB']
            buy_usd = dic['purchaseRateNB']

    # Запись в базу по гривне
    bank = 'NBU'
    date = db_date
    currency = 'UAH'
    buy_value = 1/buy_usd
    sell_value = 1/sale_usd

    with Session(engine) as session:
        insert_query = Model_db.Currency(bank=bank, date=date, currency=currency,
                                         buy_value=buy_value, sell_value=sell_value)
        session.add(insert_query)
        session.commit()

    for dic in curr_list['exchangeRate']:
        if dic['currency'] in ('EUR', 'GBP', 'USD'):
            currency = dic['currency']
            sale_cur = dic['saleRateNB'] / sale_usd
            buy_cur = dic['purchaseRateNB'] / buy_usd
            # запись для выбранной валлюты
            with Session(engine) as session:
                insert_query = Model_db.Currency(bank=bank, date=date, currency=currency,
                                                 buy_value=buy_cur, sell_value=sale_cur)
                session.add(insert_query)
                session.commit()
def Monobank():
    req = requests.get('https://api.monobank.ua/bank/currency')
    curr_list = req.json()
    sale_usd = ''
    buy_usd = ''
    # дата по умолчанию - сегодня
    db_date = datetime.datetime.now().strftime("%Y-%m-%d")
    for dic in curr_list:
        if dic['currencyCodeA'] == 840 and dic['currencyCodeB'] == 980:
            sale_usd = dic['rateSell']
            buy_usd = dic['rateBuy']
            # дата записи курса валют по банку
            unix_time = dic['date']
            db_date = datetime.datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")

    # Запись в базу по гривне
    bank = 'Monobank'
    currency = 'UAH'
    buy_value = 1/buy_usd
    sell_value = 1/sale_usd

    with Session(engine) as session:
        insert_query = Model_db.Currency(bank=bank, date=db_date, currency=currency,
                                         buy_value=buy_value, sell_value=sell_value)
        session.add(insert_query)
        session.commit()

    for dic in curr_list:
        if dic['currencyCodeA'] in (978, 826, 840) and dic['currencyCodeB'] == 980:
            if dic['currencyCodeA'] == 978:
                currency = 'EUR'
            elif dic['currencyCodeA'] == 826:
                currency = 'GBP'
            else:
                currency = 'USD'

            sale_cur = dic['rateSell'] / sale_usd
            buy_cur = dic['rateBuy'] / buy_usd
            # дата записи курса валют по банку
            unix_time = dic['date']
            db_date = datetime.datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")
            # запись для выбранной валлюты
            with Session(engine) as session:
                insert_query = Model_db.Currency(bank=bank, date=db_date, currency=currency,
                                                 buy_value=buy_cur, sell_value=sale_cur)
                session.add(insert_query)
                session.commit()

