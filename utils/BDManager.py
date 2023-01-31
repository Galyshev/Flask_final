import sqlite3

class DBManager():

    def __enter__(self):
        self.conn = sqlite3.connect('../BD/db_currency.db')
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()

    def get_data_from_DB(self, query):
        tmp = self.cursor.execute(query)
        result = tmp.fetchone()
        return result

    def into_to_BD(self, query):
        self.cursor.execute(query)
        self.conn.commit()


def query_to_db(bank, date, currency):
    """
    возвращает значения валюты по ключевым параметрам из базы данных
    :param bank:
    :param date:
    :param currency:
    :return: [buy_value, sell_value]
    """
    with DBManager() as db:
        sql = f'select buy_value, sell_value from curr_history where bank = "{bank}" and date = "{date}" and currency = "{currency}";'
        buy_value, sell_value = db.get_data_from_DB(sql)
        rez = [buy_value, sell_value]
        return rez

def insert_data_manual(data):
    with DBManager() as db:
        for dict in data:
            bank = dict['bank']
            date = dict['date']
            currency = dict['currency']
            buy_value = dict['buy_value']
            sell_value = dict['sell_value']
            sql = f'insert into curr_history values(NULL, "{bank}", "{date}", "{currency}", "{buy_value}", "{sell_value}");'
            db.into_to_BD(sql)

# ДЛЯ ТЕСТОВ
if __name__ == "__main__":

    # значения одинаковые, измененния в дате, для проверки записи в базу данных
    currency_bd_tmp = [
        {'bank': 'NBU', 'date': '2022-11-29', 'currency': 'UAH', 'buy_value': 0.025, 'sell_value': 0.022},
        {'bank': 'NBU', 'date': '2022-11-29', 'currency': 'EUR', 'buy_value': 0.9, 'sell_value': 0.9},
        {'bank': 'NBU', 'date': '2022-11-29', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'NBU', 'date': '2022-11-29', 'currency': 'GPB', 'buy_value': 1.1, 'sell_value': 1.2},

        {'bank': 'Privatbank', 'date': '2022-11-29', 'currency': 'UAH', 'buy_value': 0.026, 'sell_value': 0.023},
        {'bank': 'Privatbank', 'date': '2022-11-29', 'currency': 'EUR', 'buy_value': 0.91, 'sell_value': 0.96},
        {'bank': 'Privatbank', 'date': '2022-11-29', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'Privatbank', 'date': '2022-11-29', 'currency': 'GPB', 'buy_value': 1.11, 'sell_value': 1.21},

        {'bank': 'Monobank', 'date': '2022-11-29', 'currency': 'UAH', 'buy_value': 0.027, 'sell_value': 0.024},
        {'bank': 'Monobank', 'date': '2022-11-29', 'currency': 'EUR', 'buy_value': 0.92, 'sell_value': 0.97},
        {'bank': 'Monobank', 'date': '2022-11-29', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'Monobank', 'date': '2022-11-29', 'currency': 'GPB', 'buy_value': 1.12, 'sell_value': 1.22},
    ]

    insert_data_manual(currency_bd_tmp)