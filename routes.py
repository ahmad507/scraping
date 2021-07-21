import os
from copy import deepcopy
from datetime import datetime
from pyquery import PyQuery as Pq
from flask import Blueprint, send_from_directory, jsonify
from app.remote.errorhandler import log

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


# noinspection DuplicatedCode
@urls.route('/testscrap')
def test_scrap():
    f = None
    result = []
    try:
        f = open('mutasi.html', 'r')
        page_source = Pq(f.read())
        table_ = Pq(page_source)('.table-div')
        body_ = Pq(table_)('.tbody .clearfix')
        div_tr = Pq(body_)('.tr')
        i = 1
        for row in div_tr:
            log.info('Ambil baris: ' + str(i))
            kolom = {}
            mutasi = Pq(row)('.td')
            kolom['tanggal'] = Pq(mutasi[1])('span').text()
            kolom['keterangan'] = Pq(mutasi[2])('span').text()
            kolom['code'] = Pq(mutasi[3])('span').text()
            kolom['debet'] = Pq(mutasi[4])('span').text()
            kolom['kredit'] = Pq(mutasi[5])('span').text()
            kolom['saldo'] = Pq(mutasi[6])('span').text()
            result.append(deepcopy(kolom))
            i += 1
    except Exception as e:
        log.error(e.args)
    finally:
        f.close()

    return jsonify(result), 200
