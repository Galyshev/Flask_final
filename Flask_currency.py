from flask import Flask, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from celery_work import time_update
from BD import Model_db
from BD.alchemy import engine, db_session
from flask import session as flsk_sess


flask_app = Flask(__name__)
flask_app.secret_key = 'jbhjvgjhkjjghjkdsdfsd'


def fix(num, sign = 0):
    '''
    функия возвращает заданное количество чисел после запятой
    :param num: число
    :param sign: кол-во знаков после запятой, по умолчанию - 0
    :return: отформатированное число
    '''
    return f"{num:.{sign}f}"


# Стартовая страница, с приветствием, полезной информацией. Данные не вводятся. Есть переадресация на Login и Register
@flask_app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@flask_app.route("/Register", methods=['GET', 'POST'])
def Register():
    if request.method == 'GET':

        return render_template('register.html')
    else:
        user = request.form['login']
        password = request.form['psw']
        email = request.form['email']
        # можно сделать проверку правильности ввода почты, но это не цель этого урока

        with Session(engine) as session:
            insert_query = Model_db.Users(user=user, password=password, email=email)
            session.add(insert_query)
            session.commit()
        return render_template('register_ok.html')


@flask_app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_form = request.form['login']
        password_form = request.form['psw']
        query_login = db_session.query(Model_db.Users).filter_by(user=user_form)
        chk_login = ''
        chk_password = None
        for i in query_login:
            chk_login = i.user
            chk_password = i.password
        if chk_login == '':
            return render_template('login.html', no_login=True)
        if chk_password == password_form:
            flsk_sess['username'] = chk_login
            # автоматическая переадресация на функционал программы
            data_cur = [{'cur': 'UAH'}, {'cur': 'EUR'}, {'cur': 'USD'}, {'cur': 'GPB'}]
            return render_template('currency.html', bank_from_form='NBU', data_cur=data_cur)
        else:
            return render_template('login.html', no_password=True)




# выход из авторизации и возврат на стартовую страницу
@flask_app.route("/Logout", methods=['GET'])
def Logout():
    if 'username' in flsk_sess:
        flsk_sess.pop('username', None)
        return render_template('index.html')
    else:
        return "Вы не авторизированы"



# странциа пользователя. Переход на страницу Currency или Logout
@flask_app.route("/User_page", methods=['GET'])
def User_page():
    if 'username' in flsk_sess:
        return f'Logged in as {flsk_sess["username"]}'
    return 'You are not logged in'


# страница с формой запроса для получения параметров.
@flask_app.route("/Currency", methods=['GET', 'POST'])
def Currency():
    if request.method == 'GET':
        # Если кто то вводит эндпоинт вручную, минуя авторизацию
        if 'username' in flsk_sess:
            # в качестве параметра bank_from_form передается банк по умолчанию, верхний из списка, иначе идет из ветки
            # else в currency.html, а это самый нижний, что мне не нравится визуально )
            data_cur = [{'cur': 'UAH'}, {'cur': 'EUR'}, {'cur': 'USD'}, {'cur': 'GPB'}]
            return render_template('currency.html', bank_from_form='NBU', data_cur=data_cur)
        else:
            return render_template('login.html')
    else:
        if 'username' in flsk_sess:
            bank_from_form = request.form['bank']
            curr_base_from_form = request.form.get('currency_1')
            curr_conv_from_form = request.form['currency_2']
            date_from_form = request.form['date']

            currency = Model_db.Currency
            with Session(engine) as session:
                query_1 = select(currency).filter_by(bank=bank_from_form,
                                                             currency=curr_base_from_form,
                                                             date=date_from_form)
                query_list_base_curr = session.scalars(query_1).one()
                query_2 = select(currency).filter_by(bank=bank_from_form,
                                                     currency=curr_conv_from_form,
                                                     date=date_from_form)
                query_list_conv_curr = session.scalars(query_2).one()
            buy_base_curr, sell_base_curr = query_list_base_curr.buy_value, query_list_base_curr.sell_value
            buy_conv_curr, sell_conv_curr = query_list_conv_curr.buy_value, query_list_conv_curr.sell_value
            buy_exchange = buy_conv_curr / buy_base_curr
            sell_exchange = sell_conv_curr / sell_base_curr

            # функия возвращает заданное количество чисел после запятой
            buy_exchange = fix(buy_exchange, 2)
            sell_exchange = fix(sell_exchange, 2)

            lst_base_cur = [{'cur': 'UAH'}, {'cur': 'EUR'}, {'cur': 'USD'}, {'cur': 'GBP'}]
            lst_conv_cur = [{'cur': 'UAH'}, {'cur': 'EUR'}, {'cur': 'USD'}, {'cur': 'GBP'}]

            # код ниже удаляет кодировки валюты, заданные в форме запроса из общего списка, что бы не дублировались
            i = 0
            for element in lst_base_cur:
                if element['cur'] == curr_base_from_form:
                    lst_base_cur.pop(i)
                    break
                i = i + 1
            y = 0
            for element in lst_conv_cur:
                if element['cur'] == curr_conv_from_form:
                    lst_conv_cur.pop(y)
                    break
                y = y + 1
            return render_template('currency.html', bank_from_form=bank_from_form,
                                   curr_base_from_form=curr_base_from_form,
                                   buy_exchange=buy_exchange,
                                   sell_exchange=sell_exchange,
                                   curr_conv_from_form=curr_conv_from_form,
                                   date_from_form=date_from_form,
                                   lst_base_cur=lst_base_cur,
                                   lst_conv_cur=lst_conv_cur
                                   )
        else:
            return render_template('login.html')

if __name__ == '__main__':
    flask_app.run(debug=True, host="0.0.0.0", port=5000)
