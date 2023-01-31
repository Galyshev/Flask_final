from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, Float, DateTime
from BD.alchemy import Base


class Currency(Base):
    __tablename__ = "curr_history"

    id = Column(Integer, primary_key=True)
    bank = Column(String)
    date = Column(String)
    currency = Column(String)
    buy_value = Column(Float)
    sell_value = Column(Float)
    # добавление новой колонки, создание второй миграции (техническая колонка с добавлением времени запроса)
    date_add = Column(DateTime, default=datetime.utcnow)

    def __init__(self, bank, date, currency, buy_value, sell_value):
        self.bank = bank
        self.date = date
        self.currency = currency
        self.buy_value = buy_value
        self.sell_value = sell_value


    def __repr__(self):
        return f"Currency(id={self.id!r}, bank={self.bank!r}, date={self.date!r}, currency={self.currency!r}, " \
               f"buy_value={self.buy_value!r},sell_value={self.sell_value!r})"

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    user = Column(String)
    password = Column(String)

    # добавление новой колонки, создание третьей миграции
    email = Column(String)

    def __init__(self, user, password, email):
        self.user = user
        self.password = password
        self.email = email


    def __repr__(self):
        return f"Users(id={self.id!r}, user={self.user!r}, password={self.password!r}, email={self.email!r})"