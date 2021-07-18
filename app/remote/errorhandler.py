import logging
import sys

logging.basicConfig(
    filename='myapp.log',  # Tutup untuk lihat log di console
    format='%(asctime)s.%(msecs)03d %(module)s->%(funcName)s: %(levelname)s: %(''message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)  # set level, Production -> ERROR, Development -> INFO/DEBUG


def err_catch(e_less):
    message = e_less
    try:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message = ('"{}", Line {}, {}'.format(filename, lineno, repr(exc_obj)))
    except Exception as e:
        log.error('Tolong benarin errorhandler.py')
        log.error(e)

    return message
