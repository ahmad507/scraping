from datetime import datetime

from flask import Blueprint, request, jsonify

import app

bot = app.MandiriMcm(request)

urls = Blueprint('mandirimcm', __name__, )


@urls.route('/')
def index():
    return 'Hello, dari Mandiri MCM', 200


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
        company='xxxxxx',
        username='xxxxxx',
        password='xxxxxxxx',
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
    bot.ambil_mutasi('07/07/2021', '15/07/2021')
    return 'ambil mutasi', 200


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
        scraping = app.MandiriMcm()
        response = scraping.autorun(
            company=request.form.get('company'),
            username=request.form.get('username'),
            password=request.form.get('password'),
            rekening=request.form.get('rekening'),
            from_date=datetime.strptime(request.form.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y'),
            to_date=datetime.strptime(request.form.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        )
        result = response
    else:
        scraping = app.MandiriMcm()
        response = scraping.autorun(
            company='xxxxxx',
            username='xxxxxx',
            password='xxxxxx',
            rekening='xxxxxxx',
            from_date='07/07/2021',
            to_date='15/07/2021',
        )
        result = response

    return jsonify(result), status
