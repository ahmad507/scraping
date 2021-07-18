import logging
import sys

logging.basicConfig(
    filename='myapp.log',  # Tutup untuk lihat log di console
    format='%(asctime)s.%(msecs)03d %(module)s->%(funcName)s: %(levelname)s: %(''message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)  # set level, Production -> ERROR, Development -> INFO/DEBUG


class MyException(Exception):
    def __init__(self):
        Exception.__init__(self)
        # sys.tracebacklimit = 0  # Tutup untuk lihat traceback
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        self.message = ('"{}", Line {}, {}'.format(filename, lineno, repr(exc_obj)))

    def __STR__(self):
        return self.message
