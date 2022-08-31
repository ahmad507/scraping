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
        company='VSQA001',
        username='vrs01',
        password='Versa2021',
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
    result = bot.ambil_mutasi('1210006595999')
    return jsonify(result), 200


@urls.route('/closepopup')
def close_popup():
    bot.close_popup()
    return 'close popup', 200


@urls.route('/mutasi', methods=['GET', 'POST'])
def mutasi():
    result = {
        'message':
            'Required POST: company, username, password, rekening'
    }
    status = 422

    if request.method == 'POST':
        # form_date dan to_date not require
        result = bot.autorun(
            company=request.form.get('company'),
            username=request.form.get('username'),
            password=request.form.get('password'),
            rekening=request.form.get('rekening'),
            # from_date=datetime.strptime(request.form.get('from_date'), '%Y-%m-%d').strftime('%m/%d/%Y'),
            # to_date=datetime.strptime(request.form.get('to_date'), '%Y-%m-%d').strftime('%m/%d/%Y')
        )
        if result['code'] == 'OK':
            status = 200
        else:
            status = 417
    # else:
    #     response = bot.autorun(
    #         company='xxxxx',
    #         username='xxxx',
    #         password='xxxxx',
    #         rekening='xxxxxx',
    #     )
    #     result = response
    #     status = 201

    return jsonify(result), status
