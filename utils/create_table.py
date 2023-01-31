import sqlite3

"""
Файл для создания базы данных, создания таблицы и внесения стартовых тестовых данных.
Используется в случае удаления / поврежедения базы данных
"""

# коннектор к базе (если базы данных не существует, она создаeтся)
def connect_db():
    conn = sqlite3.connect('../BD/db_currency.db') #откорректироввать путь, если надо, так как этот файл был перемещен из корня
    return conn

# создание таблицы (используется один раз либо после удаления таблицы при тестах)
def create_table():
    conn = connect_db()
    sql = "create table if not exists curr_history(" \
          "id integer primary key autoincrement," \
          "bank text not null," \
          "date text not null," \
          "currency text not null," \
          "buy_value real not null," \
          "sell_value real not null);"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    finally:
        conn.close()

# внесение данных (ручной режим, для заполнения базы)
def insert_data_manual(data):
    conn = connect_db()
    for dict in data:
        line = (dict['bank'], dict['date'], dict['currency'], dict['buy_value'], dict['sell_value'])
        sql = "insert into curr_history values(NULL, ?, ?, ?, ?, ?)"
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (line))
            conn.commit()
        finally:
            conn.close()

# запрос в БД по ключам "банк", "дата", "код валюты"
def query_to_db(bank, date, currency):
    """
    возвращает значения валюты по ключевым параметрам из базы данных
    :param bank:
    :param date:
    :param currency:
    :return: [buy_value, sell_value]
    """
    conn = connect_db()
    sql = "select buy_value, sell_value from curr_history where bank = ? and date = ? and currency = ?;"
    try:
        cursor = conn.cursor()
        q = cursor.execute(sql, (bank, date, currency))
        buy_value, sell_value = q.fetchone()
        rez = [buy_value, sell_value]
        return rez
    finally:
        conn.close()

# ДЛЯ ТЕСТОВ
if __name__ == "__main__":
    # создание таблицы (используется один раз либо после удаления таблицы при тестах)
    # create_table()

    currency_bd_tmp = [
        {'bank': 'NBU', 'date': '2022-11-25', 'currency': 'UAH', 'buy_value': 0.025, 'sell_value': 0.022},
        {'bank': 'NBU', 'date': '2022-11-25', 'currency': 'EUR', 'buy_value': 0.9, 'sell_value': 0.9},
        {'bank': 'NBU', 'date': '2022-11-25', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'NBU', 'date': '2022-11-25', 'currency': 'GPB', 'buy_value': 1.1, 'sell_value': 1.2},

        {'bank': 'Privatbank', 'date': '2022-11-25', 'currency': 'UAH', 'buy_value': 0.026, 'sell_value': 0.023},
        {'bank': 'Privatbank', 'date': '2022-11-25', 'currency': 'EUR', 'buy_value': 0.91, 'sell_value': 0.96},
        {'bank': 'Privatbank', 'date': '2022-11-25', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'Privatbank', 'date': '2022-11-25', 'currency': 'GPB', 'buy_value': 1.11, 'sell_value': 1.21},

        {'bank': 'Monobank', 'date': '2022-11-25', 'currency': 'UAH', 'buy_value': 0.027, 'sell_value': 0.024},
        {'bank': 'Monobank', 'date': '2022-11-25', 'currency': 'EUR', 'buy_value': 0.92, 'sell_value': 0.97},
        {'bank': 'Monobank', 'date': '2022-11-25', 'currency': 'USD', 'buy_value': 1, 'sell_value': 1},
        {'bank': 'Monobank', 'date': '2022-11-25', 'currency': 'GPB', 'buy_value': 1.12, 'sell_value': 1.22},
    ]
    # внесение данных в таблицу (используется один раз либо после удаления таблицы при тестах)
    # insert_data_manual(currency_bd_tmp)

    # q = query_to_db('Monobank', '2022-11-25', 'UAH')
    # print(q)