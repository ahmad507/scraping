from datetime import datetime

from flask import Blueprint, request, jsonify

import app

bot = app.MandiriLivin(request)

urls = Blueprint('mandirilivin', __name__, )


@urls.route('/')
def index():
    return 'Hello, dari Mandiri Livin', 200


@urls.route('/startdriver')
def start_driver():
    bot.start_driver()
    return 'start driver', 200


@urls.route('/bahasa')
def ganti_bahasa():
    bot.ganti_bahasa()
    return 'ganti bahasa', 200


@urls.route('/login')
def login():
    bot.login(
        company='xxx',
        username='xxxxx',
        password='xxxxx',
    )
    return 'login', 200


@urls.route('/logout')
def logout():
    bot.logout()
    return 'logout', 200


@urls.route('/quitdriver')
def quit_driver():
    bot.quit_driver()
    return 'quit driver', 200


@urls.route('/closetab')
def close_tab():
    bot.close_tab()
    return 'close web tab', 200


@urls.route('/ambilmutasi')
def ambilmutasi():
    # format date utk melalui post (/mutasi), Y-m-d
    result = bot.ambil_mutasi('xxxxxxxx', '07/07/2021', '15/07/2021')
    return jsonify(result), 200


@urls.route('/closepopup')
def close_popup():
    bot.close_popup()
    return 'close popup', 200


@urls.route('/mutasi', methods=['GET', 'POST'])
def mutasi():
    result = {
        'message':
            'Required POST: company, username, password, rekening, from_date, to_date'
    }
    status = 422

    if request.method == 'POST':
        response = bot.autorun(
            company=request.form.get('company'),
            username=request.form.get('username'),
            password=request.form.get('password'),
            rekening=request.form.get('rekening'),
            from_date=datetime.strptime(request.form.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y'),
            to_date=datetime.strptime(request.form.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        )
        result = response
        status = 200
    # else:
    #     response = bot.autorun(
    #         company='xxxx',
    #         username='xxx',
    #         password='xxxx',
    #         rekening='xxxxxx',
    #         from_date='17/07/2021',
    #         to_date='17/07/2021',
    #     )
    #     result = response
    #     status = 201

    return jsonify(result), status
