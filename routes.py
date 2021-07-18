import os
from datetime import datetime

from flask import Blueprint, send_from_directory
from app.remote.errorhandler import log

company = 'MKDG001'
username = 'HAFSYAH'
password = 'Tes192021'
rekening = '1210000448880'
from_date = 'ga tau'
to_date = 'sama'

urls = Blueprint('defaults', __name__, )


@urls.route('/')
def index():
    return f'<p>Hai, Windows IIS from Flask framework.</p> <h1>{datetime.now()}</h1>', 200


@urls.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(urls.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@urls.errorhandler(404)
def not_found():
    return {"message": "Invalid route"}, 404


@urls.route('/hello')
def hello_world():
    return 'Hello World!', 200


@urls.route('/print')
def print_msg():
    log.critical('testing CRITICAL log')
    log.error('testing ERROR log')
    log.warning('testing WARNING log')
    log.info('testing INFO log')
    log.debug('testing DEBUG log')
    return "Check your console", 200
