import os
import random
import datetime

from celery import Celery
from BD import Model_db
from BD.alchemy import engine, db_session
from sqlalchemy.orm import Session
from all_bank_from_api import PrivatBank, NBU, Monobank

rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
celery = Celery('celery_work', broker=f'pyamqp://guest@{rabbit_host}//')


# перед запуском воркера во втором терминале запустить "celery -A celery_work beat -s ./utils/celerybeat-schedule.db"
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(360.0, time_update.s())

@celery.task()
def time_update():
    date_privat = datetime.datetime.now().strftime("%d.%m.%Y")
    db_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # для ПРИВАТА
    query = db_session.query(Model_db.Currency).filter_by(bank='Privatbank', date=db_date)
    chk_date = ''
    for i in query:
        chk_date = i.date
    if chk_date == '':
        PrivatBank(date_privat, db_date)
    # для НБУ
    query = db_session.query(Model_db.Currency).filter_by(bank='NBU', date=db_date)
    chk_date = ''
    for i in query:
        chk_date = i.date
    if chk_date == '':
        NBU(date_privat, db_date)
    # для МОНОБАНКА
    query = db_session.query(Model_db.Currency).filter_by(bank='Monobank', date=db_date)
    chk_date = ''
    for i in query:
        chk_date = i.date
    if chk_date == '':
        Monobank()
    return 'OK'

# time_update()


